import os
from enum import auto
from unittest.mock import patch

import pytest

from jaaspr.core.enums import FromEnviron


def get_config():
    class TestConfig(FromEnviron):
        TEST_VAR = auto()
        INT_VAR = auto()
    return TestConfig


@pytest.fixture(scope="module", autouse=True)
def patch_environment():
    with patch.dict(os.environ, {'TEST_VAR': 'test_value', 'INT_VAR': '42'}):
        yield


# Test cases
def test_environment_variable_reading():
    """Test reading environment variables using patch.dict."""
    with patch.dict(os.environ, {'TEST_VAR': 'test_value', 'INT_VAR': '42'}):
        assert get_config().TEST_VAR.value == 'test_value'
        assert get_config().INT_VAR.value == '42'


def test_environment_variable_type_conversion():
    """Test type conversion of environment variables using patch.dict."""
    with patch.dict(os.environ, {'TEST_VAR': 'test_value', 'INT_VAR': '42',}):
        assert get_config().TEST_VAR.coerce_value(str) == 'test_value'
        assert get_config().INT_VAR.coerce_value(int) == 42


def test_undefined_environment_variable():
    """Test behavior when an undefined environment variable is accessed."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="Environment variable declared, but undefined: TEST_VAR"):
            _ = get_config().TEST_VAR.value
