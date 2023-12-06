# PyTest Testing

Info for setting up tests and running tests

### Setup

Activate Virtual Environment

    .\venv\Scripts\Activate.ps1

Install Requirements

    python -m pip install -r testing-requirements.txt

Get Playwright binaries

    playwright install

### Usage

*Ensure Application is Running* 

Run All Tests

    pytest -v

Allocate more cores

    pytest --numprocessors <num> -v

Run Individual Tests

    pytest tests/<test file>.py::<test_function_name> -v

    pytest tests/test_user_access.py::test_admin_access_admin -v