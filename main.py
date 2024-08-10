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


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from xml.etree import ElementTree

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this list to specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_youtube_captions(video_id, language='en', proxies=None):
    url = f"https://www.youtube.com/api/timedtext?lang={language}&v={video_id}"
    response = requests.get(url, proxies=proxies)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve captions")
    
    root = ElementTree.fromstring(response.content)
    captions = []
    
    for elem in root.findall('text'):
        start = elem.attrib['start']
        duration = elem.attrib.get('dur', '0')
        text = elem.text or ''
        captions.append({'start': start, 'duration': duration, 'text': text})
    
    return captions

@app.get("/content/{video_id}")
async def get_captions(video_id: str, language: str = 'en'):
    try:
        # Example proxy setup (replace with actual proxy details if needed)

        proxies = {
            '45.127.248.127:5128:mfzzfgkn:dla1mef5pjk0'
'64.64.118.149:6732:mfzzfgkn:dla1mef5pjk0'
'157.52.253.244:6204:mfzzfgkn:dla1mef5pjk0'
'167.160.180.203:6754:mfzzfgkn:dla1mef5pjk0'
'166.88.58.10:5735:mfzzfgkn:dla1mef5pjk0'
'173.0.9.70:5653:mfzzfgkn:dla1mef5pjk0'
'45.151.162.198:6600:mfzzfgkn:dla1mef5pjk0'
'204.44.69.89:6342:mfzzfgkn:dla1mef5pjk0'
'173.0.9.209:5792:mfzzfgkn:dla1mef5pjk0'
'206.41.172.74:6634:mfzzfgkn:dla1mef5pjk0'

        }
        
        captions = fetch_youtube_captions(video_id, language, proxies=None)  # Set proxies=None if not using a proxy
        return {"video_id": video_id, "captions": captions}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the app, use the command: uvicorn script_name:app --reload