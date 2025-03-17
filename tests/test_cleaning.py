import pytest
import pandas as pd
import logging
import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.clean import clean_text

@pytest.fixture
def setup_test_env(tmp_path):
    """Setup test environment with sample data."""
    test_data = pd.DataFrame({"content": ["Hello, this is a test! The quick brown fox.", "Another sample text with stopwords."]})
    output_file = tmp_path / "cleaned_output.csv"
    logger = logging.getLogger("test_logger")
    
    return test_data, output_file, logger

def test_clean_text(setup_test_env):
    """Test text cleaning and stopword removal."""
    df, output_file, logger = setup_test_env

    cleaner = clean_text(df, output_file, logger)
    cleaner.clean_text()

    # Load the cleaned output
    cleaned_df = pd.read_csv(output_file)

    assert "cleaned_content" in cleaned_df.columns, "Missing cleaned_content column"
    assert cleaned_df.shape[0] == 2, "Incorrect number of rows"
    assert "test" in cleaned_df.iloc[0]["cleaned_content"], "Text cleaning failed"
    assert "the" not in cleaned_df.iloc[0]["cleaned_content"], "Stopword removal failed"
