from app.errors import object_payload
from fastapi import APIRouter, Body
from app.modules.m7_audit.service import execute
router=APIRouter()
@router.post("/api/7")
def calculate(payload:object=Body(default=None)):
    payload=object_payload(payload)
    from app.pipeline import sample_text
    text=payload.get("text",sample_text())
    if not isinstance(text,str):
        from app.errors import BusinessError
        raise BusinessError("TEXT","输入须为文本")
    return execute(text)
@router.get("/api/7")
def sample():
    from app.pipeline import sample_text
    return execute(sample_text())
