from pathlib import Path

from flask import Flask, jsonify, render_template, request

from database import create_item, delete_item, init_db, list_items, update_item


DEFAULT_DB = Path(__file__).with_name("lab6.db")


def create_app(db_path: str | Path = DEFAULT_DB) -> Flask:
    """Повышенное №1 — Flask + SQLite CRUD."""
    app = Flask(__name__)
    app.config["DB_PATH"] = str(db_path)

    init_db(app.config["DB_PATH"])

    @app.get("/")
    def index():
        return {
            "laboratory": 6,
            "variant": 8,
            "message": "Flask + SQLite CRUD",
        }

    @app.get("/table")
    def table():
        """Среднее №4 — страница с таблицей данных."""
        items = list_items(app.config["DB_PATH"])
        return render_template("table.html", items=items)

    @app.get("/api/items")
    def api_list_items():
        return jsonify(list_items(app.config["DB_PATH"]))

    @app.post("/api/items")
    def api_create_item():
        data = request.get_json(silent=True) or {}
        name = str(data.get("name", "")).strip()

        try:
            quantity = int(data.get("quantity", 0))
        except (TypeError, ValueError):
            return {"error": "quantity должен быть целым числом"}, 400

        if not name:
            return {"error": "Поле name обязательно"}, 400

        item = create_item(app.config["DB_PATH"], name, quantity)
        return jsonify(item), 201

    @app.put("/api/items/<int:item_id>")
    def api_update_item(item_id: int):
        data = request.get_json(silent=True) or {}
        name = str(data.get("name", "")).strip()

        try:
            quantity = int(data.get("quantity", 0))
        except (TypeError, ValueError):
            return {"error": "quantity должен быть целым числом"}, 400

        if not name:
            return {"error": "Поле name обязательно"}, 400

        item = update_item(
            app.config["DB_PATH"],
            item_id,
            name,
            quantity,
        )

        if item is None:
            return {"error": "Запись не найдена"}, 404

        return jsonify(item)

    @app.delete("/api/items/<int:item_id>")
    def api_delete_item(item_id: int):
        if not delete_item(app.config["DB_PATH"], item_id):
            return {"error": "Запись не найдена"}, 404

        return {"message": "Запись удалена"}

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
