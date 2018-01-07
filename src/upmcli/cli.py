from upmcli.config import *
from upmcli.utils import log_output, file_path_generator, image_name
from upmcli.entrypoints_index import EntrypointsIndex
import os
import click
import docker
import logging
from .package_specification import from_prompt, from_file
from git import Repo, InvalidGitRepositoryError

logging.basicConfig(level=LOGGING_LEVEL)

# @Todo python click has feature that make it possible to create sub commands


def install_package(args):
    # @Todo check if args[0] is a path to a yml file or a package name
    # @Todo check docker path in upm yml and convert it to absolute path
    installing_pkg_path = args[0]
    curr_pkg_spec = from_file(file_path_generator(os.getcwd()))
    logging.debug('current pkg: ' + str(curr_pkg_spec))
    installing_pkg_spec = from_file(file_path_generator(installing_pkg_path))
    logging.debug('installing pkg: ' + str(installing_pkg_spec))
    logging.debug('docker value in installing pkg:' + str(installing_pkg_spec.docker))
    client = docker.api.APIClient(base_url='unix://var/run/docker.sock')
    if installing_pkg_spec.docker:
        try:
            docker_image_name = image_name(curr_pkg_spec.name, installing_pkg_spec.name, curr_pkg_spec.version)
            gen = client.build(path=installing_pkg_path,
                               rm=True,
                               tag=docker_image_name)
            log_output(gen)
            curr_pkg_spec.add_dep(str(installing_pkg_spec.name).lower().replace(' ', '_'))
            logging.debug('package path is :' + installing_pkg_path)
            curr_pkg_spec.save_to_file()
            e_index = EntrypointsIndex.from_file(path=os.path.join(os.getcwd(), MAIN_DIR, ENTRY_INDEX_FILE_NAME))
            # @TODO do sth for entrypoint duplication
            e_index.add_entrypoints(installing_pkg_spec.entrypoints, docker_image_name)
            e_index.save_to_file()
        except Exception as e:
            logging.error('ERROR')
            print(e)


def publish_package(args):
    click.echo("project most be git repo and have public remote, which the branch u wish ")

    try:
        repo = Repo(search_parent_directories=True)

    except InvalidGitRepositoryError:
        logging.error("this is not git repository please init git and with public remote before start publishing")



actions = {
    'init': from_prompt,
    'install': install_package,
    'publish': publish_package,
    'test': from_file
}


@click.command()
@click.argument('action')
@click.argument('args', nargs=-1)
def main(action, args):
    if action in actions.keys():
        actions[action](args)
    else:
        click.echo('Unknown command %s' % action)


if __name__ == '__main__':
    main()
