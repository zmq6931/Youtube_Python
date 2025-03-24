import yt_dlp
import os
from datetime import datetime

def download_youtube_video(url, output_path=None):
    """
    Download a YouTube video from the given URL using yt-dlp.
    
    Args:
        url (str): The YouTube video URL
        output_path (str, optional): The directory to save the video. Defaults to current directory.
    
    Returns:
        str: The path to the downloaded video file
    """
    try:
        # Set default output path if none provided
        if output_path is None:
            output_path = os.getcwd()
        
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Configure yt-dlp options
        ydl_opts = {
            # Format selection
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # More flexible format selection
            'merge_output_format': 'mp4',
            
            # Output template
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            
            # Network options
            'socket_timeout': 30,
            'retries': 10,
            'fragment_retries': 10,
            'file_access_retries': 10,
            'extractor_retries': 10,
            'ignoreerrors': True,
            
            # Browser simulation
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
            },
            
            # Additional options
            'no_check_certificates': True,
            'no_warnings': True,
            'quiet': False,
            'verbose': True,
            'extract_flat': False,
            'force_generic_extractor': False,
            'geo_verification_proxy': '',
            'source_address': '0.0.0.0',
        }
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            print("Fetching video information...")
            info = ydl.extract_info(url, download=False)
            
            # Print video information
            print(f"\nTitle: {info.get('title', 'Unknown Title')}")
            print(f"Duration: {info.get('duration', 'Unknown')} seconds")
            
            # Handle filesize information
            filesize = info.get('filesize')
            if filesize:
                print(f"File size: {filesize / (1024*1024):.2f} MB")
            else:
                print("File size: Unknown")
            
            # Download the video
            print("\nStarting download...")
            ydl.download([url])
            
            # Get the output file path
            output_file = os.path.join(output_path, f"{info.get('title', 'video')}.{info.get('ext', 'mp4')}")
            print(f"\nDownload completed! Saved to: {output_file}")
            
            return output_file
            
    except yt_dlp.utils.DownloadError as e:
        print(f"Download error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure the video URL is correct and the video is publicly available")
        print("2. Try using a different video URL")
        print("3. Check your internet connection")
        print("4. If using a VPN, try disabling it")
        print("5. Try updating yt-dlp: pip install --upgrade yt-dlp")
        print("6. The video might be age-restricted or region-restricted")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    video_url = input("Enter YouTube video URL: ")
    download_youtube_video(video_url) 