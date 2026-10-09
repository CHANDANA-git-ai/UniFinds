from lost_found_matching.database.db import Database
from lost_found_matching.seed_demo_data import seed
from lost_found_matching.matching.engine import MatchingEngine
def main():
 db=Database(); reports=seed(); source=next(r for r in reports if r['report_type']=='LOST' and 'Wallet' in r['item_name'])
 print('\nAI LOST & FOUND MATCHING\n'+'='*40+f"\nSearching matches for: {source['item_name']}\n")
 for i,m in enumerate(MatchingEngine(db).find_matches(source['id']),1):
  print(f"MATCH #{i}: {m['item_name']} | {m['final_score']:.2f}% ({m['confidence']})")
  print('  '+', '.join(f'{k.title()}: {v:.2f}%' for k,v in m.items() if k.endswith('_score') and v is not None))
  print('  Why: '+m['explanation']+'\n')
if __name__=='__main__':main()
