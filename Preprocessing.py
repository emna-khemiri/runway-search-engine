""" Preprocessing script to remove the background from images """

import os
from PIL import Image
from transformers import pipeline


def init_pipeline():
    """Initialize the BRIA RMBG image segmentation pipeline."""
    return pipeline(
        "image-segmentation",
        model="briaai/RMBG-1.4",
        trust_remote_code=True
    )


def remove_background_and_save(pipe, image_path: str, save_path: str):
    """Apply background removal and save the result."""
    try:
        result_image = pipe(image_path)
        result_image.save(save_path)
        print(f"Saved: {save_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")


def process_folder(pipe, input_dir: str, output_dir: str):
    """
    Process all images in `input_dir` and save background-removed results to `output_dir`,
    preserving folder structure.
    """
    for brand in os.listdir(input_dir):
        brand_path = os.path.join(input_dir, brand)
        if not os.path.isdir(brand_path) or brand.startswith('.'):
            continue

        output_brand_path = os.path.join(output_dir, brand)
        os.makedirs(output_brand_path, exist_ok=True)

        for filename in os.listdir(brand_path):
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            input_path = os.path.join(brand_path, filename)
            output_path = os.path.join(output_brand_path, filename)

            remove_background_and_save(pipe, input_path, output_path)


if __name__ == "__main__":
    INPUT_DIR = "data/fw25_resized"   # Input images with folder structure
    OUTPUT_DIR = "data/fw25-jpg"      # Output for background-removed images

    pipe = init_pipeline()
    process_folder(pipe, INPUT_DIR, OUTPUT_DIR)
