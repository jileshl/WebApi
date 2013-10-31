import db
from demo.models.job import Job
from demo.models.employee import Employee

class DemoManager(object):
    
    def GetJobList(self):              
        session = db.get_orm_session('default')
        result_list = session.query(Job).all()
        #import pdb; pdb.set_trace()
        return result_list
    
    def GetJob(self , job_id):              
        session = db.get_orm_session('default')
        result_list = session.query(Job).filter(Job.job_id == job_id ).first()
        #import pdb;pdb.set_trace()
        return result_list
    
   
    def AddJob(self, **kargs):
        session = db.get_orm_session('default')
        Jobs = Job() 
        #import pdb; pdb.set_trace()
        Jobs.job_id  = kargs['job_id']      
        Jobs.job_title = kargs['job_title']
        Jobs.min_salary= kargs['min_salary']
        Jobs.max_salary= kargs['max_salary'] 
        session.add(Jobs)
        session.commit()
        #result_list = session.query(Job).Filter(Job.Job_ID == job_id ).all()
   #     return result_list
   
    def AddEmployee(self, **kargs):
       session = db.get_orm_session('default')
       Employee = Employee()
       Employee.Employee_Id = kargs['employee_id']
       Employee.First_Name = kargs['first_name']
       Employee.Last_Name = kargs['last_name']
       Employee.Email = kargs['email']
       Employee.Phone_Number = kargs['phone_number']
       Employee.Hire_Date = kargs['hire_date']
       Employee.Job_Id = kargs['job_id']
       Employee.Salary = kargs['salary']
       Employee.Manager_Id = kargs['manager_id']
       Employee.Department_Id = kargs['department_id']
       session.add(Employee)
       session.commit()
       
       