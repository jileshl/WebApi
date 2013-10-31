import db
from demo.models.job import Job

class DemoManager(object):
    
    def GetJobList(self):              
        session = db.get_orm_session('default')
        result_list = session.query(Job).all()
        return result_list
    
    def GetJob(self , job_id):              
        session = db.get_orm_session('default')
        result_list = session.query(Job).filter(Job.job_id == job_id ).first()
        import pdb;pdb.set_trace()
        return result_list
    
   
    def AddJob(self, **kargs):
        session = db.get_orm_session('default')
        Jobs = Job() 
        Jobs.job_id  = kargs['job_id']      
        Jobs.job_title = kargs['job_title']
        Jobs.min_salary= kargs['min_salary']
        Jobs.max_salary= kargs['max_salary'] 
        session.add(Jobs)
        session.commit()
        #result_list = session.query(Job).Filter(Job.Job_ID == job_id ).all()
   #     return result_list