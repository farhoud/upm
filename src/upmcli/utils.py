import os

import pwd
import tempfile
from git import Repo
import yaml
import docker
import json
import logging
import shutil

from upmcli.config import SPEC_FILE_NAME, MAIN_DIR, ENTRY_INDEX_FILE_NAME, NETWORK_DETAILS_FILE_NAME

cwd = os.getcwd()


def file_path_generator(path):
    if os.path.isdir(path):
        file_path = os.path.join(os.path.abspath(path), SPEC_FILE_NAME)
        return file_path
    return path


def entrypoint_path_generator(path):
    if os.path.isdir(path):
        file_path = os.path.join(os.path.abspath(path), MAIN_DIR, ENTRY_INDEX_FILE_NAME)
        return file_path
    return path


def network_path_generator(path):
    if os.path.isdir(path):
        file_path = os.path.join(os.path.abspath(path), MAIN_DIR, NETWORK_DETAILS_FILE_NAME)
        return file_path
    return path


def package_exists(directory_path):
    file_path = file_path_generator(directory_path)
    return os.path.exists(file_path)


def load_yml(path):
    file_path = file_path_generator(path)
    with open(file_path, 'r') as file:
        yml_object = yaml.load(file)
        file.close()
    return yml_object


def log_output(generator):
    while True:
        try:
            output = generator.__next__()
            output = output.decode()
            json_output = json.loads(output)
            if 'stream' in json_output:
                logging.info(json_output['stream'])
        except StopIteration:
            logging.info("Docker image build complete.")
            break
        except ValueError:
            logging.error("Error")


def image_name(project_name, package_name, package_version):
    return '%s-%s:%s' % (str(project_name).lower().replace(' ', '_'),
                         str(package_name).lower().replace(' ', '_'),
                         str(package_version))


def network_name(project_name):
    return '%s-network' % str(project_name).lower().replace(' ', '_')


def get_docker_hi_client():
    return docker.DockerClient(base_url='unix://var/run/docker.sock')


def create_network(project_name):
    client = get_docker_hi_client()
    network = client.networks.create(network_name(project_name), driver="bridge")
    logging.info('network created  ... name: %s, id: %s' % (network.name, network.id))
    return network


def port_mapper(str):
    mapped_ports = {}
    removed_space_str = str.replace(" ", "")
    port_list = removed_space_str.split(',')
    for port_map in port_list:
        if ":" in port_map:
            ports = port_map.split(":")
            mapped_ports[int(ports[0])] = int(port_map[1])
        else:
            mapped_ports[int(port_map)] = int(port_map)
    return mapped_ports


def check_network(name=None):
    client = get_docker_hi_client()
    project_network = network_name(name)
    if name:
        network_list = client.networks.list(names=[project_network])
    else:
        network_list = client.networks.list()

    for network in network_list:
        if project_network == network.name:
            logging.info('Network Already exist.')
            return network
        logging.info('network not exists')
        return False


def get_user_id():
    logging.debug(pwd.getpwuid(os.getuid()).pw_name)
    return pwd.getpwuid(os.getuid()).pw_uid


# def fetch_package(path):
#     dirpath = tempfile.mkdtemp()
#     shutil.copy2(path, dirpath)


def my_unicode_repr(self, data):
    return self.represent_str(data.encode('utf-8'))
