from fastapi import FastAPI
import yt_dlp
from yt_dlp.utils import DownloadError

app = FastAPI()

ydl_opts = {
    "quiet": True,
    "skip_download": True,
    "extract_flat": True,
}

@app.get("/find-8d")
def find_8d(url_or_query: str):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url_or_query, download=False)
        except DownloadError:
            info = {"entries": [{"title": url_or_query, "id": None}]}

        video_titles = []
        original_ids = set()

        if "entries" in info:
            for entry in info["entries"]:
                if entry and "title" in entry:
                    video_titles.append(entry["title"])
                    if entry.get("id"):
                        original_ids.add(entry["id"])
        elif "title" in info:
            video_titles.append(info["title"])
            if info.get("id"):
                original_ids.add(info["id"])

        results_payload = {}

        for title in video_titles:
            search_term = f"{title} 8D"
            search_url = f"ytsearch10:{search_term}"
            search_info = ydl.extract_info(search_url, download=False)
            results = search_info.get("entries", [])

            results = [
                r for r in results
                if r.get("id") and r.get("id") not in original_ids
            ]

            results.sort(
                key=lambda x: x.get("view_count", 0),
                reverse=True
            )

            results_payload[title] = [
                f"https://www.youtube.com/watch?v={r['id']}"
                for r in results[:3]
            ]

        return results_payload