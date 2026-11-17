# TRAP-11
from app.modules.m2_products.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_product_alias():
    assert product("CAD-Pro")==product("cad")

def test_product_unknown():
    with pytest.raises(BusinessError):product("unknown")

def test_product_fraction():
    with pytest.raises(BusinessError):seats("1.5")

def test_product_timezone():
    assert instant("2026-11-18T08:00:00+08:00")==instant("2026-11-18T00:00:00Z")

def test_product_sample(result):
    assert len(result["normalized"])==43

def test_product_missing(result):
    assert any(r["reason"]=="MISSING" for r in result["quarantine"])

def test_product_fullwidth():
    assert seats("２")==2