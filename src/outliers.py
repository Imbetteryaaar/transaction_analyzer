import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def detect_outliers(df: pd.DataFrame, features=['amount']):
    # Use amount and maybe day-of-month to help detect anomalies
    X = pd.DataFrame()
    X['amount'] = df['amount'].abs()  # magnitude matters
    X['day'] = df['date'].dt.day
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    iso = IsolationForest(contamination=0.01, random_state=42)
    preds = iso.fit_predict(Xs)
    df = df.copy()
    df['anomaly_score'] = iso.decision_function(Xs)
    df['is_anomaly'] = preds == -1
    # Add some rule-based flags for suspicious items: large amount, duplicate large payments
    df['rule_flag'] = (df['amount'].abs() > df['amount'].abs().mean() + 3*df['amount'].abs().std())
    df['suspicious'] = df['is_anomaly'] | df['rule_flag']
    return df.sort_values('anomaly_score')
