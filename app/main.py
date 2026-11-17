from fastapi import FastAPI, Body, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.errors import BusinessError, object_payload
from app.pipeline import run, sample_text
from app import store
from app.exporter import evidence_csv
from app.timeops import display_full
from app.numbers import display_number
from pathlib import Path
import importlib
app=FastAPI(title='软件许可证并发席位与离线租约')
app.mount("/static",StaticFiles(directory=Path(__file__).parent/"static"),name="static")
templates=Jinja2Templates(directory=Path(__file__).parent/"templates")
templates.env.filters["utc_instant"]=display_full
templates.env.filters["display_number"]=display_number
MODULES=['会话接收', '产品映射', '租约裁决', '并发扫描', '超用归属', '采购对照', '补传审计']
for n,slug in enumerate(['sessions', 'products', 'leases', 'concurrency', 'excess', 'purchase', 'audit'],1):
    app.include_router(importlib.import_module(f"app.modules.m{n}_{slug}.handler").router)
@app.exception_handler(BusinessError)
async def domain_error(request,exc):
    return JSONResponse({"error":exc.code,"message":str(exc)},status_code=exc.status)
@app.get("/health")
def health(): return {"status":"ok"}
@app.get("/",response_class=HTMLResponse)
def home(request:Request): return page(request,1)
@app.get("/module/{module}",response_class=HTMLResponse)
def page(request:Request,module:int):
    if module not in range(1,8): raise BusinessError("MODULE","模块不存在",404)
    ident=request.query_params.get("run_id")
    item=store.get(ident) if ident else store.save(sample_text(),run(sample_text()))
    return templates.TemplateResponse(request=request,name="workbench.html",context={"title":'软件许可证并发席位与离线租约',"modules":MODULES,"active":module,"run":item,"report":item["result"]["reports"][module-1]})
@app.post("/api/run")
def calculate(payload:object=Body(default=None)):
    payload=object_payload(payload)
    text=payload.get("text",sample_text())
    if not isinstance(text,str): raise BusinessError("TEXT","输入须为文本")
    return store.save(text,run(text))
@app.get("/api/runs")
def list_runs(): return store.history()
@app.get("/api/runs/{ident}")
def run_detail(ident:str): return store.get(ident)
@app.post("/api/review")
def review(payload:object=Body(...)):
    payload=object_payload(payload)
    if not isinstance(payload.get("id"),str) or not isinstance(payload.get("decision"),str): raise BusinessError("REVIEW","复核编号与决定须为文本")
    if type(payload.get("revision")) is not int: raise BusinessError("REVISION","版本须为整数")
    return store.review(str(payload.get("id","")),payload["revision"],payload.get("decision"))
@app.get("/api/export/{ident}")
def export(ident:str):
    return Response(evidence_csv(store.get(ident)),media_type="text/csv",headers={"Content-Disposition":"attachment; filename=evidence.csv"})
@app.get("/api/sample")
def sample(): return {"text":sample_text()}
