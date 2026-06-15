import urllib.request
import re
req = urllib.request.Request('https://guide.michelin.com/en/chiang-mai-region/chiang-mai/restaurant/larb-duang-dee-mee-sook', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)
    if match:
        print(f"IMAGE_URL:{match.group(1)}")
    else:
        print("No og:image found")
except Exception as e:
    print(f"Error: {e}")
