from tastypie.resources import Resource
from demo.models.job import Job
from demo.demoManager import DemoManager
from tastypie.authorization import Authorization


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
    
class JobsResource(Resource):
    class Meta:
        object_class = Job
        resource_name = 'addjob'
        allowed_methods = ['post']
        urlconf_namespace = None
        include_resource_uri = False
        authorization = Authorization()
        default_format = 'application/json'
        
    def obj_create(self, bundle, request=None, **kwargs):
        #import pdb; pdb.set_trace()        
        bundle = self.full_hydrate(bundle)        
        resp = DemoManager().AddJob(**bundle.data)
        return resp
    
    def get_resource_uri(self, bundle_or_obj=None, url_name='uri_dispatch_list'):
        '''
        method to provide reverse uri for service call
        '''
        return ""