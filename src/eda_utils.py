# src/eda_utils.py
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV with error handling."""
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Data loaded successfully from {filepath}, shape: {df.shape}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

def basic_quality_report(df: pd.DataFrame) -> None:
    """Print missing values and duplicates."""
    print("Missing values:\n", df.isnull().sum())
    print(f"Duplicate rows: {df.duplicated().sum()}")