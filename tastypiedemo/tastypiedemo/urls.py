from django.conf.urls import patterns, include, url
from demo.api import EmployeeResource
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
employee_job = EmployeeResource()


urlpatterns = patterns('',
                       url(r'^tastypiedemo/', include(employee_job.urls)),
    # Examples:
    # url(r'^$', 'tastypiedemo.views.home', name='home'),
    # url(r'^tastypiedemo/', include('tastypiedemo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
