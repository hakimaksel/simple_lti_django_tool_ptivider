from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^lti_tool$', 'tool_provider.views.lti_tool'),
    url(r'^assessment$', 'tool_provider.views.assessment'),
    # url(r'^$', 'django_tool_provider.views.home', name='home'),
    # url(r'^django_tool_provider/', include('django_tool_provider.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
