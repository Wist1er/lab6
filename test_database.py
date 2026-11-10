import tempfile
import unittest
from pathlib import Path

from database import (
    create_item,
    delete_item,
    init_db,
    list_items,
    update_item,
)


class TestDatabaseCrud(unittest.TestCase):
    def test_crud(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "test.db"
            init_db(db_path)

            created = create_item(db_path, "Книга", 2)
            self.assertEqual(created["name"], "Книга")
            self.assertEqual(len(list_items(db_path)), 1)

            updated = update_item(db_path, created["id"], "Учебник", 3)
            self.assertIsNotNone(updated)
            self.assertEqual(updated["name"], "Учебник")
            self.assertEqual(updated["quantity"], 3)

            self.assertTrue(delete_item(db_path, created["id"]))
            self.assertEqual(list_items(db_path), [])


if __name__ == "__main__":
    unittest.main()
