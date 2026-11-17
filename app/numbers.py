from decimal import Decimal, InvalidOperation
import unicodedata
from app.errors import BusinessError
SENTINELS = {"", "-", "N/A", "NULL", "未知"}
def number(value):
    text = unicodedata.normalize("NFKC", str(value)).strip().replace(",", "")
    if text.upper() in SENTINELS or text in SENTINELS:
        raise BusinessError("MISSING", "数值缺失")
    try:
        value = Decimal(text)
    except InvalidOperation:
        raise BusinessError("NUMBER", "数值格式错误")
    if not value.is_finite():
        raise BusinessError("NUMBER", "数值必须有限")
    return value
def fmt(value, places=4):
    return format(value.quantize(Decimal(10) ** -places), "f")

def display_number(value):
    if value is None:return "—"
    try:decimal=Decimal(str(value))
    except InvalidOperation:return str(value)
    if not decimal.is_finite():return str(value)
    text=format(decimal,".6f").rstrip("0").rstrip(".")
    return "0" if decimal.is_zero() or text=="-0" else text
