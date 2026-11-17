# TRAP-23
# TRAP-13
from app.modules.m4_concurrency.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_sweep_boundary():
    assert max(r["count"] for r in sweep([{"a":0,"b":10,"quantity":1,"lease_id":"a"},{"a":10,"b":20,"quantity":1,"lease_id":"b"}]))==1

def test_sweep_overlap():
    assert max(r["count"] for r in sweep([{"a":0,"b":11,"quantity":1,"lease_id":"a"},{"a":10,"b":20,"quantity":1,"lease_id":"b"}]))==2

def test_sweep_quantity():
    assert sweep([{"a":0,"b":10,"quantity":3,"lease_id":"a"}])[0]["count"]==3

def test_sweep_empty():
    assert sweep([])==[]

def test_sweep_sample_peak(result):
    assert max(r["count"] for r in result["segments"])==20

def test_sweep_sample_sorted(result):
    assert result["segments"][0]["ids"]==["00001"]

def test_sweep_sample_last(result):
    assert result["segments"][-1]["count"]==1