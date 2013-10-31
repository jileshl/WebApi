from sqlalchemy.orm import mapper

from .hr import jobs
from base_model import BaseModel

__all__ = ['Job']


class Job(BaseModel):
    '''
    job model
    '''
    def __init__(self, **kwargs):
        super(Job, self).__init__(**kwargs)

    @property
    def blah(self):
        return 'blah'

    @blah.setter
    def blah(self, val):
        self.city = val

mapper(Job, jobs,
       properties={'job_id': jobs.c.job_id,
                   'job_title': jobs.c.job_title,
                   'min_salary': jobs.c.min_salary,
                   'max_salary': jobs.c.max_salary,                   
                   })