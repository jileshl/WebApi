from tastypie.resources import Resource
from demo.models.job import Job
from demo.demoManager import DemoManager


class EmployeeResource(Resource):
    class Meta:        
        resource_name = 'jobs'
        allowed_methods = ['get']
        urlconf_namespace = None
        include_resource_uri = False

    def obj_get(self, request=None, **kwargs):
        #print kwargs['pk']
        result =DemoManager().GetJob(kwargs['pk'])       
        return result
        
    def obj_get_list(self, request=None, **kwargs):
        result = DemoManager().GetJobList()
        return result
    
    
    def dehydrate(self, bundle):
        bundle.data = bundle.obj.__dict__
        return bundle
    
class JobAddResource(Resource):
    class Meta:        
        resource_name = 'addjob'
        allowed_methods = ['post']
        urlconf_namespace = None
        include_resource_uri = False
        
    def obj_create(self, bundle, request=None, **kwargs):
        print ''