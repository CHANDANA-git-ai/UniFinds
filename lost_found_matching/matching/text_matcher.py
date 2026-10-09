"""Semantic text similarity with a TF-IDF fallback when offline."""
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
log=logging.getLogger(__name__); _model=None; _failed=False
def _get_model():
 global _model,_failed
 if _model is None and not _failed:
  try:
   from sentence_transformers import SentenceTransformer
   _model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
  except Exception as e: _failed=True; log.warning('Semantic model unavailable; using TF-IDF: %s',e)
 return _model
def calculate_text_similarity(text1, text2):
 if not (text1 and text2): return None
 model=_get_model()
 if model:
  embeds=model.encode([text1,text2],normalize_embeddings=True)
  return round(float(np.clip(np.dot(embeds[0],embeds[1]),0,1)*100),2)
 matrix=TfidfVectorizer(ngram_range=(1,2),stop_words='english').fit_transform([text1,text2])
 return round(float(max(0,cosine_similarity(matrix[0],matrix[1])[0,0])*100),2)
