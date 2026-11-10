import importlib.util
import tempfile
import unittest
from pathlib import Path

FLASK_AVAILABLE = importlib.util.find_spec("flask") is not None

if FLASK_AVAILABLE:
    from flask_app import create_app


@unittest.skipUnless(FLASK_AVAILABLE, "Для теста Flask установите requirements.txt")
class TestFlaskApp(unittest.TestCase):
    def test_crud_api_and_table(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "test.db"
            app = create_app(db_path)
            app.config["TESTING"] = True

            with app.test_client() as client:
                response = client.post(
                    "/api/items",
                    json={"name": "Книга", "quantity": 2},
                )
                self.assertEqual(response.status_code, 201)
                item_id = response.get_json()["id"]

                response = client.get("/api/items")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.get_json()), 1)

                response = client.put(
                    f"/api/items/{item_id}",
                    json={"name": "Учебник", "quantity": 3},
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json()["name"], "Учебник")

                response = client.get("/table")
                self.assertEqual(response.status_code, 200)
                self.assertIn("Учебник", response.get_data(as_text=True))

                response = client.delete(f"/api/items/{item_id}")
                self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
