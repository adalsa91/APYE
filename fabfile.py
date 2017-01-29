import os
import yaml
from fabric.contrib.files import exists
from fabric.api import *

env.key_filename = 'azure.rsa'
env.user = 'apye'
env.hosts = ['apye.cloudapp.net']

with open('vars.yaml', 'r') as f:
    env.vars = yaml.load(f)

project_root = env.vars['root_dir'] + '/' + env.vars['project_name']

def get_repo():

    if exists(project_root + '/' + '.git'):
        run('cd {} && git pull origin master'.format(project_root))
    else:
        run('git clone {} {}'.format(env.vars['project_repo'], project_root))

def deploy():
    sudo('mkdir -p {}'.format(project_root))
    sudo('chown -R {}:{} {}'.format(env.vars['vm_user'], env.vars['vm_user'], project_root))
    with cd(project_root):
        get_repo()
        #with shell_env(APP_SETTINGS=env.vars['APP_SETTINGS'], DATABASE_URL=env.vars['DATABASE_URL'], SECRET_KEY=env.vars['SECRET_KEY']):
        sudo('make install')
        sudo('service gunicorn restart')
