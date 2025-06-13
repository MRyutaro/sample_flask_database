from datetime import UTC, datetime

from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(
    app, version="1.0", title="Task API", description="タスク管理のためのRESTful API"
)

ns = api.namespace("tasks", description="タスク操作")

task_model = ns.model(
    "Task",
    {
        "id": fields.Integer(readonly=True, description="タスクの一意識別子"),
        "name": fields.String(required=True, description="タスク名"),
        "description": fields.String(description="タスクの説明"),
        "created_at": fields.DateTime(readonly=True, description="作成日時"),
        "updated_at": fields.DateTime(readonly=True, description="更新日時"),
    },
)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


@ns.route("")
class TaskList(Resource):
    @ns.doc("list_tasks")
    @ns.marshal_list_with(task_model)
    def get(self):
        """すべてのタスクを取得"""
        return Task.query.all()

    @ns.doc("create_task")
    @ns.expect(task_model)
    @ns.marshal_with(task_model, code=201)
    def post(self):
        """新しいタスクを作成"""
        data = api.payload
        new_task = Task(name=data["name"], description=data.get("description", ""))
        db.session.add(new_task)
        db.session.commit()
        return new_task, 201


@ns.route("/<int:task_id>")
@ns.param("task_id", "タスクのID")
@ns.response(404, "タスクが見つかりません")
class TaskResource(Resource):
    @ns.doc("get_task")
    @ns.marshal_with(task_model)
    def get(self, task_id):
        """IDでタスクを取得"""
        return Task.query.get_or_404(task_id)

    @ns.doc("update_task")
    @ns.expect(task_model)
    @ns.marshal_with(task_model)
    def put(self, task_id):
        """タスクを更新"""
        task = Task.query.get_or_404(task_id)
        data = api.payload
        task.name = data.get("name", task.name)
        task.description = data.get("description", task.description)
        db.session.commit()
        return task

    @ns.doc("delete_task")
    @ns.response(204, "タスクが削除されました")
    def delete(self, task_id):
        """タスクを削除"""
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return "", 204


if __name__ == "__main__":
    app.run(debug=True)
