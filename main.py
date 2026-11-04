import os
import asyncio
import subprocess
import edge_tts
from google import genai
import random

# قائمة الأفلام (يمكنك ترك فيلم واحد فقط لو أردت تجربته الآن)
MOVIES = [
    "Jurassic Reborn 2025",
    "Jurassic World Rebirth 2025",
    "Dune Part Two",
    "Godzilla x Kong The New Empire",
    "Alien Romulus"
]

VOICE = "ar-SA-HamedNeural"  # صوت عربي رجالي احترافي ومجاني

async def generate_voice(text, output_file="voice.mp3"):
    communicate = edge_tts.Communicate(text, VOICE, rate="+5%")
    await communicate.save(output_file)

def generate_script(movie_name):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = f"""
    اكتب سكريبت مراجعة وملخص مشوق وقصير جداً (حوالي 80 كلمة، يُقرأ في 35 ثانية) لفيلم {movie_name} 
    مناسب لفيديو تيك توك ويوتيوب شورتس.
    ابدأ بخطاف قوي يجذب الانتباه في أول جملة، ثم اذكر القصة باختصار وهل يستحق المشاهدة.
    اكتب النص العربي الذي سيُقرأ فقط بدون أي مقدمات أو توجيهات إخراجية أو رموز.
    """
    response = client.models.generate_content(
        model="gemini-3.8-flash",  # تم التحديث إلى النموذج الجديد المعتمد
        contents=prompt,
    )
    return response.text.strip()

def download_trailer(movie_name):
    search_query = f"ytsearch1:{movie_name} official trailer"
    cmd = [
        "yt-dlp",
        "-f", "best[height<=720][ext=mp4]/best[ext=mp4]/best",
        "--extractor-args", "youtube:player_client=android,web",
        "--max-filesize", "50M",
        "-o", "trailer.mp4",
        search_query
    ]
    subprocess.run(cmd, check=True)

def create_short():
    cmd = [
        "ffmpeg", "-y",
        "-ss", "00:00:08",
        "-i", "trailer.mp4",
        "-i", "voice.mp3",
        "-filter_complex", "[0:v]scale=-2:1280,crop=720:1280,eq=contrast=1.05:saturation=1.1[v]",
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-c:a", "aac",
        "-shortest",
        "final_short.mp4"
    ]
    subprocess.run(cmd, check=True)

async def main():
    movie = random.choice(MOVIES)
    print(f"🎬 جاري صناعة فيديو عن فيلم: {movie}")
    
    script = generate_script(movie)
    print(f"📝 السكريبت:\n{script}")
    
    await generate_voice(script)
    download_trailer(movie)
    create_short()
    print("✅ تم تجهيز الفيديو بنجاح: final_short.mp4")

if __name__ == "__main__":
    asyncio.run(main())
