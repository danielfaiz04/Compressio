import os
import logging
from moviepy.editor import VideoFileClip

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def optimize_video(input_path: str, output_path: str, crf: int = 28) -> str:
    """
    Optimizes a video file using FFmpeg via moviepy, reducing its size.
    CRF (Constant Rate Factor) controls the quality: lower is better quality, larger file size.
    Typical range: 18 (visually lossless) to 28 (high compression).
    """
    try:
        logging.info(f"Optimizing video: {input_path} to {output_path} with CRF={crf}")
        clip = VideoFileClip(input_path)
        clip.write_videofile(output_path, 
                             codec="libx264", 
                             audio_codec="aac", 
                             ffmpeg_params=['-crf', str(crf)],
                             logger=None) # Suppress moviepy's own logging if desired
        clip.close()
        logging.info(f"Video optimized successfully: {input_path} -> {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"Error optimizing video {input_path}: {e}", exc_info=True)
        raise

def compare_videos(video1_path: str, video2_path: str) -> tuple[str, float]:
    """
    Compares two video files. This is a very basic comparison (file size, duration).
    More advanced comparison would involve perceptual hashing or detailed frame analysis.
    Returns a summary string and simulated decompression time.
    """
    summary = "Video Comparison: "
    simulated_decompress_time_ms = 100.0 # Base simulation time
    
    try:
        size1 = os.path.getsize(video1_path)
        size2 = os.path.getsize(video2_path)
        
        # Get durations (this can be slow for large videos)
        clip1 = VideoFileClip(video1_path)
        duration1 = clip1.duration
        clip1.close()

        clip2 = VideoFileClip(video2_path)
        duration2 = clip2.duration
        clip2.close()

        summary += f"Size: {size1} bytes vs {size2} bytes. Duration: {duration1:.2f}s vs {duration2:.2f}s."
        
        if abs(duration1 - duration2) < 0.1: # Allow small floating point differences
            summary += " Durations are similar."
        else:
            summary += " Durations differ."

        # Simulate decompression time based on file size and duration
        simulated_decompress_time_ms += (size2 / 1024) * 0.1 + (duration2 * 10) # Add 0.1ms per KB, 10ms per second

    except Exception as e:
        logging.warning(f"Error during video comparison for {video1_path} and {video2_path}: {e}")
        summary = f"Video Comparison Error: {e}"

    return summary, simulated_decompress_time_ms

if __name__ == "__main__":
    # Example Usage (requires a dummy video file and ffmpeg/imageio-ffmpeg installed)
    # To create a dummy video:
    # from moviepy.editor import ColorClip
    # clip = ColorClip((640, 480), color=(255,0,0), duration=5) # 5-second red video
    # clip.write_videofile("dummy_input.mp4", fps=24)

    input_video = "dummy_input.mp4" # Replace with a real video file for testing
    output_video = "optimized_dummy_input.mp4"

    if os.path.exists(input_video):
        print(f"Optimizing {input_video} to {output_video}...")
        try:
            optimize_video(input_video, output_video, crf=30)
            print(f"Original size: {os.path.getsize(input_video)} bytes")
            print(f"Optimized size: {os.path.getsize(output_video)} bytes")
            summary, decompress_time = compare_videos(input_video, output_video)
            print(f"Comparison Summary: {summary}")
            print(f"Simulated Decompression Time: {decompress_time:.2f} ms")
        except Exception as e:
            print(f"Optimization/comparison failed: {e}")
        finally:
            # Clean up generated files
            if os.path.exists(output_video):
                os.remove(output_video)
    else:
        print(f"Please create a dummy video file named '{input_video}' for testing.") 