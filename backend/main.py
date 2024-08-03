import logging

from app import App
from config import Config

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    config = Config()
    config.read_server_variables()

    app = App(config.host, config.port, config.debug)
    app.run()
