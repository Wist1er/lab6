import unittest

import fastapi_app
from fastapi_app import TaskCreate


class TestFastApiLogic(unittest.TestCase):
    def setUp(self):
        fastapi_app._tasks[:] = [
            fastapi_app.Task(id=1, title="Тест", completed=False)
        ]
        fastapi_app._next_id = 2

    def test_hello_parameter(self):
        self.assertEqual(
            fastapi_app.hello("Никита"),
            {"message": "Привет, Никита!"},
        )

    def test_create_and_list_task(self):
        created = fastapi_app.create_task(
            TaskCreate(title="Новая задача", completed=False)
        )

        self.assertEqual(created.id, 2)
        self.assertEqual(created.title, "Новая задача")
        self.assertEqual(len(fastapi_app.get_tasks()), 2)


if __name__ == "__main__":
    unittest.main()
