from sqlalchemy.orm import mapper

from .hr import locations
from base_model import BaseModel

__all__ = ['Location']


class Location(BaseModel):
    '''
    Location model
    '''
    def __init__(self, **kwargs):
        super(Location, self).__init__(**kwargs)

    @property
    def blah(self):
        return 'blah'

    @blah.setter
    def blah(self, val):
        self.city = val

mapper(Location, locations,
       properties={'location_id': locations.c.location_id,
                   'street_address': locations.c.street_address,
                   'postal_code': locations.c.postal_code,
                   'city': locations.c.city,
                   'state_province': locations.c.state_province,
                   'country_id': locations.c.country_id,
                   })
