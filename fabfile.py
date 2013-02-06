from fabric.api import env, task, get
from fabric.contrib import django

import sys
import os.path
sys.path.insert(0, os.path.dirname(env.real_fabfile))

django.project('pycon')
from django.conf import settings

env.use_ssh_config = True
env.hosts = [ 'pycon.it' ]

@task
def sync_db():
    remote_path = '/srv/europython/data/site/p3.db'
    local_path = settings.DATABASES['default']['NAME']
    get(remote_path, local_path)

def parent_(path):
    if path[-1] == '/':
        path = path[:-1]
    return os.path.dirname(path)

@task
def sync_media():
    remote_path = '/srv/europython/data/media_public'
    local_path = parent_(settings.MEDIA_ROOT)
    get(remote_path, local_path)
