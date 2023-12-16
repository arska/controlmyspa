# Balboa ControlMySpa™ cloud API for hot tub spa systems

[![Tests](https://github.com/arska/controlmyspa/actions/workflows/main.yml/badge.svg)](https://github.com/arska/controlmyspa/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/arska/controlmyspa/branch/main/graph/badge.svg?token=H2107AXHOX)](https://codecov.io/gh/arska/controlmyspa)
[![PyPI version](https://badge.fury.io/py/controlmyspa.svg)](https://badge.fury.io/py/controlmyspa)

Python API for ControlMySpa.com cloud-controlled of Balboa spa control systems for hot tubs.

- https://www.balboawatergroup.com/ControlMySpa
- https://controlmyspa.com

## 2023-12-13: iot.controlmyspa.com missing intermediate certificate

Since approximately June 2023 iot.controlmyspa.com has a new TLS certificate. This certificate is signed by digicert, but the intermediate certificate chain is not served by iot.controlmyspa.com and is also missing in the python certifi trust store. Instead of disabling the TLS certificate validation, we download the intermediate certificate from digicert over a successfully verified TLS connection and add it to the local trust store on first run. This does, however, not work for read-only runtimes like Docker containers. See https://github.com/arska/controlmyspa-porssari/blob/main/Dockerfile and https://github.com/arska/controlmyspa-porssari/blob/main/get_certificate.py for an example how to download the certificate at Docker image build time instead.

## Usage

see example.py for a runnable example

```python
from controlmyspa import ControlMySpa

API = ControlMySpa("user@example.com", "myverysecretpassword")
pprint.pprint(API._info)
```

## References

Based on the JavaScript library https://gitlab.com/VVlasy/controlmyspajs
