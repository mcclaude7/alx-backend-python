# ALX Backend Python Project

This project contains unit tests for utility functions in the `utils` module.

## Setup
1. Clone the repository: `git clone https://github.com/mcclaude7/alx-backend-python.git`
2. Install dependencies: `pip install parameterized`
3. Ensure Python 3.7 is installed on Ubuntu 18.04 LTS.

## Usage
Run tests with:
```bash
python3 -m unittest test_utils.py

## 🌐 Mocking HTTP Requests with unittest.mock

We test the `get_json(url)` function using mocks to avoid real HTTP calls.

### What It Does

- Sends a `GET` request to a URL using `requests.get`.
- Returns the parsed JSON response.

### Why Mock?

- Ensures unit tests are not dependent on external servers.
- Makes tests fast and consistent.

### How We Tested It

- Used `@patch("utils.requests.get")` to mock the network call.
- Simulated `.json()` using a `Mock()` object.
- Checked:
  - That `requests.get(url)` was called once.
  - The output of `get_json(url)` matches expected payload.

### Example Tested Inputs

| URL                   | Payload              |
|------------------------|-----------------------|
| `http://example.com`   | `{ "payload": True }` |
| `http://holberton.io`  | `{ "payload": False }` |

