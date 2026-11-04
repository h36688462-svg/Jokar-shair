import os
import asyncio
import subprocess
import edge_tts
import random

# 1. قائمة الـ 15 فيلماً أجنبياً
FOREIGN_MOVIES = [
    "Jurassic Reborn 2025", "Avatar 3", "Dune Part Two", "Godzilla x Kong", "Alien Romulus",
    "Deadpool and Wolverine", "Mad Max Fury Road", "The Batman Part II", "Gladiator II", "Oppenheimer",
    "John Wick Chapter 4", "Mission Impossible 8", "Spider-Man Across the Spider-Verse", "Inception", "Interstellar"
]

# 2. قائمة الـ 15 فيلماً عربياً
ARABIC_MOVIES = [
    "ولاد رزق 3", "السرب", "الإسكندراني", "بيت الروبي", "نبيل المهاراتي",
    "عصابة الماكس", "العميل صفر", "مرعي البريمو", "شقو", "رحلة 404",
    "رفعت زقزوق", "فاصل من اللحظات اللذيذة", "بعلم الوصول", "الهنا اللي أنا فيه", "الملحد"
]

# 3. قائمة المسلسلات الشهيرة
SERIES_LIST = [
    "مسلسل لعبة الحبار (Squid Game)", "مسلسل صراع العروش (Game of Thrones)", "مسلسل بريزون بريك (Prison Break)",
    "مسلسل بيكي بلايندرز (Peaky Blinders)", "مسلسل لا كاسا دي بابيل (Money Heist)", "مسلسل سترينجر ثينجز (Stranger Things)"
]

# 4. جدول المباريات والأحداث الكروية الحماسية
MATCHES_LIST = [
    "قمةريال مدريد وبرشلونة (الكلاسيكو)", "دوري أبطال أوروبا: ليلة الأبطال الكبرى", "قمة الدوري الإنجليزي: مانشستر سيتي ضد ليفربول",
    "ديربي مدريد المشتعل", "مباريات حاسمة في دوري أبطال أوروبا حصرياً على Jokar TV"
]

VOICE = "ar-SA-HamedNeural"  # صوت عربي رجالي احترافي

async def generate_voice(text, output_file="voice.mp3"):
    communicate = edge_tts.Communicate(text, VOICE, rate="+5%")
    await communicate.save(output_file)

def create_background_video():
    # تصميم خلفية سينمائية متوافقة مع التيك توك والريلز (9:16)
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "color=c=navy:s=720x1280:r=30",
        "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=stereo",
        "-t", "35",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "trailer.mp4"
    ]
    subprocess.run(cmd, check=True)

def merge_audio():
    cmd = [
        "ffmpeg", "-y",
        "-i", "trailer.mp4",
        "-i", "voice.mp3",
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        "final_short.mp4"
    ]
    subprocess.run(cmd, check=True)

async def main():
    # اختيار عشوائي للقسم (فلم أجنبي، فلم عربي، مسلسل، أو مباراة) لضمان التنوع اليومي
    category_choice = random.choice(["foreign", "arabic", "series", "match"])
    
    if category_choice == "foreign":
        item = random.choice(FOREIGN_MOVIES)
        script = f"أقوى الأفلام العالمية وأحدثها تجدها الآن بجودة عالية! تابع فيلم {item} حصرياً عبر تطبيق Jokar TV. حمّل التطبيق الآن واستمتع بمشاهدة بلا حدود."
    elif category_choice == "arabic":
        item = random.choice(ARABIC_MOVIES)
        script = f"السينما العربية في أبهى صورها! لا تفوت مشاهدة الفيلم العربي الرائع {item} بجودة عالية وبدون إعلانات مزعجة عبر منصة Jokar TV."
    elif category_choice == "series":
        item = random.choice(SERIES_LIST)
        script = f"هل أنت من عشاق الماراثون الدرامي؟ تابع أحداث ومواسم {item} كاملة وبجودة فائقة عبر تطبيق Jokar TV على هاتفك أو شاشتك الذكية."
    else:
        item = random.choice(MATCHES_LIST)
        script = f"عشاق المستديرة والكرة الأوروبية.. لا تفوتوا متابعة أقوى المباريات والأحداث الرياضية مثل {item} بث مباشر وبجودة عالية عبر تطبيق Jokar TV!"

    print(f"🎬 القسم المختار اليوم: {category_choice.upper()} - العنصر: {item}")
    print(f"📝 السكريبت التسويقي:\n{script}")
    
    # حفظ الوصف والهاشتاجات الجاهزة للنسخ
    with open("description.txt", "w", encoding="utf-8") as f:
        f.write(f"{script}\n\n📲 حمّل تطبيق Jokar TV الآن:\n🌐 الموقع الرسمي: https://jokartv.com\n🍏 للايفون (App Store): https://apps.apple.com/app/id1628995509\n🤖 للاندرويد: متوفر حصرياً عبر موقعنا الرسمي\n\n#ملخصات_افلام #JokarTV #مباريات_اليوم #مسلسلات #تيك_توك_افلام #اكسبلور #سينما")

    print("🎙️ جاري توليد التعليق الصوتي...")
    await generate_voice(script)
    
    print("🎨 جاري تجهيز الفيديو...")
    create_background_video()
    merge_audio()
    
    print("✅ تم تجهيز الفيديو والوصف اليومي بنجاح!")

if __name__ == "__main__":
    asyncio.run(main())
