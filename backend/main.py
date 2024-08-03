import logging

from app import App
from config import Config

HOST_IP: str = "192.168.1.60"
PORT: int = 5000
DEBUG: bool = True

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    config = Config()
    config.read_server_variables()

    app = App(config.host, config.port, config.debug)
    app.run()
