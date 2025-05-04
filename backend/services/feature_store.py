"""
This module handles feature extraction for fashion images using a locally loaded
CLIP model. It provides functions to:
    - Extract image embeddings
    - Cache/load features for faster startup
    - Traverse a directory of background-removed images and compute embeddings
"""
import os
import numpy as np
import pickle
from PIL import Image
from core.config import *
from core.clip_model import model, processor, device
import torch

def save_features_and_paths(features, paths):
    """
    Saves extracted features and corresponding image paths to disk.

    Args:
        features (np.ndarray): Feature matrix of shape (N, D)
        paths (list[str]): List of image file paths
    """    
    np.save(FEATURE_PATH, features)
    with open(PATHS_PATH, 'wb') as f:
        pickle.dump(paths, f)

def load_features_and_paths():
    """
    Loads previously saved features and paths from disk.

    Returns:
        Tuple of:
            - features (np.ndarray): Feature matrix of shape (N, D)
            - paths (list[str]): List of image file paths
    """
    features = np.load(FEATURE_PATH)
    with open(PATHS_PATH, 'rb') as f:
        paths = pickle.load(f)
    return features, paths

def extract_image_features(image_path):
    """
    Extracts normalized CLIP image features for a given image.

    Args:
        image_path (str): Path to the input image

    Returns:
        np.ndarray: Normalized feature vector of shape (1, D),
        
    """
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
    return (outputs / outputs.norm(p=2, dim=-1, keepdim=True)).cpu().numpy()

def compute_or_load_features():
    """
    Computes or loads all CLIP features for images in the BACKGROUND_REMOVED_DIR.
    Traverses the directory recursively by brand, extracts features, and saves them.

    Returns:
        Tuple of:
            - features (np.ndarray): Feature matrix of shape (N, D)
            - paths (list[str]): List of image file paths corresponding to each feature
    """
    
    # Load cached features if they already exist
    if os.path.exists(FEATURE_PATH) and os.path.exists(PATHS_PATH):
        return load_features_and_paths()

    all_features, all_paths = [], []
    for brand in os.listdir(BACKGROUND_REMOVED_DIR):
        brand_path = os.path.join(BACKGROUND_REMOVED_DIR, brand)
        if not os.path.isdir(brand_path): continue
        for img_file in os.listdir(brand_path):
            if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                img_path = os.path.join(brand_path, img_file)
                try:
                    feat = extract_image_features(img_path)
                    all_features.append(feat)
                    all_paths.append(img_path)
                except Exception as e:
                    print(f"Error processing {img_path}: {e}")

    features_np = np.vstack(all_features)
    save_features_and_paths(features_np, all_paths)
    return features_np, all_paths
