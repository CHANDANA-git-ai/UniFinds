import logging
from pathlib import Path
import numpy as np
log=logging.getLogger(__name__); _model=_processor=None; _failed=False
def _get_model():
 global _model,_processor,_failed
 if _model is None and not _failed:
  try:
   from transformers import CLIPModel, CLIPProcessor
   _model=CLIPModel.from_pretrained('openai/clip-vit-base-patch32'); _processor=CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')
  except Exception as e: _failed=True; log.warning('CLIP unavailable: %s',e)
 return _model,_processor
def calculate_image_similarity(image1_path, image2_path):
 if not image1_path or not image2_path or not Path(image1_path).is_file() or not Path(image2_path).is_file(): return None
 try:
  from PIL import Image
  import torch
  model,processor=_get_model()
  if not model: return None
  images=[Image.open(image1_path).convert('RGB'),Image.open(image2_path).convert('RGB')]
  with torch.no_grad(): features=model.get_image_features(**processor(images=images,return_tensors='pt'))
  features=features/features.norm(dim=-1,keepdim=True)
  return round(float(torch.clamp((features[0]*features[1]).sum(),0,1)*100),2)
 except Exception as e: log.warning('Could not compare images: %s',e); return None
