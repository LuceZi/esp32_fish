import sounddevice as sd
import numpy as np

class Recorder:
    def __init__(self, samplerate=16000, channels=1):
        """初始化錄音器"""
        self.samplerate = samplerate
        self.channels = channels

    def record(self, duration):
        """錄製指定秒數的音訊，並回傳 NumPy 陣列"""
        #print(f"🎤 開始錄音 ({duration} 秒)...")
        audio = sd.rec(int(self.samplerate * duration), samplerate=self.samplerate, channels=self.channels, dtype="int16")
        sd.wait()  # 等待錄音完成
        audio_arr = np.squeeze(audio)  # 轉成一維 NumPy 陣列

        #print(f"🛑 錄音結束，回傳音訊")
        return audio_arr  # ✅ 直接回傳數據，讓 `main.py` 處理
    