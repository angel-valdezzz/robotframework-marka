---
tags:
  - Development
---

# Development and publishing

## Install

```bash
pip install "robotframework-marka[robot]"
```

Python users can install `robotframework-marka` without the Robot adapter dependencies.

## Development and publishing

```bash
python -m pip install -e ".[robot,dev]"
pytest
ruff check .
ruff format --check .
python docs/scripts/build_docs.py
poetry build
```

Pull requests validate code, browser examples, both languages and distributable packages.
Documentation deploys from `main`. Releases publish to PyPI through GitHub OIDC Trusted Publishing:
configure repository `robotframework-marka`, workflow `release.yml`, environment `pypi`, then publish tag `v0.1.0`.
No API tokens are stored in this repository. Keep release tags aligned with `pyproject.toml`.
