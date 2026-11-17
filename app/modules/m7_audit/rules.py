from app.report import report
from app.timeops import display

def reject_stale(current,proposed):
    if proposed<=current:raise ValueError("补传版本须递增")
    return proposed

def apply(ctx):
    ctx["final"]=[dict(r,start=display(r["a"]),end=display(r["b"])) for r in ctx["usage"] if r["status"]!="PASS"]
    ctx["blocked"]=bool(ctx["final"])
    return report(ctx["lease_audit"],忽略心跳=sum(r["reason"]=="HEARTBEAT_NO_SEAT" for r in ctx["lease_audit"]),离线释放保留=sum(r["reason"]=="OFFLINE_UNTIL_EXPIRY" for r in ctx["lease_audit"]))
