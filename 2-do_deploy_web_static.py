#!/usr/bin/python3
'''
    fabfile containing the do_pack and do_deploy functions
'''
from fabric import operations as fo
from fabric.api import env
import os

env.user = 'ubuntu'
env.hosts = '107.22.148.78', '54.204.244.213'


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
