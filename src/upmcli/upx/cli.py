import click
import docker
import dockerpty
import os
from upmcli.config import *
from upmcli.entrypoints_index import EntrypointsIndex
from upmcli.package_specification import from_file
from upmcli.utils import entrypoint_path_generator, log_output, check_network, file_path_generator, create_network, \
    get_user_id


def test_func(args):
    click.echo(args)


def run(cmd, args):
    entrypoint = get_entrypoint(cmd)
    project_spec = from_file(file_path_generator(os.getcwd()))
    client = docker.api.APIClient(base_url='unix://var/run/docker.sock')
    command = entrypoint['cmd'] + ' ' + ' '.join(args)
    host_config = client.create_host_config(group_add=[0])
    container = client.create_container(entrypoint['image'],
                                        command,
                                        volumes=['/src'],
                                        host_config=client.create_host_config(binds=[
                                            os.getcwd() + ':/src:rw']),
                                        # user='%s:%s' % (get_user_id(), 0),
                                        stdin_open=True,
                                        tty=True,)
                                        # working_dir=CONTAINER_VOLUME_MOUNT_PATH)

    d_network = check_network(project_spec.name)
    if not d_network:
        d_network = create_network(project_spec.name)

    client.connect_container_to_network(container['Id'], d_network.id)

    dockerpty.start(client, container)


def get_entrypoint(cmd):
    e_index = EntrypointsIndex.from_file(entrypoint_path_generator(os.getcwd()))
    return e_index.find_entrypoint(cmd)


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('args', nargs=-1)
def main(args):
    run(args[0], args[1:])


if __name__ == '__main__':
    main()
