from app.modules.m3_leases.rules import *
from app.errors import BusinessError
from app.numbers import number
from decimal import Decimal
import pytest

def test_lease_online_release():
    assert close_time("online",0,100,[30])==30

def test_lease_offline():
    assert close_time("offline",0,100,[30])==100

def test_lease_prior_release():
    assert close_time("online",10,100,[5])==100

def test_lease_end_equal():
    assert close_time("online",0,100,[100])==100

def test_lease_sample(result):
    assert len(result["leases"])==20

def test_lease_heartbeats(result):
    assert sum(r["reason"]=="HEARTBEAT_NO_SEAT" for r in result["lease_audit"])==20

def test_lease_offline_audit(result):
    assert sum(r["reason"]=="OFFLINE_UNTIL_EXPIRY" for r in result["lease_audit"])==1
def test_release_at_lease_start_frees_online():
    assert close_time('online',0,100,[0])==0
    assert close_time('offline',0,100,[0])==100

def test_same_lease_id_different_products_kept(sample):
    from app.pipeline import run
    extra='\n'.join(line.replace(',CAD-Pro,',',Render,').replace(',cad,',',Render,').replace(',CAD,',',Render,') for line in sample.splitlines()[1:] if ',CAD' in line or ',cad,' in line)
    r=run(sample+'\n'+extra+'\n')
    assert len(r['leases'])==40
    assert {x['canonical'] for x in r['leases']}=={'CAD','RENDER'}
