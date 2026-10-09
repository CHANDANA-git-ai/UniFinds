from datetime import datetime
def _parse(r):
 date=r.get('event_date'); time=r.get('event_time') or '00:00:00'
 if not date:return None
 for pattern in ('%Y-%m-%d %H:%M:%S','%Y-%m-%d %H:%M','%Y-%m-%d %I:%M %p'):
  try:return datetime.strptime(f'{date} {time}',pattern)
  except ValueError:pass
 return None
def calculate_time_similarity(report1,report2,zero_score_hours=168):
 a,b=_parse(report1),_parse(report2)
 if not a or not b:return None
 return round(max(0,100*(1-abs((a-b).total_seconds())/3600/zero_score_hours)),2)
