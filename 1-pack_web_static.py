#!/usr/bin/python3
'''
    fabfile containing the do_pack function
'''
from fabric import operations as fo
from datetime import datetime
import os


def do_pack():
    '''
        packs all files from web_static into a .tgz
    '''
    if os.path.exists('./versions') is False:
        fo.local('sudo mkdir versions')

    now = datetime.now().strftime('%Y%m%d%H%M%S')
    error = fo.local('tar -cvzf versions/web_static_{}.tgz web_static'.format(
        now), capture=True)
    print(error)
    f_size = os.path.getsize("versions/web_static_{}.tgz".format(now))
    print("web_static packed: versions/web_static_{}.tgz -> {}Bytes".format(
        now, f_size))
    return 'versions/web_static_{}.tgz'.format(
        now) if error.failed is False else None
