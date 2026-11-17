import pytest
from app.errors import BusinessError
from app.reader import read_rows

def test_whitespace_file_is_distinct():
    with pytest.raises(BusinessError) as caught:
        read_rows("\n\r\n",["id"])
    assert caught.value.code=="BLANK_FILE"

def test_large_text_rejected_before_parse():
    with pytest.raises(BusinessError) as caught:
        read_rows("id\n"+"x"*2_000_001,["id"])
    assert caught.value.status==413
