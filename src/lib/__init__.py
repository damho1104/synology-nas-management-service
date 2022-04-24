from .utils.file import *
from .utils.singleton import *
from .utils import log
from .config.loader import *
from .server import *
from .server.service.synology import SynologyManager
from .core import run

configuration: ConfigLoader = ConfigLoader()
syno_manager: SynologyManager = SynologyManager()
