from decimal import Decimal
from app.report import report

def seat_hours(rows):
    return sum((r["b"]-r["a"])*r["excess"]/Decimal(3600) for r in rows)

def apply(ctx):
    out=[]
    for p in sorted({r["product"] for r in ctx["usage"]}):
        rows=[r for r in ctx["usage"] if r["product"]==p]
        out.append({"product":p,"peak":max(r["concurrent"] for r in rows),"excess_seat_hours":seat_hours(rows),"overuse_segments":sum(r["excess"]>0 for r in rows)})
    ctx["purchase"]=out;ctx["balance"]={"input":ctx["input_count"],"accepted":ctx["input_count"]-len(ctx["quarantine"])-ctx["blank_rows"],"quarantined":len(ctx["quarantine"]),"blank":ctx["blank_rows"]}
    return report(out,产品=len(out),超用席位小时=seat_hours(ctx["usage"]))
