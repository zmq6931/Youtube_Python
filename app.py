import streamlit as st
import yt_dlp
import os


def download_youtube_video(url, output_path=None, progress_callback=None):
    """
    Download a YouTube video from the given URL using yt-dlp.
    
    Args:
        url (str): The YouTube video URL
        output_path (str, optional): The directory to save the video. Defaults to current directory.
        progress_callback (function, optional): A callback function to update the progress.
    
    Returns:
        tuple: The path to the downloaded video file and the result message
    """
    try:
        if output_path is None or output_path.strip() == "":
            output_path = "downloads"
        output_path = os.path.abspath(output_path)
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
            'quiet': True,
            'verbose': True,
            'extract_flat': False,
            'force_generic_extractor': False,
            'geo_verification_proxy': '',
            'source_address': '0.0.0.0',
            'progress_hooks': [progress_callback] if progress_callback else [],
        }
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            st.write("Fetching video information...")
            info = ydl.extract_info(url, download=True)
            
            # Print video information
            st.write(f"\nTitle: {info.get('title', 'Unknown Title')}")
            st.write(f"Duration: {info.get('duration', 'Unknown')} seconds")
            
            # Handle filesize information
            filesize = info.get('filesize')
            if filesize:
                st.write(f"File size: {filesize / (1024*1024):.2f} MB")
            else:
                st.write("File size: Unknown")
            
            # Get the output file path
            output_file = os.path.join(output_path, f"{info.get('title', 'video')}.{info.get('ext', 'mp4')}")
            st.write(f"\nDownload completed! Saved to: {output_file}")
            
            return output_file, info
            
    except yt_dlp.utils.DownloadError as e:
        st.error(f"Download error: {str(e)}")
        # 获取可用格式
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                st.write("Available formats:")
                for f in formats:
                    st.write(f"{f.get('format_id')}: {f.get('ext')} - {f.get('format_note', '')} - {f.get('filesize', 'Unknown')} bytes")
        except Exception as e2:
            st.write("Could not fetch available formats.")
        return None, str(e)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None, str(e)


st.title("Youtube Downloader")

url = st.text_input("Enter Youtube URL")
progress_placeholder = st.empty()  # 只出现一次

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0.0%')
        progress_placeholder.write(f"Downloading... {percent}")
    elif d['status'] == 'finished':
        progress_placeholder.success("Download finished!")

if st.button("Download"):
    if not url:
        st.error("Please enter a valid Youtube URL")
    else:
        with st.spinner("Downloading....."):
            output_file, result = download_youtube_video(
                url, output_path="downloads", progress_callback=progress_hook
            )
            if output_file and os.path.exists(output_file):
                st.success("Download completed!")
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="Download Video",
                        data=f,
                        file_name=os.path.basename(output_file),
                        mime="video/mp4"
                    )
            else:
                st.error("Download failed or file not found. Please check the URL or try again.")
