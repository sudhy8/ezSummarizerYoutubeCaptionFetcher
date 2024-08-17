
# Video Summarization 

## Youtube Caption Fetcher

Video summarization has become an essential tool in managing the overwhelming amount of video content available online. In the context of YouTube, where millions of hours of video are uploaded daily, efficiently extracting key information from videos is crucial for users who seek to quickly grasp the content without watching the entire video. The YouTube Caption Fetcher module addresses this need by leveraging closed captions to facilitate the summarization process.

This section of the project focuses on the integration of video summarization techniques through the extraction and processing of YouTube captions. By utilizing these captions, the module can generate concise summaries that capture the essence of the video content, enhancing user experience by saving time and providing quick insights. The implementation not only includes caption extraction but also incorporates fallback mechanisms for videos without captions, ensuring robustness and reliability across diverse video types. Through this approach, the module plays a pivotal role in making vast amounts of video content more accessible and manageable.
## Contributing

Agish Libertin
Albin Baby
Ashok Kumar
Jasmin Joseph
Niva Sadanandan
Sudhy Sukumaran


## Features

Download Best Available Audio: The application downloads the best quality audio available from the provided YouTube video.

Audio Format: The audio is extracted and converted to MP3 format with a quality of 192 kbps.

Error Handling: The application includes robust error handling to manage issues during the download and file processing stages.

Automatic Cleanup: After the audio file is served, it is automatically removed from the server to save space.


## End Points

GET /download_audio/

Parameters
url (required): The URL of the YouTube video from which to download the audio.

Response
Success: Returns the MP3 audio file as a downloadable response.

Error: Returns an HTTP error with a detailed message in case of any issues during the download or file processing.

Example
To download audio from a YouTube video, make a GET request to the /download_audio/ endpoint with the YouTube video URL:

curl -X GET "http://127.0.0.1:8000/download_audio/?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"

## Installation and Setup

Prerequisites
Python 3.7+
FFmpeg: Required for audio extraction and conversion. Install it using your package manager, for example:

sudo apt-get install ffmpeg

yt-dlp: Install yt-dlp via pip:
pip install yt-dlp

Install Python Dependencies
Create a virtual environment and install the required Python packages:

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

Run the Application
To start the FastAPI application, run:
uvicorn main:app --reload
This will start the application on http://127.0.0.1:8000/.
## Notes

Logging: The quiet option in yt-dlp is enabled to reduce console output during debugging. You can disable it if detailed logs are required.

Error Handling: The application handles various exceptions to provide meaningful error messages and HTTP status codes.

Cleanup: The downloaded audio file is automatically deleted after it is served to the client.
## Potential Improvements

Custom Output Paths: Allow users to specify custom output paths for the downloaded files.

Additional Formats: Extend support to other audio formats such as WAV or FLAC.

Enhanced Error Reporting: Provide more granular error messages to help diagnose specific issues related to YouTube download restrictions or network problems.