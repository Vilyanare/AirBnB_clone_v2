#!/usr/bin/python3
'''
    fabfile containing the do_pack and do_deploy functions
'''
from fabric import operations as fo
from datetime import datetime
from fabric.api import env
from fabric.decorators import runs_once
import os

env.user = "ubuntu"
env.hosts = '107.22.148.78', '54.204.244.213'

@runs_once
def do_pack():
    '''
        packs all files from web_static into a .tgz
    '''
    if os.path.exists('./versions') is False:
        fo.local('sudo mkdir versions')

    now = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = 'versions/web_static_{}.tgz'.format(now)
    print("Packing web_static to {}".format(file_name))
    tar_out = fo.local('tar -cvzf {} web_static'.format(
        file_name), capture=True)
    print(tar_out)
    f_size = os.path.getsize("{}".format(file_name))
    print("web_static packed: {} -> {}Bytes".format(file_name, f_size))
    return '{}'.format(file_name) if tar_out.failed is False else None


def do_deploy(archive_path):
    '''
        deploys static web packages to servers listed in decorator
    '''
    if os.path.isfile(archive_path):
        arch_name = archive_path.split('/')[-1]
        fo.put(archive_path, "/tmp/{}".format(arch_name))
        file_name = '/data/web_static/releases/' + arch_name.split(".")[0]
        fo.run("mkdir -p {}".format(file_name))
        fo.run("tar -xzf /tmp/{} -C {}/".format(arch_name, file_name))
        fo.run("rm -rf /tmp/{}".format(arch_name))
        fo.run("mv {}/web_static/* {}/".format(file_name, file_name))
        fo.run("rm -rf {}/web_static".format(file_name))
        fo.run("rm -rf /data/web_static/current")
        fo.run("ln -s {}/ /data/web_static/current".format(file_name))
        print("New version deployed!")
        return True

    return False


def deploy():
    '''
        runs do_pack then passes arguments to, and runs, do_deploy
    '''
    archive = do_pack()

    if archive is None:
        return False

    return do_deploy(archive)
