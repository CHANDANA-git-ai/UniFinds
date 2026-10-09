"""Orchestrates report comparison, persistence, explanations, and ranking."""
from lost_found_matching.database.db import Database
from .text_matcher import calculate_text_similarity
from .image_matcher import calculate_image_similarity
from .attribute_matcher import calculate_attribute_similarity
from .location_matcher import calculate_location_similarity
from .time_matcher import calculate_time_similarity
from .scoring import score_match,confidence_for
from .ranking import rank_matches
def _description(r): return ' '.join(str(r.get(k) or '') for k in ('item_name','description','category','color')).strip()
def _explain(s,final):
 bits=[]
 if s['image'] is not None and s['image']>=75: bits.append('Images show strong visual similarity')
 if s['text'] is not None and s['text']>=70: bits.append('descriptions are semantically similar')
 if s['attribute'] is not None and s['attribute']>=75: bits.append('item attributes closely match')
 if s['location'] is not None and s['location']>=75: bits.append('reported locations are close')
 if s['time'] is not None and s['time']>=75: bits.append('reported times are close')
 lead='Strong potential match' if final>=80 else 'Potential match' if final>=60 else 'Low-confidence match'
 return lead + (': ' + '; '.join(bits) + '.' if bits else '; available report details have limited similarity.')
class MatchingEngine:
 def __init__(self,db=None): self.db=db or Database()
 def find_matches(self,report_id,top_k=5):
  source=self.db.get_report(report_id)
  if not source: raise ValueError(f'Report {report_id} was not found')
  results=[]
  for candidate in self.db.get_opposite_reports(source['report_type']):
   scores={'image':calculate_image_similarity(source.get('image_path'),candidate.get('image_path')),
    'text':calculate_text_similarity(_description(source),_description(candidate)),
    'attribute':calculate_attribute_similarity(source,candidate), 'location':calculate_location_similarity(source,candidate),
    'time':calculate_time_similarity(source,candidate)}
   final=score_match(scores); confidence=confidence_for(final); explanation=_explain(scores,final)
   lost,found=(source,candidate) if source['report_type']=='LOST' else (candidate,source)
   self.db.upsert_match(lost_report_id=lost['id'],found_report_id=found['id'],image_score=scores['image'],text_score=scores['text'],attribute_score=scores['attribute'],location_score=scores['location'],time_score=scores['time'],final_score=final,confidence=confidence,explanation=explanation)
   results.append({'report_id':candidate['id'],'item_name':candidate['item_name'],'image_score':scores['image'],'text_score':scores['text'],'attribute_score':scores['attribute'],'location_score':scores['location'],'time_score':scores['time'],'final_score':final,'confidence':confidence,'explanation':explanation})
  return rank_matches(results,top_k)
def find_matches(report_id,top_k=5): return MatchingEngine().find_matches(report_id,top_k)
