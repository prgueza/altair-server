from __future__ import annotations
from abc import ABC, abstractmethod
from src.beer.beerdb import *


class Observable(ABC):
    """
    Observable abstract class which provides Observable classes with the abstract methods attach and notify. Usually we
    would include a detach method too but we are not going to use it in this scenario so we won't include it for
    simplicity
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self, message) -> None:
        pass


class Observer(ABC):
    """
    Observer abstract class which provides Observer classes with the on_notify method, which will be called from the
    observed class whenever the notify method is called
    """

    @abstractmethod
    def on_notify(self, db: BeerDB, message) -> None:
        pass
