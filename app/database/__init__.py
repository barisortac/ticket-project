from app.database.manager import MongoManager
from config.config import Config


async def get_database_manager():
    db_manager = MongoManager()
    await db_manager.connect_to_database(path=Config().DATABASE_URL)

    return db_manager
