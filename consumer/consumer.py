import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.database import get_database_manager
from aio_pika import ExchangeType, connect_robust

from app.business_logic.assign_ticket import assign_ticket_to_agent
from app.schemas.schemas import Ticket
from config.config import Config
from config.constants import TEXT_MESSAGE_PRIORITY, VOICE_CALL_PRIORITY


async def consume_messages(queue_config):
    database_manager = await get_database_manager()

    connection = await connect_robust(Config().RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            queue_config["exchange"], ExchangeType.DIRECT
        )
        queue = await channel.declare_queue(
            name=queue_config["queue"],
            arguments={"x-max-priority": queue_config["priority"]},
        )
        await queue.bind(exchange, queue_config["routing_key"])

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(
                        f"Received message from {queue_config['queue']}: {message.body.decode()}"
                    )
                    ticket_message = message.body.decode()
                    ticket = Ticket(**json.loads(ticket_message))
                    agent = await assign_ticket_to_agent(
                        ticket=ticket, database_manager=database_manager
                    )
                    print(f"Ticket assigned to agent: {agent}")


if __name__ == "__main__":
    import asyncio

    queue_configs = [
        {
            "queue": "voice_call_queue",
            "exchange": "ticket_exchange",
            "routing_key": "voice_call",
            "priority": VOICE_CALL_PRIORITY,
        },
        {
            "queue": "text_message_queue",
            "exchange": "ticket_exchange",
            "routing_key": "text_message",
            "priority": TEXT_MESSAGE_PRIORITY,
        },
    ]

    loop = asyncio.get_event_loop()

    # Start consuming messages from each queue concurrently
    tasks = [consume_messages(queue_config) for queue_config in queue_configs]
    loop.run_until_complete(asyncio.gather(*tasks))
