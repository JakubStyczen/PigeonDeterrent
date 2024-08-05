from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class IDeterrent(ABC):
    @abstractmethod
    def deter(self) -> None:
        raise NotImplementedError


class ServoDeterrent(IDeterrent):
    def __init__(self) -> None:
        pass

    def deter(self) -> None:
        pass
