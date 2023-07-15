"""
WSGI config for aw project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""


import os, sys
# add the hellodjango project path into the sys.path
sys.path.append('C:/Dev/avenv/src')

# add the virtualenv site-packages path to the sys.path
sys.path.append('C:/Dev/avenv/Lib/site-packages')
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aw.settings')

application = get_wsgi_application()
