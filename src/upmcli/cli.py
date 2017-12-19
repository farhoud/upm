import click
import os
import yaml
import docker

from .project import Project

FILE_NAME = "upm.yml"
cwd = os.getcwd()

ascii_snek = """\
    --..,_                     _,.--.
       `'.'.                .'`__ o  `;__.
          '.'.            .'.'`  '---'`  `
            '.`'--....--'`.'
              `'--....--'`
"""

def file_path_generator(path):
    file = path + "/" + FILE_NAME
    return file


def is_exist(path):
    file = file_path_generator(path)
    print(file)
    return os.path.exists(file)


def load_yml(path):
    if os.path.isdir(path):
        file_content = open('%s/upm.yml' % path, 'r')
    else:
        file_content = open(path, 'r')
    yml_object = yaml.load(file_content)
    return yml_object


def init_project():
    if is_exist(cwd):
        print("project inited before")
    else:
        name = click.prompt('Please enter project name', type=str)
        author = click.prompt('Please enter project author', type=str)
        description = click.prompt('Please enter project description', type=str)
        version = click.prompt('Please enter project version', default='0.0.1', type=str)
        docker = click.prompt('Please enter Dockerfile path', default='./Dockerfile', type=str)
        tmp = click.prompt('Please network endpoints (comma separated)', default='80,443', type=str)
        endpoints = [x.strip() for x in tmp.split(',')]
        project = Project(name, author, version, description, docker, endpoints)
        path = file_path_generator(cwd)
        with open(path, 'w') as file:
            yaml.dump(project.to_dict(), file, default_flow_style=False)
            file.close()
        print("project inited")


def install_package(args):
    # @Todo check if args[0] is a path to a yml file or a package name
    package_path = args[0]
    package_yml = load_yml(package_path)
    client = docker.from_env()
    if 'dockerfile' in package_yml.keys():
        image = client.images.build(fileobj=open(package_yml['dockerfile'], 'rb'), quiet=False)
        # client.containers.run(image, command=package_yml['entrypoints']['node'])


actions = {
    'init': init_project,
    'install': install_package
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


