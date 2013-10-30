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


class PayoffQuoteResponseResource(Resource):
    """
    Resource that represents a PayoffQuoteResponse.  Provides methods that
    are used when exposing resource via a RESTful API.
    """
    class Meta:
        '''
        meta class for resource
        '''
        object_class = Location
        resource_name = 'location'
        authorization = Authorization()
        allowed_methods = ['post']

    def obj_create(self, bundle, request=None, **kwargs):
        '''
        function to pass data to dtplatform
        '''
        bundle = self.full_hydrate(bundle)
        resp = create_location(bundle.data)
        return resp

    def get_resource_uri(self, bundle_or_obj=None, url_name='uri_dispatch_list'):
        '''
        method to provide reverse uri for service call
        '''
        return ""
