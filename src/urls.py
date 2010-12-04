from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^news/', include('news.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

import sys
if 'runserver' in sys.argv or 'runserver_plus':
    urlpatterns = patterns('', url(
        r'^media/(.*)$',
        'django.views.static.serve',
        kwargs={'document_root': os.path.join(settings.PROJECT_PATH, 'media')}
    ),) + urlpatterns
