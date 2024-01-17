from fastapi import APIRouter

from app.business_logic.publish_ticket import publish_ticket
from app.schemas.schemas import Ticket, TicketRequest

router = APIRouter()


@router.post("/assign")
async def assign_ticket(payload: TicketRequest) -> None:
    ticket = Ticket(
        id=payload.id, languages=payload.restrictions, platform=payload.platform
    )

    return await publish_ticket(ticket=ticket)
