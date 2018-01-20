import click
import docker
import dockerpty
import os
import logging
import random
from upmcli.config import *
from upmcli.entrypoints_index import EntrypointsIndex
from upmcli.package_specification import from_file
from upmcli.utils import entrypoint_path_generator, log_output, check_network, file_path_generator, create_network, \
    get_user_id


def test_func(args):
    click.echo(args)


def run(cmd, command_args):
    entrypoint, entry_args = get_entrypoint(cmd)
    project_spec = from_file(file_path_generator(os.getcwd()))
    client = docker.api.APIClient(base_url='unix://var/run/docker.sock')
    command = entrypoint['command'] + ' ' + ' '.join(entry_args) + ' '.join(command_args)
    print(command)
    # ports = []
    # if 'ports' in entrypoint:
    #     for key in entrypoint['ports'].keys():
    #         ports.append(key)
    # d_network = check_network(project_spec.name)
    # print(ports)
    # print(entrypoint)
    # if not d_network:
    #     d_network = create_network(project_spec.name)
    # networking_config = client.create_networking_config({
    #     d_network.name: client.create_endpoint_config()
    # })
    container = client.create_container(entrypoint['image'],
                                        command,
                                        name=project_spec.name+"_"+cmd+"_"+str(random.randint(0, 500)),
                                        volumes=['/src'],
                                        # ports=ports,
                                        host_config=client.create_host_config(
                                            binds=[os.getcwd() + ':/src:rw'],
                                            network_mode='host',
                                            # port_bindings=entrypoint['ports'] if 'ports' in entrypoint else None,
                                            publish_all_ports=True),
                                        # user='%s:%s' % (get_user_id(), 0),
                                        # networking_config=networking_config,
                                        stdin_open=True,
                                        tty=True,
                                        working_dir=CONTAINER_VOLUME_MOUNT_PATH)

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
