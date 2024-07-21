import os
import tempfile
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
import shutil

app = FastAPI()

@app.get("/content/{video_id}")
async def get_content(video_id: str):
    try:
        # Try to get captions
        try:
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
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return JSONResponse(content={"captions": transcript})
        except Exception as caption_error:
            # If captions are not available, proceed to audio download
            pass

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

@app.on_event("shutdown")
async def shutdown_event():
    # Clean up downloaded files
    for file in os.listdir("downloads"):
        os.remove(os.path.join("downloads", file))
