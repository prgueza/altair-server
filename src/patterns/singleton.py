from __future__ import annotations

from typing import Optional

from ..beer.beerdb import *


class SingletonMetaClass(type):
    """
    As the BeerDB class acts as a database it might be useful to declare it as a Singleton so every call to the
    class constructor method results in the same instance. This helps observation declarations on the BeerDB class.
    IMPORTANT NOTE: This is not thread safe! But as we are not using multi threading and this is just for demo purposes
    we can live with it
    """
    _instance: Optional[BeerDB] = None

    def __call__(cls) -> BeerDB:
        """
        Singleton Pattern: Extending BeerDB using this metaclass and memoizing the instance in the _instance variable
        makes every initialization of the BeerDB class, but the first one, return the original instance (declared in
        the first initialization)
        :return: The BeerDB instance if it exists or the newly created BeerDB Singleton if it doesn't
        """
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance
