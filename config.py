from configparser import ConfigParser


class SingletonMeta(type):
    """
    The Singleton class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    """
    The Config class.
    """

    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')

    def get_coords(self, name) -> str:
        return self.config["COORDINATES"][name]
