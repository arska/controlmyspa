# Balboa ControlMySpa Whirlpool cloud API

[![Python package](https://github.com/arska/controlmyspa/actions/workflows/main.yml/badge.svg)](https://github.com/arska/controlmyspa/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/arska/controlmyspa/branch/main/graph/badge.svg?token=H2107AXHOX)](https://codecov.io/gh/arska/controlmyspa)
[![PyPI version](https://badge.fury.io/py/controlmyspa.svg)](https://badge.fury.io/py/controlmyspa)

Python API for ControlMySpa.com cloud-controlled whirlpools

## Usage

see example.py for runnable example

```python
from controlmyspa import ControlMySpa

API = ControlMySpa("user@example.com", "myverysecretpassword")
pprint.pprint(API._info)
```

## References

Based on the JavaScript library https://gitlab.com/VVlasy/controlmyspajs
