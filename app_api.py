from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from report_bot.core import Columns, clean_transactions, categorize, flag_large, summarize, category_breakdown

app = FastAPI(title="Report Bot API", version="0.1.0")

class ReportRequest(BaseModel):
    records: list[dict]
    date_col: str = "date"
    amount_col: str = "amount"
    desc_col: str = "description"
    type_col: str | None = "type"
    threshold: float = 10_000.0

@app.post("/report")
def create_report(req: ReportRequest):
    df = pd.DataFrame(req.records)
    cols = Columns(date=req.date_col, description=req.desc_col, amount=req.amount_col, tx_type=req.type_col)
    df = clean_transactions(df, cols)
    df = categorize(df)
    flags = flag_large(df, threshold=req.threshold)
    summary = summarize(df)
    cat = category_breakdown(df)
    return {
        "summary": summary,
        "category_breakdown": cat.to_dict(orient="records"),
        "flags": flags.to_dict(orient="records"),
        "transactions_count": int(df.shape[0]),
    }
