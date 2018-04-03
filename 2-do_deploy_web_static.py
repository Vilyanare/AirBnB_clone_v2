#!/usr/bin/python3
'''
    fabfile containing the do_pack and do_deploy functions
'''
from fabric import operations as fo
from datetime import datetime
from fabric.api import env
import os

env.user = "ubuntu"
env.key_filename = "~/.ssh/holberton"
env.hosts = '107.22.148.78', '54.204.244.213'


def do_pack():
    '''
        packs all files from web_static into a .tgz
    '''
    if os.path.exists('./versions') is False:
        fo.local('sudo mkdir versions')

    now = datetime.now().strftime('%Y%m%d%H%M%S')
    print("Packing web_static to versions/web_static_{}.tgz".format(now))
    tar_out = fo.local(
        'tar -cvzf versions/web_static_{}.tgz web_static'.format(
            now), capture=True)
    print(tar_out)
    f_size = os.path.getsize("versions/web_static_{}.tgz".format(now))
    print("web_static packed: versions/web_static_{}.tgz -> {}Bytes".format(
        now, f_size))
    return 'versions/web_static_{}.tgz'.format(
        now) if tar_out.failed is False else None


def do_deploy(archive_path):
    '''
        deploys static web packages to servers listed in decorator
    '''
    if os.path.isfile(archive_path) is False:
        return False

    arch_name = archive_path.split('/')[-1]
    fo.put(archive_path, "/tmp/{}".format(arch_name))
    file_name = arch_name.split(".")[0]
    fo.run("mkdir -p /data/web_static/releases/{}".format(
        file_name))
    fo.run(
        "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            arch_name, file_name))
    fo.run("rm -rf /tmp/{}".format(arch_name))
    s = ("mv /data/web_static/releases/{}/web_static/*"
         " /data/web_static/releases/{}/".format(
             file_name, file_name))
    fo.run(s)
    fo.run(
        "rm -rf /data/web_static/releases/{}/web_static".format(
            file_name))
    fo.run("rm -rf /data/web_static/current")
    fo.run(
        "ln -s /data/web_static/releases/{}/ /data/web_static/current"
        .format(file_name))
    print("New version deployed!")
    return True
