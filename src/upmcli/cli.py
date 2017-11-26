import click
import os
import yaml

FILE_NAME = "upm.yml"

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
    cwd = os.getcwd()
    if is_exist(cwd):
        print("project inited before")
    else:
        path = file_path_generator(cwd)
        file = open(path, 'w')
        file.write("file created")
        print("project inited")
        file.close()

# def upm_content(name, author, )
