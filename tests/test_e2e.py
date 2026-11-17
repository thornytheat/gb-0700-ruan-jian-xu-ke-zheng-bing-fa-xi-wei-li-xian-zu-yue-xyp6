from app.pipeline import run,sample_text
from app import store
from app.errors import BusinessError
from app.exporter import evidence_csv
import pytest

def test_pipeline_balance():
    r=run(sample_text())
    assert r["balance"]["input"] == r["balance"]["accepted"]+r["balance"]["quarantined"]+r["balance"]["blank"]

def test_persistent_idempotence():
    a=store.save(sample_text(),run(sample_text()));b=store.save(sample_text(),run(sample_text()))
    assert a["id"]==b["id"] and a["digest"]==b["digest"]

def test_optimistic_review_rejects_stale():
    a=store.save(sample_text()+"\n",run(sample_text()+"\n"))
    store.review(a["id"],a["revision"],"退回")
    with pytest.raises(BusinessError,match="版本已更新"):
        store.review(a["id"],a["revision"],"退回")

def test_evidence_has_hash_and_quarantine():
    a=store.save(sample_text(),run(sample_text()));text=evidence_csv(a)
    assert a["digest"] in text and "quarantine" in text
