from app.report import report

def sweep(leases):
    points=sorted({r[k] for r in leases for k in ("a","b")});out=[]
    for a,b in zip(points,points[1:]):
        active=[r for r in leases if r["a"]<=a<r["b"]]
        if active:out.append({"a":a,"b":b,"count":sum(r["quantity"] for r in active),"ids":sorted(r["lease_id"] for r in active)})
    return out

def apply(ctx):
    out=[]
    for product in sorted({r["canonical"] for r in ctx["leases"]}):
        for r in sweep([r for r in ctx["leases"] if r["canonical"]==product]):out.append(dict(r,product=product))
    ctx["segments"]=out;return report(out,峰值=max((r["count"] for r in out),default=0),区间=len(out))
