import io
import pandas as pd
import streamlit as st

from report_bot.core import Columns, clean_transactions, categorize, flag_large, summarize, category_breakdown
from report_bot.io_utils import ensure_dir, save_category_chart, save_monthly_net_chart

st.set_page_config(page_title="Report Bot", page_icon="📊", layout="wide")
st.title("📊 Report Bot — Transactions to Insights")

st.markdown("Upload a CSV or Excel file of transactions, choose options, and generate a summarized report with optional charts.")

with st.expander("ℹ️ Expected columns & tips", expanded=False):
    st.write("""
    **Default columns**: `date`, `description`, `amount`, optional `type` (INCOME/EXPENSE).
    If your file uses different names, remap them in the sidebar.
    Amounts may be positive or negative; if `type` is missing, negative => EXPENSE, positive => INCOME.
    """)

st.sidebar.header("Options")
threshold = st.sidebar.number_input("Large-transaction threshold", min_value=0.0, value=10000.0, step=100.0)
make_charts = st.sidebar.checkbox("Generate charts", value=True)
delimiter = st.sidebar.text_input("CSV delimiter (for .csv files)", value=",")

date_col = st.sidebar.text_input("Date column", "date")
amount_col = st.sidebar.text_input("Amount column", "amount")
desc_col = st.sidebar.text_input("Description column", "description")
type_col = st.sidebar.text_input("Type column (optional)", "type")

uploaded = st.file_uploader("Upload transactions file (.csv or .xlsx)", type=["csv", "xlsx", "xls"])

if uploaded is not None:
    try:
        if uploaded.name.lower().endswith(".csv"):
            df_in = pd.read_csv(uploaded, delimiter=delimiter)
        else:
            df_in = pd.read_excel(uploaded)
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        st.stop()

    st.subheader("Preview")
    st.dataframe(df_in.head(20), use_container_width=True)

    cols = Columns(date=date_col, description=desc_col, amount=amount_col, tx_type=type_col or None)
    try:
        df = clean_transactions(df_in, cols)
        df = categorize(df)
        flags = flag_large(df, threshold=threshold)
        summary = summarize(df)
        cat = category_breakdown(df)
    except Exception as e:
        st.error(f"Processing error: {e}")
        st.stop()

    st.subheader("Summary")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Income", f"${summary['total_income']:,}")
    s2.metric("Total Expense", f"${summary['total_expense']:,}")
    s3.metric("Net", f"${summary['net']:,}")
    s4.metric("Transactions", f"{summary['count']:,}")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Category Breakdown")
        st.dataframe(cat, use_container_width=True)
    with c2:
        st.markdown("### Large Transactions")
        st.dataframe(flags, use_container_width=True)

    if make_charts:
        outdir = ensure_dir("output")
        try:
            p1 = save_category_chart(str(outdir), cat)
            p2 = save_monthly_net_chart(str(outdir), df, date_col="date", signed_col="signed_amount")
            img_cols = st.columns(2)
            img_cols[0].image(str(p1), caption="Category Breakdown")
            img_cols[1].image(str(p2), caption="Monthly Net")
        except Exception as e:
            st.warning(f"Could not create charts: {e}")

    st.markdown("### Download Excel Report")
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            pd.DataFrame([summary]).to_excel(writer, sheet_name="Summary", index=False)
            cat.to_excel(writer, sheet_name="CategoryBreakdown", index=False)
            df.to_excel(writer, sheet_name="Transactions", index=False)
            flags.to_excel(writer, sheet_name="Flags", index=False)
        output.seek(0)
        st.download_button(
            label="⬇️ Download Excel Report",
            data=output,
            file_name="report_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as e:
        st.error(f"Failed to build Excel for download: {e}")
else:
    st.info("Upload a .csv or .xlsx file to begin.")
