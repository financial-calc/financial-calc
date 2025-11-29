# install poetry dependencies
install:
    pip install poetry
    poetry install --no-root

# run tests
test:
    poetry run pytest

# package build
build:
    rm -rf dist
    poetry build

# publish on TestPyPI
publish-testpypi:
    twine upload -r testpypi dist/*

# publish on PyPI
publish-pypi:
    twine upload dist/*
