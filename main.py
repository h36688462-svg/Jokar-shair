import os
import asyncio
import subprocess
import edge_tts
import random

FOREIGN_MOVIES = ["Jurassic Reborn 2025", "Avatar 3", "Dune Part Two", "Godzilla x Kong", "Alien Romulus"]
ARABIC_MOVIES = ["ولاد رزق 3", "السرب", "الإسكندراني", "بيت الروبي", "عصابة الماكس"]
SERIES_LIST = ["مسلسل لعبة الحبار", "مسلسل صراع العروش", "مسلسل بريزون بريك"]
MATCHES_LIST = ["قمة ريال مدريد وبرشلونة", "دوري أبطال أوروبا", "قمة الدوري الإنجليزي"]

VOICE = "ar-SA-HamedNeural"

async def generate_voice(text, output_file="voice.mp3"):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

def create_fast_video():
    # إنشاء فيديو سريع جداً خلال ثوانٍ معدودة بدون أي عمليات معقدة
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=navy:s=720x1280:r=30",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", "30",
        "-c:v", "libx264", "-preset", "ultrafast",
        "-c:a", "aac",
        "-shortest", "final_short.mp4"
    ]
    subprocess.run(cmd, check=True)

async def main():
    category = random.choice(["foreign", "arabic", "series", "match"])
    if category == "foreign":
        item = random.choice(FOREIGN_MOVIES)
        script = f"تابع فيلم {item} بجودة عالية وبدون إعلانات حصرياً عبر تطبيق Jokar TV. حمّل التطبيق الآن واستمتع بمشاهدة بلا حدود."
    elif category == "arabic":
        item = random.choice(ARABIC_MOVIES)
        script = f"لا تفوت مشاهدة الفيلم العربي الرائع {item} بجودة عالية عبر منصة Jokar TV. حمّل التطبيق الآن!"
    elif category == "series":
        item = random.choice(SERIES_LIST)
        script = f"تابع أحداث ومواسم {item} كاملة وبجودة فائقة عبر تطبيق Jokar TV على هاتفك أو شاشتك الذكية."
    else:
        item = random.choice(MATCHES_LIST)
        script = f"عشاق المستديرة والكرة الأوروبية.. تابع أقوى المباريات والأحداث الرياضية مثل {item} بث مباشر عبر تطبيق Jokar TV!"

    print(f"🎬 العنصر المختار: {item}")
    
    with open("description.txt", "w", encoding="utf-8") as f:
        f.write(f"{script}\n\n📲 حمّل تطبيق Jokar TV الآن:\n🌐 الموقع الرسمي: https://jokartv.com\n🍏 للايفون (App Store): https://apps.apple.com/app/id1628995509\n🤖 للاندرويد: متوفر حصرياً عبر موقعنا الرسمي\n\n#ملخصات_افلام #JokarTV #مباريات_اليوم #مسلسلات #تيك_توك_افلام #اكسبلور")

    await generate_voice(script, "voice.mp3")
    create_fast_video()
    print("✅ تم الانتهاء بنجاح في وقت قياسي!")

if __name__ == "__main__":
    asyncio.run(main())
