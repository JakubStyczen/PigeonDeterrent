import logging
import sys
import threading

sys.path.append("/home/jaksty/Materials/PigeonDeterrent/")

from app import App
from config import Config
from controller import Controller

logger = logging.getLogger(__name__)


def main() -> None:
    try:
        config = Config()
        config.read_server_variables()
        config.read_mongodb_variables()
        config.read_hardware_variables()
        config.read_algorithm_variables()

        controller = Controller(config)
        controller.start_logic()

        mdb_handler = controller.get_db_handler()

        app = App(config.host, config.port, mdb_handler, False)
        app.run()
    except Exception as e:
        logger.error(e)
    finally:
        # controller.stop_and_cleanup()
        pass


if __name__ == "__main__":
    main()
