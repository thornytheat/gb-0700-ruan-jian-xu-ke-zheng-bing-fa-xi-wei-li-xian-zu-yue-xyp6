import csv, io
from app.errors import BusinessError
from app.config import MAX_BYTES

def decode(raw):
    if len(raw) > MAX_BYTES:
        raise BusinessError("SIZE", "文件超过2MB", 413)
    for encoding in ("utf-8-sig", "gb18030"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise BusinessError("ENCODING", "无法识别文件编码")

def read_rows(text, fields):
    if not text:
        raise BusinessError("EMPTY_FILE", "文件为空")
    if not text.strip():
        raise BusinessError("BLANK_FILE", "文件只有空行")
    if len(text.encode("utf-8")) > MAX_BYTES:
        raise BusinessError("SIZE", "文件超过2MB", 413)
    rows = csv.reader(io.StringIO(text.lstrip("\ufeff")), strict=True)
    try:
        header = next(rows)
    except StopIteration:
        raise BusinessError("BLANK_FILE", "文件只有空行")
    header = [x.strip() for x in header]
    if set(header) != set(fields) or len(header) != len(fields):
        raise BusinessError("HEADER", "字段不匹配")
    accepted, rejected, blanks = [], [], 0
    try:
        for cells in rows:
            line = rows.line_num
            if not cells or not any(x.strip() for x in cells):
                blanks += 1
                continue
            if cells == header:
                rejected.append({"line":line,"reason":"REPEATED_HEADER","raw":cells})
            elif len(cells) != len(header):
                rejected.append({"line":line,"reason":"COLUMN_COUNT","raw":cells})
            else:
                accepted.append(dict(zip(header, [x.strip() for x in cells]), line=line))
    except csv.Error:
        raise BusinessError("CSV", "引号或换行结构错误")
    if not accepted and not rejected and not blanks:
        raise BusinessError("HEADER_ONLY", "文件只有表头")
    return accepted, rejected, blanks
