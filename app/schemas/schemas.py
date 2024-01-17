from enum import Enum
from typing import List

from pydantic import BaseModel


class LanguageEnum(str, Enum):
    ENGLISH = "English"
    GERMAN = "German"
    FRENCH = "French"
    ITALIAN = "Italian"


class PlatformEnum(str, Enum):
    CALL = "call"
    FACEBOOK_CHAT = "facebook_chat"
    WEBSITE_CHAT = "website_chat"
    EMAIL = "email"


class TicketRequest(BaseModel):
    id: str
    restrictions: List[LanguageEnum]
    platform: PlatformEnum


class Ticket(BaseModel):
    id: str
    languages: List[LanguageEnum]
    platform: PlatformEnum


class AgentSchema(BaseModel):
    name: str
    languages: List[LanguageEnum]
    available_for_voice_call: bool
    available_for_every_call: bool
    text_call_count: int
    voice_call_count: int
    total_assigned_tasks: int
