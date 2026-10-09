from .text_matcher import calculate_text_similarity
def calculate_attribute_similarity(report1,report2):
 vals=[]
 for field,weight in [('item_name',.5),('category',.3),('color',.2)]:
  a,b=report1.get(field),report2.get(field)
  if a and b:
   score=100.0 if str(a).strip().lower()==str(b).strip().lower() else calculate_text_similarity(str(a),str(b))
   vals.append((score,weight))
 return round(sum(x*w for x,w in vals)/sum(w for _,w in vals),2) if vals else None
