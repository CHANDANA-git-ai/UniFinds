import tempfile
from pathlib import Path
from lost_found_matching.database.db import Database
def db(): return Database(Path(tempfile.mkdtemp())/'test.db')
def test_create_retrieve_and_status():
 d=db(); id=d.create_report(report_type='LOST',item_name='Phone',status='ACTIVE')
 assert d.get_report(id)['item_name']=='Phone'; assert d.update_report_status(id,'CLOSED'); assert d.get_report(id)['status']=='CLOSED'
def test_opposite_active_filtering():
 d=db(); d.create_report(report_type='LOST',item_name='A'); active=d.create_report(report_type='FOUND',item_name='B'); d.create_report(report_type='FOUND',item_name='C',status='CLOSED')
 assert [r['id'] for r in d.get_opposite_reports('LOST')]==[active]
