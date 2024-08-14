# tests/test_database.py

import unittest
from app.database import connect_to_db


class TestDatabase(unittest.TestCase):
    def test_db_connection(self):
        connection = connect_to_database()
        self.assertIsNotNone(connection)
        # Fechar conexão após o teste


if __name__ == '__main__':
    unittest.main()
