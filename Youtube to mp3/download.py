import requests
import base64
import ast
import random
import time
import json
import os
import re
from pathlib import Path
import urllib.request


def res_parser(data, start, end):
    start = start.encode()
    end = end.encode()
    return (data[data.find(start)+len(start):data.rfind(end)]).decode()
    
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def authorization(gC):
    try:
        # Decode gC.t[0] and evaluate it
        if eval(base64.b64decode(gC["t"][0]).decode()) != gC["t"][1]:
            return False

        f = gC["f"]
        part0 = f[6][::-1] + f[7]

        decoded_0 = base64.b64decode(gC["0"]).decode()
        positions = list(map(int, decoded_0.split(f[5])))

        g1_reversed = gC["1"][::-1] if f[4] > 0 else gC["1"]
        for p in positions:
            part0 += g1_reversed[p - f[3]]

        if f[1] == 1:
            part0 = part0[:len(f[6] + f[7])] + part0[len(f[6] + f[7]):].lower()
        elif f[1] == 2:
            part0 = part0[:len(f[6] + f[7])] + part0[len(f[6] + f[7]):].upper()

        if len(f[0]) > 0:
            # Ensure f[8] is an integer before using chr()
            f8 = int(f[8])  # Convert to integer if it's not already
            cleaned = base64.b64decode(f[0]).decode().replace(chr(f8), "")
            return base64.b64encode((cleaned + "_" + gC["2"]).encode()).decode()
        elif f[2] > 0:
            part_length = f[2] + len(f[6] + f[7])
            return base64.b64encode((part0[:part_length] + "_" + gC["2"]).encode()).decode()
        else:
            return base64.b64encode((part0 + "_" + gC["2"]).encode()).decode()
    except Exception as e:
        print(f"Authorization error: {e}")
        return None

