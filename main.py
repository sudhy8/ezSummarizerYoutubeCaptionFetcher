import os
import tempfile
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import shutil
import glob
app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/content/{video_id}")
async def get_content(video_id: str):
    try:
        # Try to get captions
        # try:
        #     transcript = YouTubeTranscriptApi.get_transcript(video_id)
        #     return JSONResponse(content={"captions": transcript})
        # except Exception as caption_error:
        #     # If captions are not available, proceed to audio download
        #     pass

        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(id)s.%(ext)s',
        }

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set the output template to use the temporary directory
            ydl_opts['outtmpl'] = os.path.join(temp_dir, '%(id)s.%(ext)s')

            # Download the audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

            # Find the downloaded file
            for file in os.listdir(temp_dir):
                if file.startswith(video_id):
                    src_path = os.path.join(temp_dir, file)
                    dest_path = os.path.join(os.getcwd(), f"{video_id}.mp3")
                    shutil.copy2(src_path, dest_path)

                    return FileResponse(
                        dest_path,
                        media_type="audio/mpeg",
                        filename=f"{video_id}.mp3",
                        headers={"X-Content-Type": "audio"}
                    )

        raise Exception("Audio file not found after download")

    except Exception as e:
        # If both captions and audio fail, raise an HTTP exception
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get content. Error: {str(e)}"
        )

@app.on_event("startup")
async def startup_event():
    # Create a directory to store downloaded files if it doesn't exist
    os.makedirs("downloads", exist_ok=True)



@app.get("/shutdown")
async def shutdown_event():
    # Clean up all audio files in the directory
    delete_all_audio_files('')

def delete_all_audio_files(directory: str):
    """Delete all audio files in the specified directory."""
    audio_extensions = ['*.mp3', '*.wav', '*.m4a']
    for ext in audio_extensions:
        files = glob.glob(os.path.join(directory, ext))
        for file in files:
            try:
                os.remove(file)
                print(f"Deleted file: {file}")
            except Exception as e:
                print(f"Error deleting file {file}: {e}")

@app.get("/delete_audio_files")
async def delete_audio_files():
    """Endpoint to delete all audio files in the directory."""
    try:
        delete_all_audio_files('')
        return {"message": "All audio files deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete audio files. Error: {str(e)}")
    


@app.get("/")
async def read_root():
    return {"message": "Welcome to the YouTube Content API"}