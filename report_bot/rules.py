from typing import Dict, List

DEFAULT_CATEGORY_RULES: Dict[str, List[str]] = {
    "Salary": ["payroll", "salary", "paycheque", "direct deposit"],
    "Rent": ["rent", "landlord"],
    "Groceries": ["grocery", "supermarket", "metro", "loblaws", "sobeys", "no frills", "food basics"],
    "Restaurants": ["restaurant", "cafe", "coffee", "starbucks", "tim hortons", "ubereats"],
    "Transport": ["uber", "lyft", "subway", "metro pass", "ttc", "go transit", "gas", "petro", "esso"],
    "Utilities": ["hydro", "electric", "water", "internet", "rogers", "bell", "telus"],
    "Entertainment": ["netflix", "spotify", "movie", "cinema", "game", "concert"],
    "Fees": ["fee", "service charge", "atm fee", "bank charge"],
    "Transfer": ["etransfer", "e-transfer", "interac", "transfer"],
    "Other": [],
}

def normalize_type(amount: float, tx_type: str | None) -> str:
    if tx_type:
        return str(tx_type).strip().upper()
    return "EXPENSE" if amount < 0 else "INCOME"

def categorize_description(description: str, rules: dict[str, list[str]] | None = None) -> str:
    if not rules:
        rules = DEFAULT_CATEGORY_RULES
    desc = (description or "").lower()
    for category, keywords in rules.items():
        for kw in keywords:
            if kw.lower() in desc:
                return category
    return "Other"
