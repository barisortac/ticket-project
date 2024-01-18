from typing import Optional

from app.database.manager import DatabaseManager
from app.models.agent import AgentModel
from app.schemas.schemas import PlatformEnum, Ticket
from config.constants import (
    MAXIMUM_NUMBER_OF_CALL_FOR_AGENT,
    MAXIMUM_NUMBER_OF_TASK_FOR_AGENT,
)

agent_collection = AgentModel


async def assign_voice_ticket_to_agent(
    *, agent: AgentModel, database_manager: DatabaseManager
):
    update_fields = {
        "voice_call_count": agent["voice_call_count"] + 1,
        "total_assigned_tasks": agent["total_assigned_tasks"] + 1,
        "available_for_voice_call": False,
    }

    await database_manager.update_agent(agent["_id"], update_fields)


async def assign_text_ticket_to_agent(
    *, agent: AgentModel, database_manager: DatabaseManager
):
    update_fields = {
        "text_call_count": agent["text_call_count"] + 1,
        "total_assigned_tasks": agent["total_assigned_tasks"] + 1,
    }

    if (
        agent["total_assigned_tasks"]
        == MAXIMUM_NUMBER_OF_TASK_FOR_AGENT - MAXIMUM_NUMBER_OF_CALL_FOR_AGENT
    ):
        update_fields["available_for_text_call"] = False

    await database_manager.update_agent(agent["_id"], update_fields)


async def assign_ticket(
    *, ticket: Ticket, agent: AgentModel, database_manager: DatabaseManager
):
    if ticket.platform == PlatformEnum.CALL:
        await assign_voice_ticket_to_agent(
            agent=agent, database_manager=database_manager
        )
    elif ticket.platform in [
        PlatformEnum.FACEBOOK_CHAT,
        PlatformEnum.WEBSITE_CHAT,
        PlatformEnum.EMAIL,
    ]:
        await assign_text_ticket_to_agent(
            agent=agent, database_manager=database_manager
        )


async def assign_ticket_to_agent(
    *, ticket: Ticket, database_manager: DatabaseManager
) -> Optional[AgentModel]:
    if ticket.platform == PlatformEnum.CALL:
        available_agent = await database_manager.get_available_agents_for_voice_call(
            ticket_languages=ticket.languages
        )

        if available_agent:
            await assign_ticket(
                ticket=ticket, agent=available_agent, database_manager=database_manager
            )
            return available_agent

    available_agent = await database_manager.get_agents_available_for_text_call(
        ticket_languages=ticket.languages
    )
    if available_agent:
        await assign_ticket(
            ticket=ticket, agent=available_agent, database_manager=database_manager
        )
        return available_agent

    return available_agent
