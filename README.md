# Youtube-to-mp3-via-HTTP-requests

>This project is a lightweight Flask web app that lets users convert YouTube videos to MP3 by interacting with y2mate.nu through direct HTTP requests — no browser automation or third-party APIs required.

![project_img](https://github.com/user-attachments/assets/68455d33-8166-4861-a3c3-4228c5e5516b)

## Fetures
- No browser automation (headless or otherwise).

- Works via direct HTTP requests.

- Real-time logging using SSE.

- Auto-creates download directory.

- Extracts video title from response headers.

- Lightweight and minimal dependencies.

## Overview
The app performs a decoding of an obfuscated JavaScript file that is loaded during the site’s initial request. This script is responsible for generating a critical cookie, which is Base64-encoded and obscured through deliberate code obfuscation. The cookie must be extracted and decoded to proceed.

The conversion process involves three main HTTP requests:

1. **Initial request** – Retrieves the obfuscated JavaScript and generates the cookie.

2. **Second request** – Sends the YouTube video ID `(v=...)` along with a `sig` variable (obtained from the previous response).

3. **Final request** – Retrieves the actual MP3 download URL. The response includes HTTP headers containing the file's title, which is used as the filename.

The downloaded MP3 files are saved to a `downloads/` folder within the project directory. This folder is automatically created if it doesn’t already exist.

Throughout the entire process, real-time updates are streamed to the client using **Server-Sent Events (SSE)**. A log panel on the webpage displays detailed request information, including status codes, headers, errors (if any), and a success message once the file has been downloaded.

## Usage
1. Open the web interface.

2. Paste a YouTube URL.

3. Watch the log update in real time.

4. Find the MP3 in the downloads/ folder.

## 🐳 Run with Docker
1. You can build and run locally with `docker build` and `docker run`:
Docker build:
```
docker build --tag <DOCKER_IMAGE_NAME> .
```
Docker run:
```
docker run -d -p 5000:5000 <DOCKER_IMAGE_NAME>
```


2. Or Pull the image from Docker Hub:

```
docker pull blackdragon21/youtube-to-mp3-via-http:latest
```

## Legal Disclaimer
>⚠️ This tool is intended for educational purposes only. Downloading content without permission may violate YouTube's terms of service. Use at your own discretion.
