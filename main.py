import os
import subprocess
import random

# قائمة لأبرز الأفلام والمسلسلات لجلب إعلاناتها السينمائية الحقيقية
MOVIES_AND_SERIES = [
    "Dune Part Two official trailer",
    "Godzilla x Kong official trailer",
    "Avatar 3 official trailer",
    "Squid Game official trailer",
    "Interstellar official trailer",
    "The Batman official trailer",
    "Stranger Things trailer"
]

def download_and_process_trailer():
    # اختيار فيلم أو مسلسل بشكل عشوائي
    target = random.choice(MOVIES_AND_SERIES)
    print(f"🎬 جاري البحث وتحميل الإعلان الرسمي لـ: {target}")

    search_query = f"ytsearch1:{target}"
    
    # 1. تحميل الإعلان الحقيقي بجودة عالية
    cmd_download = [
        "yt-dlp",
        "-f", "bestvideo[height<=720][ext=mp4]/best[ext=mp4]/best",
        "--extractor-args", "youtube:player_client=android,web",
        "--max-filesize", "50M",
        "-o", "raw_trailer.mp4",
        search_query
    ]
    
    try:
        subprocess.run(cmd_download, check=True)
    except Exception as e:
        print(f"⚠️ فشل التحميل المباشر: {e}")
        return

    # 2. استخدام FFmpeg لقص الفيديو وتحويله إلى مقاس طولي (9:16) بدون صوت مبدئياً
    print("✂️ جاري قص الفيديو ومعالجته لمقاس شورتس وريلز (9:16)...")
    cmd_crop = [
        "ffmpeg", "-y",
        "-i", "raw_trailer.mp4",
        "-ss", "00:00:05",  # البدء بعد 5 ثوانٍ لتجاوز الشعار والمقدمة
        "-to", "00:00:30",  # جعل مدة الفيديو 25 ثانية فقط (مثالي للتيك توك والريلز)
        "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=720:1280",
        "-c:v", "libx264",
        "-preset", "fast",
        "-an",  # كتم الصوت الأصلي مبدئياً (بدون تعليق صوتي)
        "final_short.mp4"
    ]
    subprocess.run(cmd_crop, check=True)
    
    # حفظ وصف تسويقي جاهز للنسخ لنشر الفيديو مع روابط Jokar TV
    with open("description.txt", "w", encoding="utf-8") as f:
        f.write("🔥 لا تفوت مشاهدة أقوى الأفلام والمسلسلات بجودة عالية وبدون إعلانات حصرياً عبر تطبيق Jokar TV!\n\n📲 حمّل التطبيق الآن:\n🌐 الموقع الرسمي: https://jokartv.com\n🍏 للايفون (App Store): https://apps.apple.com/app/id1628995509\n\n#ملخصات_افلام #JokarTV #افلام #مسلسلات #اكسبلور #تيك_توك")

    print("✅ تم تجهيز الفيديو الحقيقي والاحترافي بنجاح!")

if __name__ == "__main__":
    download_and_process_trailer()
