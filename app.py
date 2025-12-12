# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import plotly.io as pio
import io

from src.data_utils import load_transactions, preprocess
from src.analysis import monthly_summary, category_breakdown, top_merchants
from src.outliers import detect_outliers
from src.pdf_report import make_pdf

st.set_page_config(page_title="Transaction Analyzer", layout="wide")

st.title("Transaction Analyzer - Data Analytics Dashboard")

uploaded = st.file_uploader("Upload CSV", type=['csv'])
if uploaded is None:
    st.info("Upload a CSV or try the sample below.")
    if st.button("Load sample CSV"):
        uploaded = "transactions_sample.csv"  # local sample file path

if uploaded:
    try:
        df = load_transactions(uploaded)
    except Exception as e:
        st.error(f"Failed to load: {e}")
        st.stop()

    st.subheader("Raw transactions")
    st.dataframe(df.head(200))

    # Summaries
    st.subheader("Monthly summary")
    monthly = monthly_summary(df)
    st.dataframe(monthly)

    # Plot monthly
    fig, ax = plt.subplots()
    ax.plot(monthly['month'].dt.strftime('%Y-%m'), monthly['income'], marker='o', label='Income')
    ax.plot(monthly['month'].dt.strftime('%Y-%m'), monthly['expenses'], marker='o', label='Expenses')
    ax.set_xticklabels(monthly['month'].dt.strftime('%Y-%m'), rotation=45)
    ax.set_ylabel('Amount')
    ax.legend()
    st.pyplot(fig)

    st.subheader("Category breakdown")
    cat = category_breakdown(df)
    st.dataframe(cat[['category','total_abs','count']])

    # Pie chart using plotly
    try:
        import plotly.express as px
        fig2 = px.pie(cat, names='category', values='total_abs', title='Spending by category')
        st.plotly_chart(fig2, use_container_width=True)
    except Exception:
        st.write("Install plotly for nicer charts.")

    st.subheader("Top merchants")
    st.dataframe(top_merchants(df))

    # Outliers
    st.subheader("Unusual / suspicious transactions (ML + rules)")
    df_anom = detect_outliers(df)
    suspicious = df_anom[df_anom['suspicious']].sort_values('anomaly_score')
    st.dataframe(suspicious[['date','description','amount','category','anomaly_score','rule_flag']])

    # Allow user to export CSV of suspicious
    csv = suspicious.to_csv(index=False).encode('utf-8')
    st.download_button("Download suspicious CSV", data=csv, file_name="suspicious.csv", mime="text/csv")

    # ----------------------- PDF EXPORT SECTION -----------------------
    st.subheader("Export PDF report")

    if uploaded:   
        if st.button("Generate PDF report"):
            try:
                # -------- Summary text --------
                total_income = df[df['amount'] > 0]['amount'].sum()
                total_expenses = df[df['amount'] < 0]['amount'].abs().sum()
                top_cat = cat.iloc[0]['category'] if len(cat) > 0 else 'N/A'

                summary = f"""Transaction Summary
    ------------------------
    Total transactions: {len(df)}
    Total income: {total_income:.2f}
    Total expenses: {total_expenses:.2f}
    Top category by spend: {top_cat}
    Suspicious transactions detected: {len(suspicious)}
    """

                # -------- CHART IMAGES --------
                charts = {}

                # Monthly chart (Matplotlib)
                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight')
                charts['Monthly Chart'] = buf.getvalue()
                buf.close()

                # Pie chart (Plotly)
                if 'fig2' in locals():
                    buf2 = io.BytesIO()
                    pio.write_image(fig2, buf2, format='png', width=800, height=400)
                    charts['Category Pie'] = buf2.getvalue()
                    buf2.close()


                # -------- Generate PDF --------
                pdf_bytes = make_pdf(summary, charts)

                st.download_button(
                    "Download PDF report",
                    data=pdf_bytes,
                    file_name="transaction_report.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"Unexpected error: {e}")

    else:
        st.info("Upload a CSV before generating a PDF.")

