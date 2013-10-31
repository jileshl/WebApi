from sqlalchemy.orm import mapper

from .hr import employee
from base_model import BaseModel

__all__ = ['employee']

class Employee(BaseModel):
    '''
    Employee model
    
    '''
    def __init__(self, **kwargs):
        super(employee,self).__init__(**kwargs)
        
mapper(Employee, employees,
       properties = {
                     "Employee_Id": employee.c.employee_id,
                     "First_Name": employee.c.employee_id,
                     "Last_Name": employee.c.last_name,
                     "Email": employee.c.email,
                     "Phone_Number": employee.c.phone_number,
                     "Hire_Date": employee.c.hire_date,
                     "Job_Id": employee.c.job_id,
                     "Salary": employee.c.salary,
                     "Manager_Id": employee.c.manager_id,
                     "Department_Id": employee.c.departmentid,
                     })

