"""Idempotently populate useful text-only hackathon demonstration reports."""
from services.report_service import ReportService
def seed(service=None):
 s=service or ReportService()
 if s.get_all_reports(): return s.get_all_reports()
 rows=[
 {'report_type':'LOST','item_name':'Black Leather Wallet','description':'Black leather wallet containing college ID','category':'Wallet','color':'Black','location_name':'Bangalore','latitude':12.9716,'longitude':77.5946,'event_date':'2026-08-17','event_time':'18:00'},
 {'report_type':'FOUND','item_name':'Black Leather Wallet','description':'Black leather wallet with a student identification card','category':'Wallet','color':'Black','location_name':'Bangalore','latitude':12.9750,'longitude':77.5990,'event_date':'2026-08-17','event_time':'19:00'},
 {'report_type':'FOUND','item_name':'Black Leather Wallet','description':'Wallet found near metro station','category':'Wallet','color':'Black','location_name':'Mysore','latitude':12.2958,'longitude':76.6394,'event_date':'2026-08-17','event_time':'19:00'},
 {'report_type':'FOUND','item_name':'Blue Backpack','description':'Blue school bag with notebooks','category':'Bag','color':'Blue','location_name':'Bangalore','latitude':12.9718,'longitude':77.5949,'event_date':'2026-08-17','event_time':'18:30'},
 {'report_type':'FOUND','item_name':'Brown Wallet','description':'Leather wallet containing cards','category':'Wallet','color':'Brown','location_name':'Bangalore','event_date':'2026-08-18','event_time':'10:00'},
 {'report_type':'FOUND','item_name':'Blue Water Bottle','description':'Metal water bottle left in cafeteria','category':'Bottle','color':'Blue','location_name':'Bangalore','latitude':12.9716,'longitude':77.5946,'event_date':'2026-08-25','event_time':'11:00'},
 {'report_type':'LOST','item_name':'Silver Keys','description':'Three silver house keys on a red keyring','category':'Keys','color':'Silver','location_name':'Bangalore','event_date':'2026-08-18'},
 {'report_type':'FOUND','item_name':'Silver House Keys','description':'Set of three keys with red key ring','category':'Keys','color':'Silver','location_name':'Bangalore','event_date':'2026-08-18'},]
 for row in rows:s.create_report(**row)
 return s.get_all_reports()
if __name__=='__main__': print(f'Seeded {len(seed())} reports.')
