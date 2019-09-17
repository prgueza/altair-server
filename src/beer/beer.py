from datetime import datetime

from src.helpers.exceptions import UnValidVolumeError

beer_types = [
    {'type': 'half', 'range': [100, 300]},
    {'type': 'pint', 'range': [300, 800]},
    {'type': 'stein', 'range': [800, 1000]}
]


class Beer:

    def __init__(self, tap_id, beer_id, volume):
        self.__tap_id = tap_id
        self.__beer_id = beer_id
        self.__volume = volume
        self.__timestamp = datetime.utcnow()
        beer_type = list(filter(lambda beer: beer['range'][0] <= volume <= beer['range'][1], beer_types))
        if len(beer_type) == 0:
            raise UnValidVolumeError('There is no glass type for the specified volume')
        self.__beer_type = beer_type[0]['type']

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
        return {
            'id': self.beer_id,
            'type': self.beer_type,
            'volume': self.volume,
            'timestamp': self.timestamp.isoformat(),
            'tapId': self.tap_id
        }

    def describe(self):
        return self.timestamp.isoformat() \
               + ' - tap_id: ' + str(self.tap_id) \
               + ' - beer_id: ' + str(self.beer_id) \
               + ' - type: ' + self.beer_type \
               + ' - ml: ' + str(self.volume)
