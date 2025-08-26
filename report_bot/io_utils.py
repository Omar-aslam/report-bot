from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def read_input(path: str, delimiter: str = ",") -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    if p.suffix.lower() == ".csv":
        return pd.read_csv(p, delimiter=delimiter)
    elif p.suffix.lower() in {".xls", ".xlsx"}:
        return pd.read_excel(p)
    else:
        raise ValueError("Unsupported file type. Use .csv, .xls, or .xlsx")

def ensure_dir(path: str) -> Path:
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    return out

def export_excel(outdir: str, df_transactions: pd.DataFrame, df_flags: pd.DataFrame, df_categories: pd.DataFrame, summary: dict):
    out_path = Path(outdir) / "report_summary.xlsx"
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        pd.DataFrame([summary]).to_excel(writer, sheet_name="Summary", index=False)
        df_categories.to_excel(writer, sheet_name="CategoryBreakdown", index=False)
        df_transactions.to_excel(writer, sheet_name="Transactions", index=False)
        df_flags.to_excel(writer, sheet_name="Flags", index=False)
    return out_path

def export_csv(outdir: str, df_transactions: pd.DataFrame, df_flags: pd.DataFrame, df_categories: pd.DataFrame, summary: dict):
    out = Path(outdir)
    out_tx = out / "transactions.csv"
    out_flags = out / "flags.csv"
    out_cat = out / "category_breakdown.csv"
    out_summary = out / "summary.json"
    df_transactions.to_csv(out_tx, index=False)
    df_flags.to_csv(out_flags, index=False)
    df_categories.to_csv(out_cat, index=False)
    pd.Series(summary).to_json(out_summary, indent=2)
    return out_tx, out_flags, out_cat, out_summary

def save_category_chart(outdir: str, df_categories: pd.DataFrame):
    fig = plt.figure()
    ax = df_categories.set_index("category")["total"].plot(kind="bar")
    ax.set_title("Total by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Total ($)")
    fig.tight_layout()
    out_path = Path(outdir) / "category_breakdown.png"
    fig.savefig(out_path)
    plt.close(fig)
    return out_path

def save_monthly_net_chart(outdir: str, df: pd.DataFrame, date_col: str, signed_col: str):
    df2 = df.copy()
    df2[date_col] = pd.to_datetime(df2[date_col], errors="coerce")
    grp = df2.groupby(df2[date_col].dt.to_period("M"))[signed_col].sum().sort_index()
    fig = plt.figure()
    ax = grp.to_timestamp().plot(kind="line", marker="o")
    ax.set_title("Monthly Net ($)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Net ($)")
    fig.tight_layout()
    out_path = Path(outdir) / "monthly_net.png"
    fig.savefig(out_path)
    plt.close(fig)
    return out_path
