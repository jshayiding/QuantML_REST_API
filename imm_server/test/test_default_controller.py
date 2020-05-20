# coding: utf-8

from __future__ import absolute_import
from flask import json
from six import BytesIO

from imm_server.models.immunomatch_ed_input import ImmunomatchEdInput  # noqa: E501
from imm_server.models.immunomatch_ed_output import ImmunomatchEdOutput  # noqa: E501
from imm_server.models.version import Version  # noqa: E501
from imm_server.test import BaseTestCase

class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_about_get(self):
        """Test case for about_get

        ImmunoMatch System Version
        """
        response = self.client.open(
            '/about',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_immunomatch_ed_post(self):
        """Test case for immunomatch_ed_post

        ImmunoMatch ED Execution interface
        """
        body = ImmunomatchEdInput()
        response = self.client.open(
            '/immunomatch_ed',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_log_get(self):
        """Test case for log_get

        Return log
        """
        query_string = [('type', 'type_example')]
        response = self.client.open(
            '/log',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rsession_get(self):
        """Test case for rsession_get

        Collect Information About The Current R Session
        """
        response = self.client.open(
            '/rsession',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
