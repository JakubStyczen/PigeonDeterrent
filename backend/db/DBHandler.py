from abc import ABC, abstractmethod
from typing import Any, Optional
import logging
from DB import IDB, MongoDBColletion, IDataBaseRecord, DeterrentDataBaseRecord
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
from datetime import datetime


from bson.objectid import ObjectId

logger = logging.getLogger()


class IDBHandler(ABC):
    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError


class MongoDBHandler(IDBHandler):
    def __init__(
        self, ip: str = "localhost", port: int = 27017, uri: Optional[str] = None
    ) -> None:
        self.ip = ip
        self.port = port
        self.uri = uri
        self._db_client: Optional[MongoClient] = None
        self._db: IDB = None
        self.connect()

    def connect(self) -> None:
        if self._db_client is not None:
            logger.warning("MongoDB already connected!")
            return None
        credentials: tuple = (self.uri,) if self.uri else (self.ip, self.port)
        self._db_client = MongoClient(*credentials)
        self._db_client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
        logger.info("Connecting to db!")

    def disconnect(self) -> None:
        if self._db_client is None:
            logger.warning("MongoDB already disconnected!")
            return
        self._db_client = None
        logger.info("Disconnected from db!")

    def create_db_collection(self) -> None:
        if self._db_client is None:
            logger.warning("MongoDB connection has not been established yet!")
            return
        db = self._db_client.flask_database
        self._db = MongoDBColletion(db)
