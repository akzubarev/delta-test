#    ___   _____________
#   / _ | / __/ ___/  _/
#  / __ |_\ \/ (_ // /
# /_/ |_/___/\___/___/

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
