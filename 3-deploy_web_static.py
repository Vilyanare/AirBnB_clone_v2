#!/usr/bin/python3
'''
    fabfile containing the do_pack and do_deploy functions
'''
from fabric import operations as fo
from datetime import datetime
from fabric.api import env, hide
from fabric.decorators import runs_once
import os

env.user = "ubuntu"
env.key_filename = "~/.ssh/holberton"
env.hosts = '107.22.148.78', '54.204.244.213'


@runs_once
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
    with hide('output'):
        arch_name = archive_path.split('/')[-1]
        put_out = fo.put(archive_path, "/tmp/{}".format(arch_name))
        file_name = arch_name.split(".")[0]
        fo.run("rm -rf /data/web_static/releases/{}/".format(file_name))
        mkdir_out = fo.run("mkdir -p /data/web_static/releases/{}".format(
            file_name))
        tar_out = fo.run(
            "tar zxvf /tmp/{} -C /data/web_static/releases/{}/".format(
                arch_name, file_name))
        rm_out2 = fo.run("rm -rf /tmp/{}".format(arch_name))
        s = ("mv /data/web_static/releases/{}/web_static/*"
             " /data/web_static/releases/{}/".format(
                 file_name, file_name))
        mv_out = fo.run(s)
        rm_out = fo.run(
            "rm -rf /data/web_static/releases/{}/web_static".format(
                file_name))
        rm_out3 = fo.run("rm -rf /data/web_static/current")
        ln_out = fo.sudo(
            "ln -sf /data/web_static/releases/{}/ /data/web_static/current"
            .format(file_name))
        errors = [put_out.failed, mkdir_out.failed,
                  tar_out.failed, rm_out.failed, rm_out2.failed,
                  ln_out.failed, mv_out.failed, rm_out3.failed]
    if not any(errors):
        print("New version deployed!")
        return True
    return False


def deploy():
    '''
        runs do_pack and then passes arguments to and runs do_deploy
    '''
    archive = do_pack()

    if archive is None:
        return False

    return do_deploy(archive)
