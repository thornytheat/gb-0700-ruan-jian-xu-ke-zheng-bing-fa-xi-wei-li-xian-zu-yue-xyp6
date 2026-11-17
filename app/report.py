from collections import Counter
from decimal import Decimal

def plain(value):
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {str(k):plain(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)):
        return [plain(v) for v in value]
    return value

def report(rows, **metrics):
    return {"rows":plain(rows), "metrics":plain(metrics)}

def quarantine(ctx, row, reason):
    ctx["quarantine"].append({"line":row.get("line",0),"id":row.get("id",row.get("sample_id","")),"reason":reason,"raw":plain(row)})

def reason_counts(ctx):
    return dict(Counter(x["reason"] for x in ctx["quarantine"]))
