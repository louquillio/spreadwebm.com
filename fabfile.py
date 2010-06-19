from __future__ import with_statement
from fabric.api import *
import os, glob, socket
import fabric.contrib.project as project

PROD = 'spreadwebm.org'
PROD_PATH = 'domains/spreadwebm.com/web/public/'
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DEPLOY_PATH = os.path.join(ROOT_PATH, 'deploy')

def clean():
    local('rm -rf ./deploy/*')

def regen():
    clean()
    local('hyde.py -g -s .')

def pushcss():
    """
    For pushing CSS-only changes to the local docroot during testing.
    """
    local('cp -r media/css/* deploy/media/css/')

def serve():
    ## Kill any heel process
    local('heel --kill')
    ## Start webserver on local hostname
    #local('heel --daemonize --address ' + socket.gethostbyaddr(socket.gethostname())[0] + ' --root ./deploy')
    ## Start webserver on development hostname
    local('heel --daemonize --address localhost --root ./deploy')

def reserve():
    regen()
    local('heel --kill')
    serve()

@hosts(PROD)
def publish():
    regen()
    project.rsync_project(
        remote_dir=PROD_PATH,
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True
    )
