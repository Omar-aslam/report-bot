from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict
import pandas as pd
from .rules import normalize_type, categorize_description, DEFAULT_CATEGORY_RULES

@dataclass
class Columns:
    date: str = "date"
    description: str = "description"
    amount: str = "amount"
    tx_type: Optional[str] = "type"

def clean_transactions(df: pd.DataFrame, cols: Columns) -> pd.DataFrame:
    rename_map = {}
    if cols.date in df.columns: rename_map[cols.date] = "date"
    if cols.description in df.columns: rename_map[cols.description] = "description"
    if cols.amount in df.columns: rename_map[cols.amount] = "amount"
    if cols.tx_type and (cols.tx_type in df.columns): rename_map[cols.tx_type] = "type"
    df = df.rename(columns=rename_map)
    if "type" not in df.columns:
        df["type"] = None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["date", "amount", "description"])

    df["type"] = df.apply(lambda r: normalize_type(r["amount"], r.get("type")), axis=1)
    df["signed_amount"] = df.apply(lambda r: r["amount"] if r["type"] == "INCOME" else -abs(r["amount"]), axis=1)
    return df

def categorize(df: pd.DataFrame, rules: dict | None = None) -> pd.DataFrame:
    if rules is None:
        rules = DEFAULT_CATEGORY_RULES
    df["category"] = df["description"].apply(lambda d: categorize_description(str(d), rules))
    return df

def flag_large(df: pd.DataFrame, threshold: float = 10_000.0) -> pd.DataFrame:
    flags = df[df["amount"].abs() >= threshold].copy()
    flags.sort_values(by="amount", ascending=False, inplace=True)
    return flags

def summarize(df: pd.DataFrame) -> Dict[str, float]:
    total_income = df.loc[df["signed_amount"] > 0, "signed_amount"].sum()
    total_expense = -df.loc[df["signed_amount"] < 0, "signed_amount"].sum()
    net = df["signed_amount"].sum()
    return {
        "total_income": round(float(total_income), 2),
        "total_expense": round(float(total_expense), 2),
        "net": round(float(net), 2),
        "count": int(df.shape[0]),
    }

def category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    grp = df.groupby("category")["signed_amount"].sum().reset_index()
    grp["total"] = grp["signed_amount"].apply(lambda x: round(abs(float(x)), 2))
    grp = grp.drop(columns=["signed_amount"]).sort_values("total", ascending=False)
    return grp
