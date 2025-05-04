"""
CLIP Model Loader Script
------------------------
This script loads the pre-trained CLIP ViT-L/14 model from a local directory
and sets it up for use with GPU (if available) or CPU.

Model: CLIP-ViT-L-14-laion2B-s32B-b82K
Source: https://huggingface.co/laion/CLIP-ViT-L-14-laion2B-s32B-b82K
"""

import torch
from transformers import CLIPProcessor, CLIPModel

device = "cuda" if torch.cuda.is_available() else "cpu"

model = CLIPModel.from_pretrained("./CLIP-ViT-L-14-laion2B-s32B-b82K").to(device)
processor = CLIPProcessor.from_pretrained("./CLIP-ViT-L-14-laion2B-s32B-b82K")