def download_song(link):
    # Use a more modern User-Agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "sec-ch-ua": '"Chromium";v="121", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }
    
    # First request to get the main page
    print("Fetching main page...")
    yield f"Fetching main page..."

    response = requests.get('https://y2mate.nu/en-NIlf/', headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch main page: {response.status_code}")
        yield f"Failed to fetch main page: {response.status_code}"

        
        return
    
    print("Extracting authorization script...")
    yield f"Extracting authorization script..."
    try:
        # Extract the encoded script
        encoded_script = res_parser(response.content, "atob('", "'")
        res_script_str = base64.b64decode(encoded_script).decode()
        
        # Extract the gC object
        res_script_str_clean = find_between(res_script_str, "var gC = ", ";")
        if not res_script_str_clean:
            print("Failed to extract gC object")
            yield f"Failed to extract gC object"
            return
            
        # Parse the gC object
        res_script = ast.literal_eval(res_script_str_clean)
        
        # Generate the authorization token
        cookie = authorization(res_script)
        if not cookie:
            print("Failed to generate authorization token")
            yield f"Failed to generate authorization token"
            return
            
        print(f"Generated token: {cookie}")
        print(f"Decoded token: {base64.b64decode(cookie).decode()}")
        yield f"Generated token: {cookie}"
        yield f"Decoded token: {base64.b64decode(cookie).decode()}"
        
        # Prepare headers for API request
        api_headers = {
            "Host": "d.mnuu.nu",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Ch-Ua": '"Chromium";v="121", "Not A(Brand";v="24"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Sec-Ch-Ua-Mobile": "?0",
            "Accept": "*/*",
            "Origin": "https://y2mate.nu",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://y2mate.nu/",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        
        # Add a slight delay to mimic human behavior
        time.sleep(1.5)
        
        # Make the API request
        num_rand = random.random()
        url = f"https://d.mnuu.nu/api/v1/init?a={cookie}&_{num_rand}"
        
        print(f"Making API request #1 to: {url}")
        yield f"Making API request #1 || For getting a url for request #2 || to url: {url}"

        api_response = requests.get(url, headers=api_headers)
        
        print(f"Response status: {api_response.status_code}")
        print(f"Response headers: {api_response.headers}")
        print(f"Response body: {api_response.text}")
        yield f"Response status: {api_response.status_code}"
        yield f"Response headers: {api_response.headers}"
        yield f"Response body: {api_response.text}"


        

        request_url = find_between(api_response.text,'"convertURL":"','","error":"0"}')
        print(f"Making API request #2 to: {request_url}")
        yield f"Making API request #2 || For getting a url for request #3 || to url: {request_url}"
        time.sleep(1.5)

        headers = {
        "Host": "uumu.mnuu.nu",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": "\"Chromium\";v=\"135\", \"Not-A.Brand\";v=\"8\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Sec-Ch-Ua-Mobile": "?0",
        "Accept": "*/*",
        "Origin": "https://y2mate.nu",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://y2mate.nu/",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=4, i",
        "Connection": "keep-alive"
    }
        
        youtube_song_url = link
        song_yt_id = youtube_song_url.partition("v=")[2]
        sub = "&" # basically if the song is in a list it will have more variables
        song_yt_id = song_yt_id.split(sub)[0]

        url = f"{request_url}&v={song_yt_id}&f=mp3"
        api_response = requests.get(url, headers=headers)
        print(f"Response status: {api_response.status_code}")
        print(f"Response headers: {api_response.headers}")
        print(f"Response body: {api_response.text}")
        yield f"Response status: {api_response.status_code}"
        yield f"Response headers: {api_response.headers}"
        yield f"Response body: {api_response.text}"

        response_url = find_between(api_response.text,'"redirectURL":"','\\')
        url = f"{response_url}&v={song_yt_id}&f=mp3"
        api_response = requests.get(url, headers=headers)
        yield f"Making API request #3 || For getting a Download Url :{url}"
        print(f"Response status: {api_response.status_code}")
        print(f"Response headers: {api_response.headers}")
        print(f"Response body: {api_response.text}")
        yield f"Response status: {api_response.status_code}"
        yield f"Response headers: {api_response.headers}"
        yield f"Response body: {api_response.text}"

        time.sleep(1.5)

        download_url = find_between(api_response.text,'"downloadURL":"','","redirectURL"')
        print(f"Download_url: {download_url}")
        yield f"Download_url: {download_url}"
        
        download_response = requests.get(download_url)

        response = urllib.request.urlopen(download_url)
        headers = response.getheaders()
        print(headers)
        yield f"Headers: {headers}"

        # Convert headers to dict
        headers_dict = dict(headers)

        # Get Content-Disposition value
        cd = headers_dict.get("Content-Disposition", "")

        # Extract filename
        match = re.search(r'filename="([^"]+)"', cd)
        filename_with_ext = match.group(1) if match else None

        # Remove .mp3 extension if present
        filename = filename_with_ext.rsplit(".mp3", 1)[0] if filename_with_ext else None

        def fix_misencoded(broken_str):
            # Encode the string back to bytes assuming it was misread as latin1
            byte_str = broken_str.encode('latin1')
            # Now decode it properly as UTF-8
            return byte_str.decode('utf-8')

        def sanitize_filename(filename):
            # Remove or replace illegal Windows characters
            return re.sub(r'[<>:"/\\|?*]', '', filename)

        fixed = fix_misencoded(filename)
        safe_filename = sanitize_filename(fixed)

        print(f"file name: {safe_filename}")
        yield f"File name: {safe_filename}"

        # FILE PATH:
        # create a 'Downloads' folder in the same folder this script is
        # Get the directory where the script is located
        script_dir = Path(__file__).parent

        # Define the new directory path relative to the script location
        new_dir = script_dir / "Downloads"

        # Create the directory (and parents if needed)
        new_dir.mkdir(parents=True, exist_ok=True)

        file_Path = os.path.join(os.path.expanduser("./Downloads"), f"{safe_filename}.mp3")
        


        if download_response.status_code == 200:
            with open(file_Path, 'wb') as file:
                file.write(download_response.content)
            print('File downloaded successfully')
            yield f"File downloaded successfully"
        else:
            print('Failed to download file')
            yield f"Failed to download file"


            
    except Exception as e:
        print(f"Error: {e}")
        yield f"Error: {e}"
