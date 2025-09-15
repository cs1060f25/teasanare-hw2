import pytest
from index import app, text_to_number, number_to_text, base64_to_number, number_to_base64

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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
    
# --- Test Cases for Flask API Endpoints ---

def test_text_to_binary(client):
    """Test API conversion from text to binary."""
    response = client.post('/convert', json={'input': 'one', 'inputType': 'text', 'outputType': 'binary'})
    assert response.json['result'] == '1'
    assert response.json['error'] is None

def test_binary_to_text(client):
    """Test API conversion from binary to text."""
    response = client.post('/convert', json={'input': '111', 'inputType': 'binary', 'outputType': 'text'})
    assert response.json['result'] == 'seven'
    assert response.json['error'] is None

def test_decimal_to_base64(client):
    """Test API conversion from decimal to base64."""
    # This test will fail with the original buggy code.
    response = client.post('/convert', json={'input': '266', 'inputType': 'decimal', 'outputType': 'base64'})
    assert response.json['result'] == 'CgE='
    assert response.json['error'] is None

def test_base64_to_decimal(client):
    """Test API conversion from base64 to decimal."""
    # This test will fail with the original buggy code.
    response = client.post('/convert', json={'input': 'CgE=', 'inputType': 'base64', 'outputType': 'decimal'})
    assert response.json['result'] == '266'
    assert response.json['error'] is None
    
# --- Error Handling Tests ---

def test_invalid_input_type(client):
    """Test handling an invalid input type."""
    response = client.post('/convert', json={'input': '123', 'inputType': 'invalid_type', 'outputType': 'decimal'})
    assert response.json['error'] is not None
    assert "Invalid input type" in response.json['error']

def test_invalid_output_type(client):
    """Test handling an invalid output type."""
    response = client.post('/convert', json={'input': '123', 'inputType': 'decimal', 'outputType': 'invalid_type'})
    assert response.json['error'] is not None
    assert "Invalid output type" in response.json['error']

def test_invalid_base64_input(client):
    """Test handling malformed base64 input."""
    response = client.post('/convert', json={'input': 'invalid!', 'inputType': 'base64', 'outputType': 'decimal'})
    assert response.json['error'] is not None
    assert "Invalid base64 input" in response.json['error']

def test_invalid_octal_input(client):
    """Test handling invalid digits in an octal input."""
    response = client.post('/convert', json={'input': '18', 'inputType': 'octal', 'outputType': 'decimal'})
    assert response.json['error'] is not None
    assert "invalid literal" in response.json['error']
    
# --- text2digits Library Error Handling Test
def test_invalid_english_input(client):
    """Test handling digits in an english text input."""
    response = client.post('/convert', json={'input': '18', 'inputType': 'text', 'outputType': 'decimal'})
    assert response.json['error'] is not None
    assert "Invalid English Text input" in response.json['error']  
