from app import App

HOST_IP: str = "192.168.1.60"
PORT: int = 5000
DEBUG: bool = True


if __name__ == "__main__":
    app = App(HOST_IP, PORT, DEBUG)
    app.run()