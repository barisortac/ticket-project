import logging
from abc import abstractmethod
from typing import List, Optional

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.models.agent import AgentModel
from app.schemas.schemas import LanguageEnum

# I used a manager to have a better dependency injection


class DatabaseManager:
    @property
    def client(self):
        raise NotImplementedError

    @property
    def db(self):
        raise NotImplementedError

    @abstractmethod
    async def connect_to_database(self, path: str):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def get_available_agents_for_voice_call(
        self,
        ticket_languages: List[LanguageEnum],
    ) -> Optional[AgentModel]:
        pass

    @abstractmethod
    async def get_agents_available_for_text_call(
        self,
        ticket_languages: List[LanguageEnum],
    ) -> Optional[AgentModel]:
        pass

    @abstractmethod
    async def update_agent(
        self,
        agent_id: ObjectId,
        update_fields: dict,
    ) -> None:
        pass


class MongoManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str):
        logging.info("Connecting to MongoDB.")
        self.client = AsyncIOMotorClient(path)

        self.db = self.client.ticket
        self.agent_collection = self.db.get_collection("agent")
        logging.info("Connected to MongoDB.")

    async def close_database_connection(self):
        logging.info("Closing connection with MongoDB.")
        self.client.close()
        logging.info("Closed connection with MongoDB.")

    async def get_available_agents_for_voice_call(
        self,
        ticket_languages: List[LanguageEnum],
    ) -> Optional[AgentModel]:
        agents = (
            await self.agent_collection.find(
                {
                    "available_for_voice_call": True,
                    "languages": {"$in": ticket_languages},
                }
            )
            .sort("total_assigned_tasks", 1)
            .limit(1)
            .to_list(length=None)
        )

        if agents:
            return agents[0]

        return None

    async def get_agents_available_for_text_call(
        self,
        ticket_languages: List[LanguageEnum],
    ) -> Optional[AgentModel]:
        agents = (
            await self.agent_collection.find(
                {
                    "available_for_text_call": True,
                    "languages": {"$in": ticket_languages},
                }
            )
            .sort("total_assigned_tasks", 1)
            .limit(1)
            .to_list(length=None)
        )

        if agents:
            return agents[0]

        return None

    async def update_agent(
        self,
        agent_id: ObjectId,
        update_fields: dict,
    ) -> None:
        await self.agent_collection.update_one(
            {"_id": agent_id}, {"$set": {**update_fields}}
        )
