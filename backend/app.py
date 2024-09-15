# from flask import Flask

# from backend.db.dbHandler import IDBHandler

# app = Flask(__name__)


# @app.route("/")
# def index() -> str:
#     return "Main page"

# @app.route("/interrupts_records")
# def get_interrupts_records():
#     # Wywołanie metody read_record, aby pobrać wszystkie rekordy (None jako argument).
#     records = cls.db_handler.read_all_records()

#     if not records:
#         return "Brak rekordów w bazie danych"

#     # Stworzenie prostego szablonu HTML, aby wyświetlić rekordy
#     html_template = """
#     <h1>Interrupt Records</h1>
#     <table border="1">
#         <tr>
#             <th>ID</th>
#             <th>Data</th>
#         </tr>
#         {% for record in records %}
#         <tr>
#             <td>{{ record }}</td>
#         </tr>
#         {% endfor %}
#     </table>
#     """

#     # Renderowanie szablonu z danymi z bazy
#     return render_template_string(html_template, records=records)


# class App:

#     db_handler: IDBHandler | None = None

#     def __init__(self, ip: str, port: int, db_handler: IDBHandler, debug_mode: bool = True) -> None:
#         self.ip = ip
#         self.port = port
#         self.db_handler = db_handler
#         self.debug_mode = debug_mode

#     def run(self) -> None:
#         self.app.run(host=self.ip, port=self.port, debug=self.debug_mode)


import logging

from flask import Flask, render_template_string
from backend.db.dbHandler import IDBHandler
from backend.db.db import DeterrentInfo


# Zmienna globalna na poziomie modułu
db_handler: IDBHandler = None

logger = logging.getLogger(__name__)


def prepare_data(records: list[DeterrentInfo]) -> list[DeterrentInfo]:
    for record in records:
        record.pop("_id")
    return sorted(records, key=lambda r: r["timestamp"], reverse=True)


class App:
    app = Flask(__name__)

    def __init__(
        self,
        ip: str,
        port: int,
        db_handler_instance: IDBHandler,
        debug_mode: bool = True,
    ) -> None:
        global db_handler
        db_handler = db_handler_instance  # Ustawiamy globalny db_handler
        self.ip = ip
        self.port = port
        self.debug_mode = debug_mode

    def run(self) -> None:
        self.app.run(host=self.ip, port=self.port, debug=self.debug_mode)

    @staticmethod
    @app.route("/")
    def index() -> str:
        return "Page 2"

    @app.route("/interrupts_records")
    def get_interrupts_records():
        global db_handler  # Używamy globalnego db_handler
        # Wywołanie metody read_record, aby pobrać wszystkie rekordy (None jako argument).
        raw_records = db_handler.read_all_records()

        records = prepare_data(raw_records)

        logger.debug(records)

        if not records:
            return "Brak rekordów w bazie danych"

        # Stworzenie prostego szablonu HTML, aby wyświetlić rekordy
        html_template = """
        <h1>Interrupt Records</h1>
        <table border="1">
            <tr>
                <th>ID</th>
                <th>Data</th>
            </tr>
            {% for record in records %}
            <tr>
                <td>{{ record['timestamp'] }}</td>
            </tr>
            {% endfor %}
        </table>
        """

        # Renderowanie szablonu z danymi z bazy
        return render_template_string(html_template, records=records)
