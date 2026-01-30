from error_handling import is_password_secure

# Test is_password_secure
def test_is_password_secure_accepts_symbols_upper_lower_number():
    assert is_password_secure("Hello32!@") is True

def test_is_password_secure_include_special_symbol():
    assert is_password_secure("Hello32") is False

def test_is_password_secure_include_uppercase():
    assert is_password_secure("hello32!@") is False

def test_is_password_secure_include_lowercase():
    assert is_password_secure("HELLO32!@") is False

def test_is_password_secure_include_number():
    assert is_password_secure("Hello!@") is False


