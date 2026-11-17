# TRAP-14
# TRAP-08
# TRAP-02
from app.modules.m1_sessions.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_sessions_sample(result):
    assert len(result["raw"])==45

def test_sessions_bom(sample):
    from app.reader import read_rows
    rows,_,_=read_rows("\ufeff"+sample,FIELDS)
    assert rows[0]["lease_id"]=="CAP01"

def test_sessions_duplicate(result):
    assert any(r["reason"]=="DUPLICATE_EVENT" for r in result["quarantine"])

def test_sessions_shape(result):
    assert any(r["reason"]=="COLUMN_COUNT" for r in result["quarantine"])

def test_sessions_empty():
    with pytest.raises(BusinessError):read_rows("",FIELDS)

def test_sessions_header():
    with pytest.raises(BusinessError):read_rows(",".join(FIELDS),FIELDS)

def test_sessions_id(result):
    assert any(r["lease_id"]=="00001" for r in result["raw"])