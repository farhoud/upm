import click
import os
import yaml

from upmcli.project import Project

FILE_NAME = "upm.yml"
cwd = os.getcwd()

ascii_snek = """\
    --..,_                     _,.--.
       `'.'.                .'`__ o  `;__.
          '.'.            .'.'`  '---'`  `
            '.`'--....--'`.'
              `'--....--'`
"""


@click.command()
@click.argument('action')
def main(action):
    if action == "init":
        init_project()


if __name__ == '__main__':
    main()


def file_path_generator(path):
    file = path + "/" + FILE_NAME
    return file


def is_exist(path):
    file = file_path_generator(path)
    print(file)
    return os.path.exists(file)


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

