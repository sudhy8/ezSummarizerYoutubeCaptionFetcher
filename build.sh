#!/bin/bash

# Download and extract FFmpeg
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz
tar -xvf ffmpeg-release-64bit-static.tar.xz
mv ffmpeg-*-static/ffmpeg ffmpeg-*-static/ffprobe /usr/local/bin/