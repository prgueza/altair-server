from datetime import datetime

from src.helpers.exceptions import UnValidVolumeError

beer_types = [
    {'type': 'half', 'range': [100, 300]},
    {'type': 'pint', 'range': [300, 800]},
    {'type': 'stein', 'range': [800, 1000]}
]


class Beer:
    """
    Beer class which model the beer resource that is stored as an entry in the database. The constructor infers the
    glass type from the volume and has an exception handler that will raise an exception when the volume has no
    corresponding glass type
    """

    def __init__(self, tap_id, beer_id, volume):
        self.__tap_id = tap_id
        self.__beer_id = beer_id
        self.__volume = volume
        self.__timestamp = datetime.utcnow()
        beer_type = list(filter(lambda beer: beer['range'][0] <= volume <= beer['range'][1], beer_types))
        if len(beer_type) == 0:
            raise UnValidVolumeError('There is no glass type for the specified volume')
        self.__beer_type = beer_type[0]['type']

    """
    Once initialized, the properties should not mutated (we are not considering using an update method) so we expose 
    these properties as such using the @property decorator. State properties are meant to be private here.  
    """

    @property
    def tap_id(self):
        return self.__tap_id

    @property
    def beer_id(self):
        return self.__beer_id

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def volume(self):
        return self.__volume

    @property
    def beer_type(self):
        return self.__beer_type

    def serialize(self):
        """
        The serialize function takes the data from the beer object and serializes it as JSON
        :return: A serialized version of the beer
        """
        return {
            'id': self.beer_id,
            'type': self.beer_type,
            'volume': self.volume,
            'timestamp': self.timestamp.isoformat(),
            'tapId': self.tap_id
        }

    def describe(self):
        """
        The describe function returns a string describing in a human readable way the contents of the beer object
        :return: A string detailing the beer's properties
        """
        return self.timestamp.isoformat() \
               + ' - tap_id: ' + str(self.tap_id) \
               + ' - beer_id: ' + str(self.beer_id) \
               + ' - type: ' + self.beer_type \
               + ' - ml: ' + str(self.volume)
