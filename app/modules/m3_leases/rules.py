from app.report import report,quarantine

def close_time(kind,start,end,releases):
    if kind=="offline":return end
    times=[t for t in releases if start<=t<end]
    return min(times) if times else end

def apply(ctx):
    chosen={};audit=[]
    for r in ctx["normalized"]:
        if r["kind"] not in {"online","offline"}:continue
        key=(r["canonical"],r["lease_id"])
        if key not in chosen or r["rev"]>chosen[key]["rev"]:
            if key in chosen:audit.append({"id":chosen[key]["lease_id"],"reason":"SUPERSEDED"})
            chosen[key]=r
        elif r["rev"]==chosen[key]["rev"]:
            quarantine(ctx,r,"LEASE_CONFLICT")
        else:audit.append({"id":r["lease_id"],"reason":"SUPERSEDED"})
    out=[]
    for key,r in chosen.items():
        releases=[x["a"] for x in ctx["normalized"] if x["kind"]=="release" and x["canonical"]==key[0] and x["lease_id"]==key[1] and x["rev"]==r["rev"]]
        x=dict(r);x["b"]=close_time(r["kind"],r["a"],r["b"],releases);out.append(x)
        if r["kind"]=="offline" and releases:audit.append({"id":r["lease_id"],"reason":"OFFLINE_UNTIL_EXPIRY"})
    for r in ctx["normalized"]:
        if r["kind"]=="heartbeat":audit.append({"id":r["lease_id"],"reason":"HEARTBEAT_NO_SEAT"})
    ctx["leases"]=out;ctx["lease_audit"]=audit
    return report(out,在线=sum(r["kind"]=="online" for r in out),离线=sum(r["kind"]=="offline" for r in out))
