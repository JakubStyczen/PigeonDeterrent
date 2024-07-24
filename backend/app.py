from flask import Flask

class App():
    def __init__(self, ip: str, port: int, debug_mode: bool = True) -> None:
        self.app = Flask(__name__)
        self.ip = ip
        self.port = port
        self.debug_mode = debug_mode
        
    def run(self) -> None:
        self.app.run(host=self.ip, port=self.port, debug=self.debug_mode)