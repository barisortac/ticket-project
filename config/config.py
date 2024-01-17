from typing import Optional

from aio_pika import ExchangeType, connect_robust
from pydantic_settings import BaseSettings

from config.constants import (EXCHANGE_NAME, TEXT_MESSAGE_PRIORITY,
                              TEXT_MESSAGE_QUEUE_NAME,
                              TEXT_MESSAGE_ROUTING_KEY, VOICE_CALL_PRIORITY,
                              VOICE_CALL_QUEUE_NAME, VOICE_CALL_ROUTING_KEY)


class Config(BaseSettings):
    DATABASE_URL: Optional[str] = None
    RABBITMQ_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        from_attributes = True


voice_call_queue_options = {
    "name": VOICE_CALL_QUEUE_NAME,
    "arguments": {"x-max-priority": VOICE_CALL_PRIORITY},
}


text_message_queue_options = {
    "name": TEXT_MESSAGE_QUEUE_NAME,
    "arguments": {"x-max-priority": TEXT_MESSAGE_PRIORITY},
}


async def initialize_queues() -> None:
    connection = await connect_robust(Config().RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()

        # Declare the main exchange
        exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.DIRECT)

        # Declare and bind voice call queue
        voice_call_queue = await channel.declare_queue(**voice_call_queue_options)
        await voice_call_queue.bind(exchange, routing_key=VOICE_CALL_ROUTING_KEY)

        # Declare and bind text message queue
        text_message_queue = await channel.declare_queue(**text_message_queue_options)
        await text_message_queue.bind(exchange, routing_key=TEXT_MESSAGE_ROUTING_KEY)
