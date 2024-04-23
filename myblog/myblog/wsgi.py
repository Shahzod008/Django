"""
WSGI config for myblog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')

application = get_wsgi_application()





# import os
# import sys

# from django.core.wsgi import get_wsgi_application

# path = os.path.expanduser('~/myproject')
# if path not in sys.path:
#     sys.path.append(path)

# os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
