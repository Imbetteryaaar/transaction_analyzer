import pandas as pd

def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    monthly = df.groupby('month').agg(
        total_amount = ('amount', 'sum'),
        income = ('amount', lambda x: x[x>0].sum()),
        expenses = ('amount', lambda x: x[x<0].sum())
    ).reset_index()
    monthly['expenses'] = monthly['expenses'].abs()
    return monthly

def category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    cat = df.groupby('category').agg(
        total = ('amount', 'sum'),
        count = ('amount', 'count'),
        avg = ('amount', 'mean')
    ).reset_index()
    cat['total_abs'] = cat['total'].abs()
    cat = cat.sort_values('total_abs', ascending=False)
    return cat

def top_merchants(df: pd.DataFrame, n=10):
    return df.groupby('description').agg(total=('amount','sum'), count=('amount','count')).sort_values('total').head(n)
