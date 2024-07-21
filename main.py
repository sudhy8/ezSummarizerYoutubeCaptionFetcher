from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

@app.get("/captions/{video_id}")
async def get_captions(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return {"captions": transcript}
    except Exception as e:
        if "Subtitles are disabled for this video" in str(e):
            raise HTTPException(status_code=404, detail="Captions are disabled for this video")
        elif "No transcripts were found" in str(e):
            raise HTTPException(status_code=404, detail="No captions found for this video")
        else:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)