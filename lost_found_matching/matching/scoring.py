WEIGHTS={'image':.40,'text':.25,'attribute':.15,'location':.15,'time':.05}
def score_match(scores,weights=WEIGHTS):
 usable={k:float(v) for k,v in scores.items() if v is not None and k in weights}
 if not usable:return 0.0
 total=sum(weights[k] for k in usable)
 return round(sum(usable[k]*weights[k] for k in usable)/total,2)
def confidence_for(score,high=80,medium=60): return 'HIGH' if score>=high else 'MEDIUM' if score>=medium else 'LOW'
