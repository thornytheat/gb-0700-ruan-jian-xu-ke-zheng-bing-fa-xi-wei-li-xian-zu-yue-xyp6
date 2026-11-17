from app.reader import read_rows
from app.report import report,quarantine
FIELDS="lease_id product user start end kind version seats".split()
def apply(ctx):
    rows,bad,blank=read_rows(ctx["text"],FIELDS);ctx["quarantine"].extend(bad);ctx["blank_rows"]=blank;ctx["input_count"]=len(rows)+len(bad)+blank
    out=[];seen=set()
    for r in rows:
        key=(r["product"],r["lease_id"],r["kind"],r["version"],r["start"])
        if not r["lease_id"]:quarantine(ctx,r,"ID_REQUIRED");continue
        if key in seen:quarantine(ctx,r,"DUPLICATE_EVENT");continue
        seen.add(key);out.append(r)
    ctx["raw"]=out;return report(out,会话事件=len(out),隔离=len(ctx["quarantine"]))
