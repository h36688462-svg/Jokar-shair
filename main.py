import os
import asyncio
import subprocess
import edge_tts
import random

# قائمة الأفلام مع نصوص مراجعة جاهزة ومحفوظة لتفادي أي ضغط على الخوادم وضمان عمل السيرفر 100%
MOVIES_DATA = {
    "Jurassic Reborn 2025": "لو كنت تبحث عن فيلم ديناصورات جديد وتظن أنه الفيلم الأصلي.. انتبه! فيلم Jurassic Reborn يأخذنا في مغامرة مرعبة على جزيرة معزولة للبحث عن عينات دم الديناصورات. هل تفوقت على الأفلام الكلاسيكية؟ شاهد الفيلم واحكم بنفسك!",
    "Jurassic World Rebirth 2025": "الديناصورات تعود من جديد لتسيطر على كوكب الأرض في ملحمة سينمائية ضخمة! فريق من العلماء يواجه أخطر المخلوقات على جزيرة منسية. صراع بقاء حماسي لا ينفنفصم عنه التشويق والإثارة من اللحظة الأولى.",
    "Dune Part Two": "عودة الأسطورة بول أتريديس في ملحمة خيال علمي أبهرت العالم بصرياً وسردياً. حرب الكواكب ومعارك الرمال الكبرى في أحد أعظم أعمال السينما الحديثة. هل شاهدت الجزء الثاني؟",
    "Godzilla x Kong The New Empire": "عندما يتحد ملك الأساطير وملك الجزيرة لمواجهة تهديد مدمر يهدد العالم بأكمله! أكشن حماسي ومعارك عملاقة لا تهادن من بداية الفيلم وحتى النهاية.",
    "Alien Romulus": "رعب الفضاء يعود لأصوله المرعبة! مجموعة من الشباب يكتشفون محطة مهجورة ليجدوا أنفسهم وجهاً لوجه أمام أرعب كائن فضائي في تاريخ السينما."
}

VOICE = "ar-SA-HamedNeural"  # صوت عربي رجالي احترافي

async def generate_voice(text, output_file="voice.mp3"):
    communicate = edge_tts.Communicate(text, VOICE, rate="+5%")
    await communicate.save(output_file)

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
    movie, script = random.choice(list(MOVIES_DATA.items()))
    print(f"🎬 جاري صناعة فيديو عن فيلم: {movie}")
    print(f"📝 السكريبت:\n{script}")
    
    await generate_voice(script)
    download_trailer(movie)
    create_short()
    print("✅ تم تجهيز الفيديو بنجاح: final_short.mp4")

if __name__ == "__main__":
    asyncio.run(main())
