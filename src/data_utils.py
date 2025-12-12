import pandas as pd
import numpy as np

DATE_COLS = ['date']

def load_transactions(file_like):
    # Accepts file path or file-like (Streamlit uploader)
    df = pd.read_csv(file_like)
    return preprocess(df)

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    # Standardize column names
    df = df.rename(columns={c: c.strip() for c in df.columns})
    # Ensure required columns
    if 'date' not in df.columns:
        raise ValueError("CSV must contain a 'date' column")
    # Parse dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # Drop rows without dates
    df = df.dropna(subset=['date'])
    # Amount to numeric
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['amount'])
    # Category fallback
    if 'category' not in df.columns:
        df['category'] = df['description'].apply(guess_category)
    df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()
    df = df.sort_values('date').reset_index(drop=True)
    return df

def guess_category(desc: str) -> str:
    desc = str(desc).lower()
    if any(k in desc for k in ['supermarket', 'grocery', 'grocer', 'mart']):
        return 'Groceries'
    if any(k in desc for k in ['salary', 'pay', 'payroll']):
        return 'Salary'
    if any(k in desc for k in ['cafe', 'coffee', 'star']):
        return 'Food'
    if any(k in desc for k in ['electric', 'power', 'utility']):
        return 'Utilities'
    return 'Other'
