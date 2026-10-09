import math
def haversine_km(lat1,lon1,lat2,lon2):
 r=6371.0088; p1,p2=math.radians(lat1),math.radians(lat2); dp=math.radians(lat2-lat1); dl=math.radians(lon2-lon1)
 a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
 return 2*r*math.asin(math.sqrt(a))
def calculate_location_similarity(report1,report2,zero_score_distance_km=50):
 coords=[report1.get('latitude'),report1.get('longitude'),report2.get('latitude'),report2.get('longitude')]
 if all(x is not None for x in coords): return round(max(0,100*(1-haversine_km(*coords)/zero_score_distance_km)),2)
 a,b=report1.get('location_name'),report2.get('location_name')
 if a and b: return 100.0 if str(a).strip().lower()==str(b).strip().lower() else 0.0
 return None
