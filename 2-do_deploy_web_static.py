#!/usr/bin/python3
"""A module for web application deployment with Fabric."""
import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once

env.hosts = ['52.91.116.62', '54.144.199.248']
"""The list of host server IP addresses."""

@runs_once
def do_pack():
    """Archives the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archive_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archive_size))
    except Exception:
        output = None
    return output

def do_deploy(archive_path):
    """Deploys the static files to the host servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        archive_name = archive_path.split("/")[-1]
        archive_folder = archive_name.split(".")[0]
        release_folder = "/data/web_static/releases/{}/".format(archive_folder)
        
        put(archive_path, "/tmp/{}".format(archive_name))

        # Uncompress the archive to the folder
        run("mkdir -p {}".format(release_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, release_folder))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_name))

        # Move files out of the web_static folder
        run("mv {0}web_static/* {0}".format(release_folder))
        run("rm -rf {}web_static".format(release_folder))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(release_folder))

        print("New version deployed!")
        return True
    except Exception:
        return False

