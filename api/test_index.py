from index import text_to_number, number_to_text, base64_to_number, number_to_base64

# --- Test Cases for Helper Functions ---

def test_text_to_number():
    """Test converting English text numbers to integers."""
    assert text_to_number("zero") == 0
    assert text_to_number("ten") == 10
    assert text_to_number("one hundred and twenty-three") == 123

def test_number_to_text():
    """Test converting integers to English text."""
    assert number_to_text(1) == "one"
    assert number_to_text(100) == "one hundred"
    assert number_to_text(123) == "one hundred and twenty-three"

def test_base64_to_number():
    """Test base64 to number conversion, checking for correct endianness."""
    assert base64_to_number("Cg==") == 10
    assert base64_to_number("CgE=") == 266

def test_number_to_base64():
    """Test number to base64 conversion, checking for correct endianness."""
    assert number_to_base64(10) == "Cg=="
    assert number_to_base64(266) == "CgE="