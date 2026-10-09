from lost_found_matching.matching.attribute_matcher import calculate_attribute_similarity
from lost_found_matching.matching.location_matcher import calculate_location_similarity
from lost_found_matching.matching.time_matcher import calculate_time_similarity
from lost_found_matching.matching.scoring import score_match,confidence_for
from lost_found_matching.matching.ranking import rank_matches
def test_structured_matchers():
 a={'item_name':'Black Wallet','category':'Wallet','color':'Black','latitude':12.9716,'longitude':77.5946,'event_date':'2026-08-17','event_time':'18:00'}
 b={**a,'latitude':12.975,'longitude':77.599,'event_time':'19:00'}
 assert calculate_attribute_similarity(a,b)==100; assert calculate_location_similarity(a,b)>90; assert calculate_time_similarity(a,b)>99
def test_normalized_score_and_ranking():
 assert score_match({'image':None,'text':100,'attribute':100,'location':100,'time':100})==100
 assert confidence_for(80)=='HIGH' and confidence_for(60)=='MEDIUM'
 assert [x['final_score'] for x in rank_matches([{'final_score':10},{'final_score':90}])]==[90,10]
