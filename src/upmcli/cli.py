import click
import logging
from .package_specification import from_prompt, install_package, publish_package

logging.basicConfig(level=logging.INFO)


@click.group()
@click.option('--debug', default=False)
def main(debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)


@main.command()
def init():
    from_prompt()


@main.command()
@click.argument('path')
def install(path):
    install_package(path)


@main.command()
def publish():
    publish_package()


if __name__ == '__main__':
    main()
