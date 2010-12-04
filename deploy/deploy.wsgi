import os
import sys
import site

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/www/django/.python-eggs'

site.addsitedir('/var/www/django/<domain>/env/lib/python2.6/site-packages')
sys.path.append('/var/www/django/<domain>/src')
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
