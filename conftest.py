import pytest

from .orm import SessionFactory


@pytest.fixture
def session():
    return SessionFactory.create_session()
