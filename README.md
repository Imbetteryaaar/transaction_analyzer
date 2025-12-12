Transaction Analyzer Dashboard

A powerful Streamlit-based data analytics dashboard for exploring bank transaction data, detecting anomalies, generating summaries, and exporting a fully formatted PDF report.

Features
Upload & View Transactions

Upload your .csv file or load the included sample dataset

View the first 200 rows instantly in a clean, interactive table

Monthly Income/Expense Summary

Automatically aggregates monthly totals

Interactive Matplotlib line chart

Export-ready summary values

Category Breakdown

Groups spending by categories

Shows total amounts + count per category

Optional Plotly Pie Chart for visualization

Top Merchants

See which merchants appear most often

Useful for spend pattern insights

Outlier Detection (ML + Rules)

Detects unusual transactions using:

ML anomaly scoring

Business rule flags

Export suspicious transactions as CSV

PDF Report Generator (ReportLab)

Auto Generates a clean multipage PDF including:

Summary text

Monthly chart

Category pie chart

Includes inline images and page breaks

Tech Stack
Component	Technologies
Frontend	Streamlit
Backend	Python
Data	Pandas
Visualization	Matplotlib, Plotly
PDF Engine	ReportLab
ML Detection	Scikit-learn (Isolation Forest)
Project Structure	Modular src/ folder architecture

Future Enhancements

OCR support for PDF bank statements

More ML models for anomaly detection

Category auto-detection using NLP

Dashboard themes & dark mode

Contributing
Pull requests are welcome!
