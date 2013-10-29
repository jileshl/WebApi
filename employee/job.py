from sqlalchemy.orm import mapper

from .hr import jobs
from base_model import BaseModel

__all__ = ['Job']

class Job(BaseModel):
    '''
    Job model
    '''
    def __init__(self, **kwargs):
        super(Job, self).__init__(**kwargs)

    @property
    def blah(self):
        return 'blah'

    @blah.setter
    def blah(self, val):
        self.job_title = val

mapper(Job, jobs,
       properties={'Job_Code': jobs.c.job_id,
                   'Designation': jobs.c.job_title,
                   'Salary_Minimum': jobs.c.min_salary,
                   'Salary_Maximum': jobs.c.max_salary,
                   })