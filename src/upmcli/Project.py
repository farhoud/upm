import yaml


class Project:
    def __init__(self, name, author, version, description, docker, endpoints, services=[]):
        self.name = name
        self.author = author
        self.description = description
        self.version = version
        self.docker = docker
        self.endpoints = endpoints
        self.services = services

    def __repr__(self):
        return "%s(name=%r, author=%r, description=%r, version=%r)" % \
               (self.__class__.__name__, self.name, self.author, self.description, self.version)

    def to_dict(self):
        return {'name': self.name, 'author': self.author, 'description': self.description,
                'version': self.version, 'endpoints': self.endpoints, 'services': self.services}
