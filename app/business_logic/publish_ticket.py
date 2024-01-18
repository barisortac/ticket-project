from aio_pika import ExchangeType, Message, connect_robust

from app.schemas.schemas import PlatformEnum, Ticket
from config.config import Config
from config.constants import (
    EXCHANGE_NAME,
    TEXT_MESSAGE_PRIORITY,
    TEXT_MESSAGE_QUEUE_NAME,
    TEXT_MESSAGE_ROUTING_KEY,
    VOICE_CALL_PRIORITY,
    VOICE_CALL_QUEUE_NAME,
    VOICE_CALL_ROUTING_KEY,
)


async def _publish_ticket(
    *, ticket: Ticket, queue_name: str, routing_key: str, priority: int
) -> None:
    connection = await connect_robust(Config().RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()

        # Declare the exchange if it doesn't exist
        exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.DIRECT)

        # Declare the queue with priority
        queue = await channel.declare_queue(
            queue_name, arguments={"x-max-priority": priority}
        )

        # Bind the queue to the exchange with the routing key
        await queue.bind(exchange, routing_key)

        # Publish the message
        await exchange.publish(
            Message(body=ticket.model_dump_json().encode()),
            routing_key=routing_key,
        )


async def publish_voice_ticket(*, ticket: Ticket) -> None:
    await _publish_ticket(
        ticket=ticket,
        queue_name=VOICE_CALL_QUEUE_NAME,
        routing_key=VOICE_CALL_ROUTING_KEY,
        priority=VOICE_CALL_PRIORITY,
    )


async def publish_text_ticket(*, ticket: Ticket) -> None:
    await _publish_ticket(
        ticket=ticket,
        queue_name=TEXT_MESSAGE_QUEUE_NAME,
        routing_key=TEXT_MESSAGE_ROUTING_KEY,
        priority=TEXT_MESSAGE_PRIORITY,
    )


async def publish_ticket(*, ticket: Ticket) -> None:
    if ticket.platform == PlatformEnum.CALL:
        await publish_voice_ticket(ticket=ticket)
    elif ticket.platform in [
        PlatformEnum.FACEBOOK_CHAT,
        PlatformEnum.WEBSITE_CHAT,
        PlatformEnum.EMAIL,
    ]:
        await publish_text_ticket(ticket=ticket)
    else:
        raise NotImplementedError("Ticket platform is not supported")
