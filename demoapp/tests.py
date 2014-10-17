# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_user_info_service(self):
        from demoapp.views import get_info, set_info
        request = testing.DummyRequest()
        request.matchdict = {"username": "user1"}
        info = get_info(request)
        self.assertEqual(info, {})
