import os
import subprocess
import random
import urllib.request

# قائمة روابط لفيديوهات سينمائية حقيقية ومباشرة (بدون مشاكل حظر يوتيوب)
DIRECT_VIDEOS = [
    "https://assets.mixkit.co/videos/preview/mixkit-hands-holding-a-smartphone-with-a-green-screen-42998-large.mp4",
    "https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-screens-42838-large.mp4",
    "https://assets.mixkit.co/videos/preview/mixkit-set-of-plate-lets-go-neon-sign-42982-large.mp4",
    "https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-city-traffic-at-night-41526-large.mp4",
    "https://assets.mixkit.co/videos/preview/mixkit-cinematic-digital-background-animation-42841-large.mp4"
]

def process_direct_video():
    # اختيار فيديو حقيقي عشوائي
    video_url = random.choice(DIRECT_VIDEOS)
    print(f"🎬 جاري تحميل الفيديو الأصلي المباشر...")

    input_file = "raw_video.mp4"
    output_file = "final_short.mp4"

    # تحميل ملف الفيديو المباشر
    req = urllib.request.Request(
        video_url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    try:
        with urllib.request.urlopen(req) as response, open(input_file, 'wb') as out_file:
            out_file.write(response.read())
    except Exception as e:
        print(f"⚠️ خطأ في التحميل المباشر: {e}")
        return

    # معالجة الفيديو وقصه إلى مقاس طولي (9:16) احترافي للريلز والتيك توك
    print("✂️ جاري معالجة وقص الفيديو للمقاس الطولي (9:16)...")
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=720:1280",
        "-t", "25",  # مدة الفيديو 25 ثانية
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-an",  # بدون صوت لتركيب ترندات المنصات لاحقاً
        output_file
    ]
    subprocess.run(cmd_ffmpeg, check=True)

    # حفظ الوصف التسويقي الجاهز للنسخ في ملف description.txt مع روابط Jokar TV وموقعنا jokartv.com
    with open("description.txt", "w", encoding="utf-8") as f:
        f.write("🔥 لا تفوت مشاهدة أقوى الأفلام والمسلسلات بجودة عالية وبدون إعلانات حصرياً عبر تطبيق Jokar TV!\n\n📲 حمّل التطبيق الآن:\n🌐 الموقع الرسمي: https://jokartv.com\n🍏 للايفون (App Store): https://apps.apple.com/app/id1628995509\n\n#ملخصات_افلام #JokarTV #افلام #مسلسلات #اكسبلور #تيك_توك #سينما")

    print("✅ تم تجهيز الفيديو الأصلي الحقيقي والوصف بنجاح تام!")

if __name__ == "__main__":
    process_direct_video()
