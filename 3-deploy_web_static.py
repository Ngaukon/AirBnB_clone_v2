#!/usr/bin/python3
"""
Fabric script based on the files named as 2-do_deploy_web_static.py that creates and
distributes an archive to the 2 web servers

execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric import Connection, task
from datetime import datetime
from os.path import exists, isdir
import os

env_hosts = ['ubuntu@54.209.5.90', 'ubuntu@100.25.135.76']

def do_pack():
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            os.makedirs("versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        os.system("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None

def do_deploy(connection, archive_path):
    """distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        file_n = os.path.basename(archive_path)
        no_ext = os.path.splitext(file_n)[0]
        path = "/data/web_static/releases/"
        connection.put(archive_path, '/tmp/')
        connection.run('mkdir -p {}{}/'.format(path, no_ext))
        connection.run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        connection.run('rm /tmp/{}'.format(file_n))
        connection.run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        connection.run('rm -rf {}{}/web_static'.format(path, no_ext))
        connection.run('rm -rf /data/web_static/current')
        connection.run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False

@task
def deploy(c):
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False

    all_successful = True
    for host in env_hosts:
        conn = Connection(host, connect_kwargs={"key_filename": "~/.ssh/id_rsa"})
        if not do_deploy(conn, archive_path):
            all_successful = False
            break
    return all_successful

