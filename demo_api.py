"""
TastyPie API definition
"""
from tastypie.resources import Resource
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpAccepted
from tastypie.serializers import Serializer
from tastypie.exceptions import BadRequest

from models.location import Location
from manager import create_location

from dateutil import parser, relativedelta

import re
import datetime


class LocationResource(Resource):
    class Meta:
        '''
        meta class for resource
        '''
        object_class = Location
        resource_name = 'location'
        authorization = Authorization()
        allowed_methods = ['post']

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = self.full_hydrate(bundle)
        resp = create_location(bundle.data)
        return resp

    def get_resource_uri(self, bundle_or_obj=None, url_name='uri_dispatch_list'):
        '''
        method to provide reverse uri for service call
        '''
        return ""


class GetLeadResource(Resource):
    """
    API for Requesting PayoffQuote from any 3rd party Application
    """

    class Meta:
        '''
        meta class for resource
        '''
        object_class = LeadRequestManager
        resource_name = 'get'
        include_resource_uri = False
        always_return_data = True
        allowed_methods = ['get']
        default_format = 'application/json'

    def obj_get_list(self, request=None, **kwargs):
        '''
        This method is when a user tries to send request without
        any Lead Reference Id
        '''
        return {'error': 'Value Expected'}

    def obj_get(self, request=None, **kwargs):
        '''
        Overriding Tastypie Obj Create Method
        Get the Records from the db
        '''
        self._meta.default_format = 'application/json'
        lead = self._meta.object_class().get_lead(kwargs['pk'])
        if not lead:
            return {'error': 'No Records Found'}

        return lead

    def dehydrate(self, bundle):
        '''
        dehydrating the bundle object and copying it to the bundle data
        for serialization
        '''
        bundle.data = bundle.obj.__dict__
        return bundle

    def alter_detail_data_to_serialize(self, request, data):
        '''
        deleting the unwanted key(s) from the object
        '''
        del(data.data['_sa_instance_state'])

        return data

    def get_resource_uri(self, bundle_or_obj=None, url_name='api_dispatch_list'):
        '''
        method to provide reverse uri for service call
        '''
        return ""
