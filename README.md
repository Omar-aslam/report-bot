# 📊 Report Bot — Transactions to Insights

**Report Bot** is a student project built in Python that ingests a CSV/Excel of transactions, cleans and categorizes them, flags large transactions, and generates a summarized **Excel report + charts**.  

It’s designed to demonstrate **automation, data handling, and software development lifecycle (SDLC) skills**

---

## ✨ Features

- 🗂️ **Input**: works with CSV or Excel (`.csv`, `.xlsx`)
- 🧼 **Cleaning**: parses dates, coerces amounts, and infers transaction type if missing
- 🏷️ **Categorization**: keyword-based rules (editable in `report_bot/rules.py`)
- 🚩 **Flags**: highlights large transactions (default: $10,000, customizable)
- 📈 **Outputs**:
  - Excel report (multi-sheet): Summary, Category Breakdown, Transactions, Flags
  - Optional charts (PNG): Category breakdown bar chart + Monthly net line chart
- 🌐 Run it as:
  - A **Streamlit web app** (friendly UI)
  - A **command-line tool**
  - An **optional FastAPI backend**

---

## 🏗 Project Structure

```

report-bot/
├─ report\_bot/
│   ├─ **init**.py
│   ├─ core.py           # cleaning, categorization, flags, summary
│   ├─ rules.py          # keyword rules + type inference
│   └─ io\_utils.py       # IO helpers + chart saving
├─ app\_streamlit.py      # Streamlit web app (upload + charts + Excel download)
├─ app\_api.py            # Optional FastAPI REST API
├─ tests/
│   └─ sample\_transactions.csv
├─ requirements.txt
└─ README.md

````

---

## 🚀 Quick Start

> Prerequisites: **Python 3.9+** and **pip**

```bash
# 1) Clone or download this repo
git clone https://github.com/<YOUR_USERNAME>/report-bot.git
cd report-bot

# 2) Create & activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\activate
# Windows (if PowerShell blocks scripts):
.\.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt
````

---

## ▶️ Option A — Run as a Website (Streamlit)

```bash
streamlit run app_streamlit.py
```

* Open the local URL ([http://localhost:8501](http://localhost:8501) by default).
* Upload a CSV/Excel file.
* Preview data, view summary stats, see flagged large transactions, and download an Excel report.
* Toggle chart generation (saved in `./output/`).

---

## ▶️ Option B — Command-Line Pipeline

```bash
python -m report_bot.cli tests/sample_transactions.csv --out output --export excel --threshold 8000 --charts
```

Generates:

* `report_summary.xlsx` (multi-sheet)
* `category_breakdown.png`
* `monthly_net.png`

---

## ▶️ Option C — REST API (FastAPI, optional)

```bash
uvicorn app_api:app --reload --port 8000
```

Test it:

```bash
curl -X POST http://127.0.0.1:8000/report \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {"date":"2025-01-03","description":"Payroll - RBC Direct Deposit","amount":3000,"type":"INCOME"},
      {"date":"2025-01-04","description":"Metro Groceries","amount":-56.43,"type":"EXPENSE"}
    ],
    "threshold": 8000
  }'
```

---

## 📦 Sample Data

You can test quickly with the included:

```
tests/sample_transactions.csv
```

or create your own, e.g.:

```csv
date,description,amount,type
2025-01-02,Payroll - RBC Direct Deposit,2800.00,INCOME
2025-01-05,Metro Groceries,-75.34,EXPENSE
2025-01-12,Rent Payment,-1200.00,EXPENSE
2025-01-28,Bonus Payment,500.00,INCOME
```

> If `type` is missing, the program infers it (negative = EXPENSE, positive = INCOME).

---

## ⚙️ Configuration

* **Categories/keywords**: edit `DEFAULT_CATEGORY_RULES` in `report_bot/rules.py`
* **Large transaction threshold**: change in Streamlit sidebar, CLI flag, or API JSON
* **Charts**: toggle in Streamlit; saved to `./output/`

---

## 🧪 SDLC Talking Points

This project demonstrates:

* **Requirements → Design → Implementation → Testing**

  * *Requirements*: parse input, categorize, flag, summarize, export
  * *Design*: modular package (`core`, `rules`, `io_utils`) + UI/API entry points
  * *Implementation*: clear Python functions, documented & commented
  * *Testing*: `tests/sample_transactions.csv` + manual runs via CLI and UI
* **Code quality**: docstrings, inline comments, clear error handling
* **Future extensions**:

  * Config file (YAML) for custom rules
  * Continuous Integration (GitHub Actions)
  * Deploy Streamlit app on the cloud
  * Database storage (SQLite/Postgres)

---

## 🧰 Troubleshooting

**PowerShell blocks activation**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
# or just:
.\.venv\Scripts\activate.bat
```

**Excel writer error**
Reinstall deps:

```bash
pip install -r requirements.txt
```

**Wrong CSV delimiter**
Change the delimiter in Streamlit sidebar (`;`, `,`, `|`, etc.).

**`ModuleNotFoundError: report_bot`**
Make sure you’re inside the repo folder and the venv is active.

---

## 🗂️ Recommended .gitignore

```gitignore
# Virtual environment
.venv/

# Python cache
__pycache__/
*.pyc

# Streamlit output
output/

# IDE settings
.vscode/
.idea/
```

---

## 🙋 About

Made by **Omar** as a student project to practice **Python, automation, and full-stack fundamentals**.
Feel free to fork, experiment, and improve 🚀

