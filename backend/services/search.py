"""
This module handles text-to-image search using CLIP and FAISS.

Workflow:
    - Loads or computes image features using the CLIP model
    - Creates a FAISS index for fast similarity search
    - Allows querying with natural language to retrieve visually similar images

"""
import faiss
from core.clip_model import model, processor, device
from core.config import BACKGROUND_REMOVED_DIR, ORIGINAL_IMAGE_DIR
from services.feature_store import compute_or_load_features
import torch

# Load precomputed or freshly computed image features and their corresponding file paths
features_np, paths = compute_or_load_features()

# Initialize a FAISS index for L2 (Euclidean) similarity search
# The dimensionality must match the CLIP model's output embedding size
index = faiss.IndexFlatL2(model.config.projection_dim)

# Add image feature vectors to the FAISS index
index.add(features_np)

def search_images(query: str, top_k: int):
    """
    Searches for the top-K most visually similar images to a text query.

    Args:
        query (str): Natural language search query (e.g., "red dress with ruffles")
        top_k (int): Number of top results to return

    Returns:
        list[str]: List of URLs pointing to the original (non-background-removed) image files
    """
    # Tokenize and encode the query using CLIP's text encoder
    inputs = processor(text=query, return_tensors="pt").to(device)

    with torch.no_grad():
        text_features = model.get_text_features(**inputs)
    # Normalize the text feature vector to unit length (L2 norm)
    text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)

    # Perform nearest-neighbor search using FAISS
    D, I = index.search(text_features.cpu().numpy(), k=top_k)
    results = []
    for idx in I[0]:
        # Replace background-removed image path with original image path
        rel_path = paths[idx].replace(BACKGROUND_REMOVED_DIR, ORIGINAL_IMAGE_DIR).replace("\\", "/")
        if rel_path.startswith("/"):
            rel_path = rel_path[1:]
        results.append(f"http://127.0.0.1:8000/{rel_path}")
    return results