# tests/test_dash_app/test_g1_news/test_layouts.py

import unittest
from app.dash_app.g1_news.layouts import create_layout


class TestG1NewsLayout(unittest.TestCase):
    def test_layout_creation(self):
        layout = create_layout()
        self.assertIsNotNone(layout)
        # Adicionar mais asserts conforme necessário


if __name__ == '__main__':
    unittest.main()
