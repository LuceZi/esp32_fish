import sounddevice as sd
import numpy as np
import queue

class Recorder:
    def __init__(self, samplerate=16000, channels=1, buffer_size=5):
        """初始化錄音模組"""
        self.samplerate = samplerate  # 取樣率
        self.channels = channels  # 聲道數（單聲道）
        self.is_recording = False  # 錄音狀態
        self.audio_queue = queue.Queue()  # 建立音訊佇列
        self.buffer = []  # 暫存音訊的 buffer，存放最近 buffer_size 秒的音訊
        self.buffer_size = buffer_size * samplerate  # 設定 buffer 大小

    def callback(self, indata, frames, time_info, status):
        """錄音回調函數，將音訊數據放入 queue 和 buffer"""
        if status:
            print(f"錄音錯誤: {status}", flush=True)

        # 轉換成 NumPy 陣列
        audio_data = np.frombuffer(indata, dtype=np.int16)

        # 存入 queue 供即時處理
        self.audio_queue.put(audio_data)

        # 存入 buffer，確保最多 buffer_size 秒的音訊
        self.buffer.extend(audio_data)
        if len(self.buffer) > self.buffer_size:
            self.buffer = self.buffer[-self.buffer_size:]  # 只保留最新的 buffer_size 秒音訊

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
        """取得 buffer 內的音訊數據（提供給語音辨識）"""
        return np.array(self.buffer, dtype=np.int16)

    def get_audio_from_queue(self):
        """從 queue 取得即時音訊數據（適合即時處理）"""
        if not self.audio_queue.empty():
            return self.audio_queue.get()
        return None

if __name__ == "__main__":
    try:
        # 創建錄音器
        recorder = Recorder(16000,1,20)

        # 啟動錄音
        recorder.start()

        # 讓它錄 10 秒
        input("按 Enter 鍵停止錄音...")
        recorder.stop()

        # 取得最近 5 秒的音訊
        audio_data = recorder.get_audio_buffer()
        print(f"獲取的音訊長度: {len(audio_data)}")
    
    except Exception as e:
        print(e)
        recorder.stop() # 確保錄音器被正確關閉
    