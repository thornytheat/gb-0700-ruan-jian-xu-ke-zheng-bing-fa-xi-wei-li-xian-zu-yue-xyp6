from app.modules.m6_purchase.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_purchase_decimal():
    assert seat_hours([{"a":Decimal(0),"b":Decimal(3600),"excess":2}])==2

def test_purchase_partial():
    assert seat_hours([{"a":Decimal(0),"b":Decimal(1800),"excess":1}])==Decimal("0.5")

def test_purchase_zero():
    assert seat_hours([])==0

def test_purchase_conserve():
    assert seat_hours([{"a":Decimal(0),"b":Decimal(1800),"excess":2},{"a":Decimal(1800),"b":Decimal(3600),"excess":2}])==2

def test_purchase_sample(result):
    assert result["purchase"][0]["peak"]==20

def test_purchase_balance(result):
    assert result["balance"]=={"input":48,"accepted":43,"quarantined":4,"blank":1}

def test_purchase_single(result):
    assert len(result["purchase"])==1