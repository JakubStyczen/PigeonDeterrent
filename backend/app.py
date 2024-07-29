from flask import Flask

class App():
    APP = Flask(__name__)
    def __init__(self, ip: str, port: int, debug_mode: bool = True) -> None:

        self.ip = ip
        self.port = port
        self.debug_mode = debug_mode
        
    def run(self) -> None:
        self._set_views()
        self.APP.run(host=self.ip, port=self.port, debug=self.debug_mode)
        
    def _set_views(self) -> None:
        self.APP.add_url_rule("/", view_func=lambda: "Working?")
        
    @staticmethod
    @APP.route('/home/')
    def index() -> str:
        return "Page 2"