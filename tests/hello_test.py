# /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""

Author: samzong.lu
E-mail: samzong.lu@gmail.com

"""

import unittest

from src import hello


class TestHelloFunction(unittest.TestCase):
    def test_hello_returns_correct_string(self):
        self.assertEqual(hello.hello(), "Hello World")

    def test_hello_returns_string_type(self):
        self.assertIsInstance(hello.hello(), str)
