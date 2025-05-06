import requests

def link_check(link):
    check_starts = link.startswith("https://www.youtube.com/watch?v=")
    try:
        x = requests.get(link)
        check_status_code = x.status_code
    except requests.RequestException:
        return False

    return check_starts and check_status_code == 200

