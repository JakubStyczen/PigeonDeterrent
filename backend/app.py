import logging
import os

from flask import Flask, Response, render_template_string, render_template, request
from flask_restful import Resource, Api
from backend.db.dbHandler import IDBHandler
from backend.db.db import DeterrentInfo

# Create paths for custom user location of frontend resources
template_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../frontend/templates")
)
static_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../frontend/static")
)

db_handler: IDBHandler = None

logger = logging.getLogger(__name__)


class Index(Resource):
    def get(self):
        return Response(render_template("index.html", content="Main page"))


class TestTemplate(Resource):
    def get(self):
        content = """
                    <h2>About this Page</h2>
                    <p>This page is created using <strong>Flask</strong> and <em>Jinja2</em>.</p>
                    """
        return Response(render_template("index.html", content=content))


class InterruptsRecords(Resource):
    def __init__(self, *args, **kwargs):
        self.db_handler = kwargs["db_handler"]

    def prepare_data(self, records: list[DeterrentInfo]) -> list[DeterrentInfo]:
        for record in records:
            record.pop("_id")
            record["Time"] = record["Time"].strftime("%Y-%m-%d %H:%M:%S")
        return sorted(records, key=lambda r: r["Time"], reverse=True)

    def get(self):
        raw_records = self.db_handler.read_all_records()
        records = self.prepare_data(raw_records)

        if not records:
            return {"Error": "Empty database"}, 500

        limit: int = request.args.get("limit", default=5, type=int)
        records = records[:limit]

        first_record_data = records[0]
        first_record_data.pop("id", None)
        dynamic_fields = first_record_data.keys()

        html_template = """
        <div class="interrupt-container">
            <h1 class="left-header">Pigeons interrupt records</h1>
            
            <div class="description">
                <p>This page displays the list of interrupt records from the database. You can view the timestamp and other relevant details for each record.</p>
            </div>
            
            <div class="table-wrapper">
                <table class="interrupt-table">
                    <tr>
                        {% for field in dynamic_fields %}
                            <th>{{ field }}</th>
                        {% endfor %}
                    </tr>
                    {% for record in records %}
                    <tr>
                        {% for field in dynamic_fields %}
                            <td>{{ record[field] }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </table>
            </div>
        </div>
        """

        content = render_template_string(
            html_template, records=records, dynamic_fields=dynamic_fields
        )
        return Response(render_template("index.html", content=content))


class App:
    def __init__(
        self,
        ip: str,
        port: int,
        db_handler_instance: IDBHandler,
        debug_mode: bool = True,
    ) -> None:
        self.app = Flask(
            __name__, template_folder=template_dir, static_folder=static_dir
        )
        self.api = Api(self.app)
        self.db_handler = db_handler_instance
        self.ip = ip
        self.port = port
        self.debug_mode = debug_mode

    def run(self) -> None:
        self.api.add_resource(Index, "/")
        self.api.add_resource(TestTemplate, "/template")
        self.api.add_resource(
            InterruptsRecords,
            "/pigeons_interrupt_records",
            resource_class_kwargs={"db_handler": self.db_handler},
        )
        self.app.run(host=self.ip, port=self.port, debug=self.debug_mode)
