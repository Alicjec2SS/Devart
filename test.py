import numpy as np
import sounddevice as sd
import time
from datetime import datetime

# CẤU HÌNH THÔNG SỐ "BẮT CHÓ"
SAMPLE_RATE = 48000
THRESHOLD_DB = 75  # Ngưỡng ồn phạt (tính bằng dB)
DURATION_ALERT = 3  # Thời gian ồn vượt ngưỡng trước khi cảnh báo (giây)

# Biến toàn cục
noise_history = []
is_alerting = False

def audio_callback(indata, frames, time, status):
    global noise_history, is_alerting
    
    # Tính dB từ tín hiệu âm thanh
    rms = np.sqrt(np.mean(indata**2))
    db = 20 * np.log10(rms / (2**15)) + 94  # Chuyển đổi sang dB
    
    # Ghi nhận lịch sử ồn ào
    noise_history.append({
        'time': datetime.now(),
        'db': db,
        'raw_audio': indata.copy()
    })
    
    # Phát hiện "chó sủa" - vượt ngưỡng
    if db > THRESHOLD_DB:
        if not is_alerting:
            start_time = noise_history[-1]['time']
            # Kiểm tra nếu ồn kéo dài
            for entry in reversed(noise_history[:-1]):
                if (noise_history[-1]['time'] - entry['time']).seconds >= DURATION_ALERT:
                    if all(e['db'] > THRESHOLD_DB for e in noise_history[-DURATION_ALERT*10:]):
                        activate_punishment()
                        is_alerting = True
                        break
    else:
        is_alerting = False

def activate_punishment():
    """Kích hoạt hình phạt sáng tạo"""
    print("\n🚨 PHÁT HIỆN CHÓ SỒN! 🚨")
    print("THÔNG BÁO: Lớp học đang ồn ào quá mức cho phép!")
    
    # Tuỳ chọn hình phạt (bỏ comment để kích hoạt):
    # 1. Phát tiếng cảnh báo
    # sd.play(0.5 * np.sin(2 * np.pi * 1000 * np.arange(30000) / 48000), samplerate=48000)
    
    # 2. Ghi log vào file
    with open("noise_violations.log", "a") as f:
        f.write(f"{datetime.now()}: Noise violation - {max(e['db'] for e in noise_history[-30:])} dB\n")
    
    # 3. Gửi cảnh báo qua Telegram (cần cài thư viện python-telegram-bot)
    # send_telegram_alert()

# Khởi động hệ thống
print("🔥 HỆ THỐNG GIÁM SÁT TRẬT TỰ LỚP HỌC 🔥")
print(f"⚡ Đang theo dõi... Ngưỡng cảnh báo: {THRESHOLD_DB} dB")

with sd.InputStream(callback=audio_callback, samplerate=SAMPLE_RATE, channels=1):
    while True:
        time.sleep(1)
        # Hiển thị mức âm thanh hiện tại
        current_db = noise_history[-1]['db'] if noise_history else 0
        print(f"\rMức ồn hiện tại: {current_db:.1f} dB", end="", flush=True)