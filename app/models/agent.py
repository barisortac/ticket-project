from beanie import Document

from app.schemas.schemas import AgentSchema


class AgentModel(AgentSchema, Document):
    # I directly inherited AgentSchema since they are the same, we can seperate those
    class Config:
        json_schema_extra = {
            "example": {
                "name": "A",
                "languages": ["English", "German"],
                "available_for_voice_call": False,
                "available_for_text_call": True,
                "text_call_count": 1,
                "voice_call_count": 1,
                "total_assigned_tasks": 2,
            }
        }
        from_attributes = True

    class Settings:
        name = "agent"
