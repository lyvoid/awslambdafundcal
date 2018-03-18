# -*-coding:utf-8-*-
import os
from datetime import datetime

from fabric.api import *

env.user = 'ly'
# env.sudo_user = 'root'
env.hosts = ['172.96.248.100:28198']


_TAR_FILE = 'lambda.tar.gz'


def build():
    includes = ['requirements.txt', 'update.sh', '*.py']
    excludes = ['venv', '*.zip', 'fabfile.py', 'local', 'dist', 'test']
    local('rm -f dist/%s' % _TAR_FILE)
    # with lcd(os.path.join(os.path.abspath('.'), )):
    cmd = ['tar', '--dereference', '-czvf', 'dist/%s' % _TAR_FILE]
    cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
    cmd.extend(includes)
    print(' '.join(cmd))
    local(' '.join(cmd))


_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_TMP_DIR = '/tmp/mylambda'


def deploy():
    sudo('rm -f %s' % _REMOTE_TMP_TAR)
    # delete current tmp dir
    sudo('rm -rf %s' % _REMOTE_TMP_DIR)
    # create new dir
    sudo('mkdir %s' % _REMOTE_TMP_DIR)
    # upload new tar file
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    # unpack to new dir
    with cd(_REMOTE_TMP_DIR):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
        # update new lambda function source
        sudo('chmod +x %s/update.sh' % _REMOTE_TMP_DIR)
        sudo('./update.sh')

    # 重置软链接:
    # with cd(_REMOTE_BASE_DIR):
    #     sudo('rm -f www')
    #     sudo('ln -s %s www' % newdir)
    #     sudo('chown www-data:www-data www')
    #     sudo('chown -R www-data:www-data %s' % newdir)
    # 重启Python服务和nginx服务器:
    # with settings(warn_only=True):
    #     sudo('supervisorctl stop awesome')
    #     sudo('supervisorctl start awesome')
    #     sudo('/etc/init.d/nginx reload')
