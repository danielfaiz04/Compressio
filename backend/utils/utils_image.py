import os
from PIL import Image
import logging
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def optimize_image_webp(input_path: str, output_path: str, quality: int = 80) -> str:
    """
    Optimizes an image by converting it to WebP format.
    """
    try:
        with Image.open(input_path) as img:
            img.save(output_path, "webp", quality=quality)
        logging.info(f"Optimized image to WebP: {input_path} -> {output_path} (quality: {quality})")
        return output_path
    except Exception as e:
        logging.error(f"Error optimizing image {input_path} to WebP: {e}", exc_info=True)
        raise

def compare_images(image1_path: str, image2_path: str) -> tuple[float, float, float]:
    """
    Compares two images using PSNR and SSIM metrics.
    Returns (similarity_score, psnr_value, ssim_value).
    similarity_score is a simple average/combination, higher is better.
    """
    try:
        img1 = Image.open(image1_path).convert('L') # Convert to grayscale for metrics
        img2 = Image.open(image2_path).convert('L')

        # Resize img2 to match img1 if dimensions differ
        if img1.size != img2.size:
            logging.warning(f"Image dimensions mismatch. Resizing {image2_path} from {img2.size} to {img1.size}.")
            img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)

        img1_np = np.array(img1)
        img2_np = np.array(img2)

        # Calculate PSNR (Peak Signal-to-Noise Ratio)
        # Data range is for 8-bit grayscale images (0-255)
        psnr_val = psnr(img1_np, img2_np, data_range=255)

        # Calculate SSIM (Structural Similarity Index)
        ssim_val = ssim(img1_np, img2_np, data_range=255, multichannel=False)

        # Simple combined similarity score (can be refined)
        similarity_score = (psnr_val / 100) + ssim_val # Normalize PSNR to a similar scale

        logging.info(f"Image comparison: PSNR={psnr_val:.2f}, SSIM={ssim_val:.2f}")
        return similarity_score, psnr_val, ssim_val

    except Exception as e:
        logging.error(f"Error comparing images {image1_path} and {image2_path}: {e}", exc_info=True)
        return 0.0, 0.0, 0.0 # Return zeros on error

if __name__ == "__main__":
    # Example Usage (requires dummy image files)
    # from PIL import Image
    # Image.new('RGB', (100, 100), color = 'red').save("original.png")
    # Image.new('RGB', (100, 100), color = 'blue').save("different.png")

    input_img = "original.png" # Replace with a real image for testing
    output_webp = "optimized.webp"

    if os.path.exists(input_img):
        print(f"Optimizing {input_img} to WebP...")
        try:
            optimize_image_webp(input_img, output_webp)
            print(f"Original size: {os.path.getsize(input_img)} bytes")
            print(f"Optimized size: {os.path.getsize(output_webp)} bytes")
            
            # Compare original and optimized
            similarity, psnr_val, ssim_val = compare_images(input_img, output_webp)
            print(f"Comparison (Original vs Optimized): Similarity={similarity:.2f}, PSNR={psnr_val:.2f}, SSIM={ssim_val:.2f}")

            # Create a slightly different image for comparison test
            img_diff = Image.open(input_img).convert("RGB")
            # Make a small change, e.g., draw a pixel
            img_diff.putpixel((10, 10), (0, 0, 0)) # Change one pixel to black
            different_img = "slightly_different.png"
            img_diff.save(different_img)
            
            similarity_diff, psnr_diff, ssim_diff = compare_images(input_img, different_img)
            print(f"Comparison (Original vs Slightly Different): Similarity={similarity_diff:.2f}, PSNR={psnr_diff:.2f}, SSIM={ssim_diff:.2f}")

        except Exception as e:
            print(f"Optimization/comparison failed: {e}")
        finally:
            # Clean up generated files
            if os.path.exists(output_webp): os.remove(output_webp)
            if os.path.exists(different_img): os.remove(different_img)
    else:
        print(f"Please create a dummy image file named '{input_img}' for testing.") 