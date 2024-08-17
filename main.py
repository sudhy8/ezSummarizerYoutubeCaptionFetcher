# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from youtube_transcript_api import YouTubeTranscriptApi
# import logging
# import os
# import glob

# app = FastAPI()

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods
#     allow_headers=["*"],  # Allow all headers
# )

# @app.get("/content/{video_id}")
# async def get_content(video_id: str):
#     try:
#         logging.info(f"Fetching transcript for video ID: {video_id}")
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         logging.info("Transcript fetched successfully")
#         return JSONResponse(content={"captions": transcript})
#     except Exception as e:
#         logging.error(f"Failed to fetch transcript: {e}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to get content. Error: {str(e)}"
#         )

# @app.on_event("startup")
# async def startup_event():
#     # Create a directory to store downloaded files if it doesn't exist
#     os.makedirs("downloads", exist_ok=True)
#     logging.info("Startup: Downloads directory ensured")

# @app.get("/shutdown")
# async def shutdown_event():
#     # Clean up all audio files in the directory
#     delete_all_audio_files('downloads')
#     return {"message": "Server shutdown and cleaned up"}

# def delete_all_audio_files(directory: str):
#     """Delete all audio files in the specified directory."""
#     audio_extensions = ['*.mp3', '*.wav', '*.m4a']
#     for ext in audio_extensions:
#         files = glob.glob(os.path.join(directory, ext))
#         for file in files:
#             try:
#                 os.remove(file)
#                 logging.info(f"Deleted file: {file}")
#             except Exception as e:
#                 logging.error(f"Error deleting file {file}: {e}")

# @app.get("/delete_audio_files")
# async def delete_audio_files():
#     """Endpoint to delete all audio files in the directory."""
#     try:
#         delete_all_audio_files('downloads')
#         return {"message": "All audio files deleted successfully"}
#     except Exception as e:
#         logging.error(f"Failed to delete audio files: {e}")
#         raise HTTPException(status_code=500, detail=f"Failed to delete audio files. Error: {str(e)}")

# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to the YouTube Content API"}


from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
import yt_dlp
import os

app = FastAPI()

def download_audio(youtube_url: str, output_path: str):
    # Define the options for downloading the audio
    ydl_opts = {
        'format': 'bestaudio/best', # Download the best available audio quality
        'postprocessors': [{
            'key': 'FFmpegExtractAudio', # Extract audio using FFmpeg
            'preferredcodec': 'mp3', # Convert the audio to mp3 format
            'preferredquality': '192', # Set the audio quality to 192 kbps
        }],
        'outtmpl': output_path,
        'quiet': True  # Enable logging for debugging
    }
    try:
        # Use yt-dlp to download the audio from the provided YouTube URL
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"File not found after download: {output_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading audio: {str(e)}")

@app.get("/download_audio/")
async def download_audio_endpoint(url: str = Query(..., description="YouTube video URL")):
    try:
        output_path = "audio.mp3"
        try:
            download_audio(url, output_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Downloaded : {str(e)}")
        try:
            print("--------------")
            return FileResponse(output_path+'.mp3', media_type='audio/mpeg', filename="audio.mp3.mp3")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected file downloaderror: {str(e)}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        return FileResponse(output_path+'.mp3', media_type='audio/mpeg', filename="audio.mp3.mp3")
        if os.path.exists(output_path):
            os.remove(output_path)  # Clean up the downloaded file
