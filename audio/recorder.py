import sounddevice as sd
import numpy as np
import queue
import threading
import time

class Recorder:
    def __init__(self, samplerate=16000, channels=1, buffer_size=5, buffer_step=2.5):
        """初始化錄音模組"""
        self.samplerate = samplerate  # 取樣率
        self.channels = channels  # 聲道數（單聲道）
        self.is_recording = False  # 錄音狀態
        self.audio_queue = queue.Queue()  # 建立音訊佇列
        self.buffer = []  # 暫存音訊的 buffer，存放最近 buffer_size 秒的音訊
        self.buffer_size = buffer_size * samplerate  # 設定 buffer 大小
        self.buffer_step = buffer_step * samplerate  # 設定 buffer 步長
        
        if buffer_size < buffer_step:
            raise ValueError("buffer_size 必須大於 buffer_step！")
        
        self.lock = threading.Lock()  # 創建鎖，避免多執行緒競爭

    def callback(self, indata, frames, time_info, status):
        """錄音回調函數，將音訊數據放入 queue 和 buffer"""
        if status:
            print(f"錄音錯誤: {status}", flush=True)

        # 轉換成 NumPy 陣列
        audio_data = np.frombuffer(indata, dtype=np.int16)

        if audio_data.shape == ():
            audio_data = np.array([audio_data], dtype=np.int16)

        with self.lock:
            self.buffer.extend(audio_data.tolist())

            if len(self.buffer) > self.buffer_size:
                self.buffer = self.buffer[-self.buffer_size:]  # ✅ 強制維持 buffer 長度
                
            print(f"\r🎤 已錄音 {len(self.buffer)} / {self.buffer_size} 樣本", end="", flush=True)

                
    def start(self):
        """開始錄音"""
        if not self.is_recording:
            print("🎤 開始錄音...")
            self.is_recording = True
            self.stream = sd.RawInputStream(
                samplerate=self.samplerate,
                channels=self.channels,
                dtype="int16",
                callback=self.callback
            )
            self.stream.start()
        else:
            print("⚠️ 錄音已經在進行中！")

    def stop(self):
        """停止錄音"""
        if self.is_recording:
            print("🛑 停止錄音...")
            self.is_recording = False
            self.stream.stop()
            self.stream.close()
        else:
            print("⚠️ 錄音已經停止！")

    def get_audio_buffer(self):
        """取得 buffer 內最近n秒 的音訊數據（提供給語音辨識）"""
        with self.lock:
            if len(self.buffer) < self.buffer_size:
                print(f"⚠️ 音訊 buffer 長度不足 ({len(self.buffer)}/{self.buffer_size})，使用現有音訊...")
                return np.array(self.buffer, dtype=np.int16)  # ✅ 改為使用現有音訊
            return np.array(self.buffer[-self.buffer_size:], dtype=np.int16)  # ✅ 正確切片

    def clear_old_audio(self):
        """清空舊的音訊數據"""
        with self.lock:
            if len(self.buffer) < self.buffer_step:
                print(f"⚠️ 音訊 buffer 長度不足 ({len(self.buffer)}/{self.buffer_size})，無法清除舊音訊...")
                return
            
            self.buffer = self.buffer[self.buffer_step:]

            # 確保 buffer 不會超過 buffer_size
            if len(self.buffer) > self.buffer_size:
                self.buffer = self.buffer[-self.buffer_size:]  # ✅ 強制維持 buffer 長度

    