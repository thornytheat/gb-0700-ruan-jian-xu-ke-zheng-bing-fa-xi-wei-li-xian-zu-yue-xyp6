# TRAP-19
from app.modules.m5_excess.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_excess_capacity_boundary():
    assert capacity_at([{"a":0,"b":10,"rev":1,"quantity":3}],10)==(0,False)

def test_excess_capacity_version():
    assert capacity_at([{"a":0,"b":10,"rev":1,"quantity":3},{"a":0,"b":10,"rev":2,"quantity":5}],1)==(5,False)

def test_excess_capacity_conflict():
    assert capacity_at([{"a":0,"b":10,"rev":1,"quantity":3},{"a":0,"b":10,"rev":1,"quantity":5}],1)==(3,True)

def test_excess_latest_user():
    assert allocate_excess([{"a":0,"lease_id":"a","user":"u1","quantity":1},{"a":1,"lease_id":"b","user":"u2","quantity":1}],1)[0]["user"]=="u2"

def test_excess_sample(result):
    assert any(r["status"]=="OVERUSE" for r in result["usage"])

def test_excess_sample_peak(result):
    assert max(r["excess"] for r in result["usage"])==8

def test_excess_accounted(result):
    assert all(sum(x["seats"] for x in r["offenders"])==r["excess"] for r in result["usage"])