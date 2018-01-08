import os
import logging
import click
import yaml
from upmcli.entrypoints_index import EntrypointsIndex
from upmcli.config import *

class PackageSpecification:
    def __init__(self, yml_path, name, author, version, description, entrypoints, docker=None, dependencies=None):
        self.yml_path = yml_path
        if dependencies is None:
            dependencies = []
        self.name = name
        self.author = author
        self.description = description
        self.version = version
        self.docker = docker
        self.entrypoints = entrypoints
        self.dependencies = dependencies

    def __repr__(self):
        return "%s(name=%r, author=%r, description=%r, version=%r)" % \
               (self.__class__.__name__, self.name, self.author, self.description, self.version)

    def to_dict(self):
        result = {'name': self.name, 'author': self.author, 'description': self.description,
                  'version': self.version, 'entrypoints': self.entrypoints}
        if self.docker is not None:
            result['docker'] = self.docker
        if len(self.dependencies):
            result['dependencies'] = self.dependencies
        return result

    def add_dep(self, dep):
        self.dependencies.append(dep)

    def save_to_file(self, path=None):
        # logging.debug('save to file path is' + path)
        with open(path if path is not None else self.yml_path, 'w') as file:
            yaml.dump(self.to_dict(), file, default_flow_style=False)
            file.close()

    def get_yml_file(self):
        return self.yml_path


def from_prompt(args):
    logging.info('loading yml')
    cwd = os.getcwd()
    logging.info(cwd)
    from upmcli.utils import package_exists, file_path_generator
    if package_exists(cwd):
        print("project already initialized")
    else:
        logging.debug('start to get input')
        name = click.prompt('Please enter project name', type=str)
        logging.debug('name selected')
        author = click.prompt('Please enter project author', type=str)
        logging.debug('author selected')
        description = click.prompt('Please enter project description', type=str)
        version = click.prompt('Please enter project version', default='0.0.1', type=str)
        has_dockerfile = click.prompt('do u have a docker file?', default=False, type=bool)
        docker = None
        if has_dockerfile:
            docker = click.prompt('Please enter Dockerfile path', default='./Dockerfile', type=str)
        entrypoints_flag = True
        entrypoints = {}
        while entrypoints_flag:
            key = click.prompt('Please enter entrypoint name', default='run', type=str)
            value = click.prompt('please enter command', default='npm start', type=str)
            entrypoints[key] = value
            entrypoints_flag = click.prompt('more entrypoint?', default=False, type=bool)
        file_path = file_path_generator(cwd)
        package = PackageSpecification(file_path, name, author, version, description, entrypoints, docker)
        logging.debug(package)
        logging.debug(package.to_dict())
        with open(file_path, 'w') as file:
            yaml.dump(package.to_dict(), file, default_flow_style=False)
            file.close()

        os.mkdir('.upm')
        i_entrypoints = {}
        for key, value in package.entrypoints.items():
            i_entrypoints[key] = {'cmd': value}
        e_index = EntrypointsIndex(
            path=os.path.join(os.getcwd(), MAIN_DIR, ENTRY_INDEX_FILE_NAME), entrypoints=i_entrypoints)
        e_index.save_to_file()

        print("project initialized")
        return package


def from_file(file_path):
    from upmcli.utils import package_exists
    if not package_exists(file_path):
        logging.error("package specification not found")
        return
    from upmcli.utils import load_yml
    yml_obj = load_yml(file_path)
    return PackageSpecification(yml_path=file_path, **yml_obj)
