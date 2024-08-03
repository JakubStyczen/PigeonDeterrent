from flask import Flask


class App:
    app = Flask(__name__)

    def __init__(self, ip: str, port: int, debug_mode: bool = True) -> None:

        self.ip = ip
        self.port = port
        self.debug_mode = debug_mode

    def run(self) -> None:
        # self._set_views()
        self.app.run(host=self.ip, port=self.port, debug=self.debug_mode)

    @staticmethod
    @app.route("/")
    def index() -> str:
        return "Page 2"
