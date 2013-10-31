from sqlalchemy.orm import mapper

from .hr import departments
from base_model import BaseModel

__all__ = ['Departments']

class Department(BaseModel):
    '''
    Department Model
    
    '''
    def __init__(self, **quargs):
        super(Job, self).__init__(**kwargs)
    
    @property
    def DepartmentLocation(self):
        return self.location_id
    
    @DepartmentLocation.setter
    def DepartmentLocation(self, val):
        self.DepartmentLocation = val
        
mapper(Department, departments,
       properties={'Department_ID': jobs.c.department_id,
                   'Department_Name': jobs.c.department_name,
                   'Manager_ID': jobs.c.manager_id,
                   'Location_ID': jobs.c.location_id,
                   })
        