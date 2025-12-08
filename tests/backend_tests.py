# ================================================================
# Orbit API
# Description: FastAPI backend sanity test script for the Orbit application.
# Version: 0.1.0
# Author: Jerry
# License: MIT
# ================================================================

import logging
import unittest

import pytest
import requests


class OrbitBackendSanityTest(unittest.TestCase):
    """ Orbit Sanity Tests """

    @classmethod
    def setUpClass(cls):
        """ Initialize device """

        logging.info(f"Initialize Tests...")

        cls.host = pytest.options['host']
        cls.port = pytest.options['port']
        cls.protocol = pytest.options['protocol']
        cls.url = f"{cls.protocol}://{cls.host}:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        """ Teardown device """

        logging.info(f"Teardown Tests...")

    @classmethod
    def clean_up_projects(cls):
        """ Clean up projects after tests """

        # Cleanup existing projects
        response = requests.get(f"{cls.url}/api/projects")
        for item in response.json():
            prj_key = item['project_key']
            response = requests.delete(f"{cls.url}/api/projects/{prj_key}")
            assert response.status_code == 204

    @pytest.mark.order(1)
    def test_list_projects(self):
        """ Test: List Projects - Expecting empty list """

        logging.info(f"--- Starting test: {self._testMethodName} ---")
        self.__class__.clean_up_projects()

        response = requests.get(f"{self.__class__.url}/api/projects")
        assert response.status_code == 200
        assert response.json() == []

        self.__class__.clean_up_projects()
        logging.info(f"--- Test: {self._testMethodName} Complete ---")

    @pytest.mark.order(2)
    def test_create_projects(self):
        """ Test: Create Projects """

        logging.info(f"--- Starting test: {self._testMethodName} ---")
        self.__class__.clean_up_projects()

        n = 3
        for i in range(0, n):
            payload = {"project_key": f"PRJ-{i}", "description": f"Project #{i}"}
            response = requests.post(f"{self.__class__.url}/api/projects",
                                     json=payload)
            assert response.status_code == 201

        response = requests.get(f"{self.__class__.url}/api/projects")
        assert response.status_code == 200
        assert len(response.json()) == n

        #self.__class__.clean_up_projects()
        logging.info(f"--- Test: {self._testMethodName} Complete ---")


if __name__ == "__main__":
    unittest.main()
