from yaml.loader import Loader
from yaml import load as yaml_loads
from json import loads as json_loads


class Config:
    """
    Config class that reads the config file and returns the values username and password

    :param file_name: The config file
    """

    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.config = self.read_config()

    def keys(self):
        """
        Returns the keys of the config file

        :return: The keys of the config file
        """
        return self.config.keys()

    def valid_is_json(self):
        """
        Checks if the config file is a json file

        :return: True if the config file is a json file
        """
        return self.file_name.endswith('.json')

    def valid_is_yaml(self):
        """
        Checks if the config file is a yaml file

        :return: True if the config file is a yaml file
        """
        return self.file_name.endswith('.yml')

    def read_config(self) -> dict:
        """
        Reads the config file and returns the values username and password

        :return: The config file
        """

        if self.valid_is_json():
            with open(self.file_name, 'r') as file:
                return json_loads(file.read())
        elif self.valid_is_yaml():
            with open(self.file_name, 'r') as file:
                return yaml_loads(file.read(), Loader=Loader)
        else:
            raise Exception('Invalid config file')

    def __getitem__(self, item):
        return self.config[item]
