# coding=utf-8
from enum import Enum, auto


class DataType(Enum):
    """The object to indicate the type of data in ModuleData"""

    INIT = auto()
    REDIRECT = auto()
    HELP = auto()
    ALIAS = auto()
    CLOCK = auto()

    POSTBACK = auto()
    MESSAGE_TEXT = auto()
    MESSAGE_IMAGE = auto()
    MESSAGE_VIDEO = auto()
    MESSAGE_AUDIO = auto()
    MESSAGE_LOCATION = auto()
    MESSAGE_STICKER = auto()
    MESSAGE_FILE = auto()

    REPLY = auto()
    PUSH_USER = auto()
    PUSH_GROUP = auto()
    PUSH_ROOM = auto()


class DataPriority(int):
    """The object to indicate the priority of data for ModuleData"""
    SYSTEM = 0
    MODULE = 1
    MESSAGE = 2


class ModuleData(object):
    """The genaral object used for transfer data between modules."""

    def __init__(self,
                 data=None,
                 data_type=DataType.MESSAGE_TEXT,
                 redirect_module: str = None,
                 module_tag: int = None,
                 module_name: str = None):
        """The initialization of the object, nothing else to say OωO.

        Arguments:
        data -- Data to transfer (default None)

        data_type -- The type of data (default DataType.MESSAGE_TEXT)
            See DataType for all available argments.

        redirect_module -- The module name that data redirect to (default None)
            Used only when data_type is REDIRECT.

        module_tag -- The tag of the module sent from (default None)
            Used only when data_type is INIT.

        module_name -- The name of the module sent from (default None)
            Used only when data_type is INIT.
        """

        self.data_type = data_type
        self.data = data
        self.tag = module_tag
        self.name = module_name
        self.redirect = redirect_module

    # def __str__(self):
    #     return self.tag

    def __lt__(self, other):
        """Just a workaround, might fix someday OωO"""
        return True
