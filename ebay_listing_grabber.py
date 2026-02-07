import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup


def download_video_ffmpeg(m3u8_url, output_path):
    """
    Downloads m3u8 stream directly using ffmpeg subprocess.
    """
    try:
        command = [
            "ffmpeg",
            "-y",
            "-i",
            m3u8_url,
            "-c",
            "copy",
            "-bsf:a",
            "aac_adtstoasc",
            "-loglevel",
            "error",
            output_path,
        ]

        print("Running FFmpeg...")
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed with error: {e}")
        return False
    except FileNotFoundError:
        print("FFmpeg not found. Please install it (sudo apt install ffmpeg).")
        return False


def download_ebay_media(url, folder_name="ebay_media"):
    os.makedirs(folder_name, exist_ok=True)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        }
    )

    print(f"Fetching listing: {url}")
    response = session.get(url)
    response.raise_for_status()
    page_source = response.text

    # --- VIDEO EXTRACTION ---
    print("Scanning page source for video links...")
    video_pattern = r'"HLS":"(https://video\.ebaycdn\.net/.*?.m3u8)"'
    match = re.search(video_pattern, page_source)

    if match:
        video_url = match.group(1).replace(r"\/", "/")
        print(f"Video URL found: {video_url}")

        output_file = os.path.join(folder_name, "listing_video.mp4")

        if download_video_ffmpeg(video_url, output_file):
            print(f"Video saved successfully: {output_file}")
        else:
            print("Failed to download video.")
    else:
        print("No video found in page source.")

    # --- IMAGE EXTRACTION ---
    print("Extracting images...")
    soup = BeautifulSoup(page_source, "html.parser")
    img_elements = soup.select("div.ux-image-carousel img")
    unique_urls = set()

    for img in img_elements:
        src = img.get("src") or img.get("data-src") or img.get("data-zoom-src")
        if src and "i.ebayimg.com" in src:
            clean_url = src.split("?")[0]
            hi_res = re.sub(r"s-l\d+", "s-l1600", clean_url)
            unique_urls.add(hi_res)

    print(f"Found {len(unique_urls)} unique images.")

    sorted_urls = sorted(unique_urls)

    def download_image(args):
        i, img_url = args
        try:
            img_data = session.get(img_url).content
            filepath = os.path.join(folder_name, f"image_{i + 1}.jpg")
            with open(filepath, "wb") as f:
                f.write(img_data)
        except Exception as e:
            print(f"Failed to download image: {img_url} ({e})")

    with ThreadPoolExecutor(max_workers=5) as pool:
        pool.map(download_image, enumerate(sorted_urls))

    print("Done.")


if __name__ == "__main__":
    target_url = "https://www.ebay.com/itm/266887458583"
    download_ebay_media(target_url)
