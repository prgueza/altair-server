import logging
from typing import List

from src.helpers.exceptions import NotFoundException
from src.patterns.decorators import *
from src.patterns.observer import Observable, Observer
from src.patterns.singleton import BeerDBMetaClass


class BeerDB(Observable):
    """
    BeerDB declares a list which will be the beer collection. Extending this class from the SingletonMetaClass will
    ensure that this class is a Singleton, and there is only one BeerDB at any moment. This will be useful when we try
    to observe this class from the Socket Handler Class
    """
    __beers = []

    # To avoid metaclass conflicts
    __metaclass__ = BeerDBMetaClass

    """
    We have used the Observable class here so we can notify on DB updates to any other class that might want to be 
    notified, somehow simulating DB Hooks
    """
    __observers: List[Observer] = []

    """
    We implement methods from the abstract class which make this class able to store observers and notify them when 
    changes are made
    """

    def attach(self, observer) -> None:
        """
        Attach: Attaches the observer to the BeerDB Singleton
        :param observer: The observer that has to be attached to this class
        :return: None
        """
        logging.info('Instance with id %s is observing DB updates', id(observer))
        self.__observers.append(observer)

    def notify(self, message) -> None:
        """
        Notify: Calling this method will notify attached observers trough their on_notify method
        :param message: Message that will be passed to the notified observers
        :return: None
        """
        # We pass a message for simple notifications and the db instance for more complex operations
        for observer in self.__observers:
            observer.on_notify(self, message)

    @property
    def beers(self):
        """
        Beers property: The collection of beers stored in the db
        :return: A collection of beers
        """
        return self.__beers

    @property
    def count(self):
        """
        Count property: The number of beers in the collection
        :return: The total number of beers
        """
        return len(self.__beers)

    @serialize
    async def add(self, beer):
        """
        Add query: Adds a new beer to the collection
        :param beer: Beer to be added to the collection
        :return: Beer added to the collection
        """
        self.__beers.append(beer)
        self.notify('Tap with id ' + str(beer.tap_id) + ' posted a new beer (id: ' + str(beer.beer_id) + ')!')
        return beer

    async def delete(self, beer_id):
        """
        Delete by ID query: Deletes the beer with the specified ID from the collection
        :param beer_id: The id of the beer to be deleted
        :return: None
        """
        self.__beers = list(filter(lambda beer: beer.beer_id != int(beer_id), self.__beers))
        self.notify('Beer ' + str(beer_id) + ' deleted from the collection')

    @serialize
    async def find_by_id(self, beer_id):
        """
        Find By ID query: Returns the beer with the specified ID
        :param beer_id: The id of the beer to be returned
        :return: The beer with the corresponding id if found
        """
        result = list(filter(lambda beer: beer.beer_id == int(beer_id), self.beers))
        if len(result) == 0:
            raise NotFoundException('Beer with id ' + str(beer_id) + ' not found')
        return result[0]

    @serialize
    @paginate
    async def find(self):
        """
        Find All query: Returns a paginated and sorted list containing every beer stored in the db
        :return: A paginated list of beers
        """
        return self.beers

    @serialize
    @paginate
    async def find_by_type(self, beer_type):
        """
        Find By Type query: Returns a paginated and sorted list of beers corresponding to the specified beer type
        :param beer_type: The type of beer used as a filter
        :return: A paginated list of filtered beers
        """
        result = list(filter(lambda beer: beer.beer_type == beer_type, self.__beers))
        return result
