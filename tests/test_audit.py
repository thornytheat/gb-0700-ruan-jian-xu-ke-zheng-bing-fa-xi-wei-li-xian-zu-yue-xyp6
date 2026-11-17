# TRAP-26
from app.modules.m7_audit.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_audit_stale():
    with pytest.raises(ValueError):reject_stale(2,2)

def test_audit_backward():
    with pytest.raises(ValueError):reject_stale(2,1)

def test_audit_increment():
    assert reject_stale(2,3)==3

def test_audit_display():
    assert display(Decimal(0))=="01-01 00:00 UTC"

def test_audit_sample(result):
    assert result["blocked"] is True

def test_audit_final(result):
    assert len(result["final"])>0

def test_audit_time(result):
    assert all(r["start"].endswith("UTC") for r in result["final"])