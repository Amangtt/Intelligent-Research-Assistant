import os,sys
import pytest
import pandas as pd
import fitz  # PyMuPDF
import logging
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.extract import get_data  


@pytest.fixture(scope="module")
def setup_test_env():
    """Fixture to set up and clean up the test environment"""
    test_folder = "test_pdfs"
    output_csv = "test_output.csv"
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)

    os.makedirs(test_folder, exist_ok=True)

    # Create a mock PDF file
    with open(os.path.join(test_folder, "test.pdf"), "wb") as f:
        f.write(b"%PDF-1.4 mock pdf content")

    yield test_folder, output_csv, logger

    # Cleanup
    if os.path.exists(output_csv):
        os.remove(output_csv)
    for file in os.listdir(test_folder):
        os.remove(os.path.join(test_folder, file))
    os.rmdir(test_folder)


@patch("fitz.open")
@patch("os.listdir")
def test_load(mock_listdir, mock_fitz_open, setup_test_env):
    """Test PDF text extraction and CSV writing"""
    test_folder, output_csv, logger = setup_test_env

    # Mock os.listdir to return a test PDF file
    mock_listdir.return_value = ["test.pdf"]

    # Mock fitz.open and get_text to return dummy text
    mock_pdf = MagicMock()
    mock_pdf.__enter__.return_value = mock_pdf  # Ensure context manager works
    mock_pdf.__exit__.return_value = False
    mock_page = MagicMock()
    mock_page.get_text.return_value = "Mock PDF Content"
    mock_pdf.__iter__.return_value = iter([mock_page])  # Ensure iteration works
    mock_fitz_open.return_value = mock_pdf

    # Run the function
    extractor = get_data(test_folder, output_csv, logger)
    extractor.load()

    # Check if the output CSV is created
    assert os.path.exists(output_csv), "CSV file was not created"

    # Check if the extracted text matches the expected output
    df = pd.read_csv(output_csv)
    assert df.shape[0] == 1, "Incorrect number of rows in CSV"
    assert df.iloc[0]["filename"] == "test.pdf", "Filename mismatch"
    assert df.iloc[0]["content"] == "Mock PDF Content", "Extracted text mismatch"
