from datetime import datetime,timezone
from decimal import Decimal
from app.errors import BusinessError

def instant(text):
    try:dt=datetime.fromisoformat(text.replace("Z","+00:00"))
    except ValueError:raise BusinessError("TIME","时间格式错误")
    if dt.tzinfo is None:raise BusinessError("TIMEZONE","时间须含时区")
    return Decimal(str(dt.timestamp()))

def display(t):return datetime.fromtimestamp(float(t),timezone.utc).strftime("%m-%d %H:%M UTC")

def display_full(seconds):
    if seconds is None:return "—"
    return datetime.fromtimestamp(float(seconds),timezone.utc).strftime("%Y-%m-%d %H:%M")
