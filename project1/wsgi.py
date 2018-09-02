import os
import sys
from os.path import join,dirname,abspath
from django.core.wsgi import get_wsgi_application

PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0,PROJECT_DIR)
sys.path.append('/home/mysite_env/lib/python3.6/site-packages')
os.environ["DJANGO_SETTINGS_MODULE"] = "project1.settings"

application = get_wsgi_application()

