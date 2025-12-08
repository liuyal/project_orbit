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
            response = requests.delete(f"{cls.url}/api/projects/{prj_key}/nuke")
            assert response.status_code == 204

    @classmethod
    def clean_up_test_cases(cls):
        """ Clean up test cases after tests """

        # Cleanup existing test cases
        response = requests.get(f"{cls.url}/api/projects")
        for item in response.json():
            prj_key = item['project_key']
            response = requests.delete(f"{cls.url}/api/projects/{prj_key}/test-cases/")
            assert response.status_code == 204

    @pytest.mark.order(1)
    def test_projects(self):
        """ Test: Projects """

        logging.info(f"--- Starting test: {self._testMethodName} ---")
        self.__class__.clean_up_projects()

        response = requests.get(f"{self.__class__.url}/api/projects")
        assert response.status_code == 200
        assert response.json() == []

        n = 3
        for i in range(0, n):
            payload = {"project_key": f"PRJ{i}", "description": f"Project #{i}"}
            response = requests.post(f"{self.__class__.url}/api/projects", json=payload)
            assert response.status_code == 201

        response = requests.get(f"{self.__class__.url}/api/projects")
        assert response.status_code == 200
        assert len(response.json()) == n

        # self.__class__.clean_up_projects()
        logging.info(f"--- Test: {self._testMethodName} Complete ---")

    @pytest.mark.order(2)
    def test_test_cases(self):
        """ Test: Test Cases """

        logging.info(f"--- Starting test: {self._testMethodName} ---")
        self.__class__.clean_up_test_cases()

        n = 25

        project_key = "PRJ0"
        for i in range(0, n):
            payload = {"test_case_key": f"{project_key}-T{i}", "project_key": project_key}
            response = requests.post(f"{self.__class__.url}/api/projects/{project_key}/test-cases", json=payload)
            assert response.status_code == 201
        response = requests.get(f"{self.__class__.url}/api/test-cases")
        assert response.status_code == 200
        assert len(response.json()) == n

        project_key = "PRJ1"
        for i in range(0, n):
            payload = {"test_case_key": f"{project_key}-T{i}", "project_key": project_key}
            response = requests.post(f"{self.__class__.url}/api/projects/{project_key}/test-cases", json=payload)
            assert response.status_code == 201
        response = requests.get(f"{self.__class__.url}/api/test-cases")
        assert response.status_code == 200
        assert len(response.json()) == n * 2

        project_key = "PRJ2"
        for i in range(0, n):
            payload = {"test_case_key": f"{project_key}-T{i}", "project_key": project_key}
            response = requests.post(f"{self.__class__.url}/api/projects/{project_key}/test-cases", json=payload)
            assert response.status_code == 201
        response = requests.get(f"{self.__class__.url}/api/test-cases")
        assert response.status_code == 200
        assert len(response.json()) == n * 3

        prj_key = "PRJ1"
        response = requests.delete(f"{self.__class__.url}/api/projects/{prj_key}/test-cases/")
        assert response.status_code == 204
        response = requests.get(f"{self.__class__.url}/api/test-cases")
        assert response.status_code == 200
        assert len(response.json()) == n * 2

        # prj_key = "PRJ2"
        # response = requests.delete(f"{self.__class__.url}/api/projects/{prj_key}/test-cases/")
        # assert response.status_code == 204
        # response = requests.get(f"{self.__class__.url}/api/test-cases")
        # assert response.status_code == 200
        # assert len(response.json()) == n
        #
        # prj_key = "PRJ0"
        # response = requests.delete(f"{self.__class__.url}/api/projects/{prj_key}/test-cases/")
        # assert response.status_code == 204
        # response = requests.get(f"{self.__class__.url}/api/test-cases")
        # assert response.status_code == 200
        # assert len(response.json()) == 0

        # self.__class__.clean_up_projects()
        logging.info(f"--- Test: {self._testMethodName} Complete ---")


if __name__ == "__main__":
    unittest.main()
