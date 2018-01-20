import logging
import yaml


class EntrypointsIndex:
    def __init__(self, path=None, entrypoints=None):
        self.entrypoints = {} if entrypoints is None else entrypoints
        # self.add_entrypoints(entrypoints if entrypoints is not None else {}, None)
        self.path = path

    @staticmethod
    def from_file(path):
        from upmcli.utils import package_exists
        if not package_exists(path):
            logging.error("entrypoints index not found")
            return
        from upmcli.utils import load_yml
        yml_obj = load_yml(path)
        return EntrypointsIndex(path=path, entrypoints=yml_obj['entrypoints'])

    def add_entrypoints(self, entrypoints, image_name):
        # @TODO check for duplications
        for key, value in entrypoints.items():
            self.entrypoints[key] = value
            if image_name is not None:
                self.entrypoints[key]['image'] = image_name

    def save_to_file(self, path=None):
        with open(path if path is not None else self.path, 'w') as file:
            entrypoints = {'entrypoints': self.entrypoints}
            yaml.dump(entrypoints, file, default_flow_style=False)

    def find_entrypoint(self, cmd, ports=None, args=[]):
        entrypoint = self.entrypoints[cmd].copy()
        if ports:
            if 'ports' in entrypoint:
                entrypoint['ports'] = {**ports, **entrypoint['ports']}
            else:
                entrypoint['ports'] = ports
        print(self.entrypoints)
        if 'image' in entrypoint:
            return entrypoint, args
        i_cmd = entrypoint['command'].split(' ')[0]
        args = args + entrypoint['command'].split(' ')[1:]
        return self.find_entrypoint(i_cmd, entrypoint['ports'], args)

