import vosk
import json
import numpy as np
import threading
import time
from audio.recorder import Recorder

class SpeechProcessor:
    def __init__(self, model_path="models/vosk_model",buffer_size=4, buffer_step=2):
        """初始化語音辨識模組"""
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.recorder = Recorder(buffer_size=buffer_size, buffer_step=buffer_step)  # ✅ 傳遞參數
        self.running = False  # 語音辨識狀態
        self.thread = None  # 處理語音辨識的執行緒
        self.command_callback  = None  # 處理語音辨識結果的回調函數

    def start_recording(self):
        """啟動錄音"""
        self.recorder.start()
        self.running = True
        self.thread = threading.Thread(target=self.process_audio_loop)
        self.thread.start()

    def stop_recording(self):
        """停止錄音"""
        self.running = False
        if self.thread:
            self.thread.join()
        self.recorder.stop()

    def process_audio_loop(self):
        """背景執行語音辨識"""
        while self.running:
            for i in range(self.recorder.buffer_step // self.recorder.samplerate):
                time.sleep(1)
                print(f"🕒 剩餘 {self.recorder.buffer_step//self.recorder.samplerate-i} 秒開始辨識...", end="\r")
            print("\r",end="")
            
            audio_data = self.recorder.get_audio_buffer()
            if len(audio_data) == 0:
                print("⚠️ 沒有音訊資料")
                continue

            # 轉換音訊為 bytes 格式
            audio_bytes = np.array(audio_data, dtype=np.int16).tobytes()

            if self.recognizer.AcceptWaveform(audio_bytes):
                result = json.loads(self.recognizer.Result())
                text = result["text"]
                print(f"📝 辨識結果: {text}")

                commands = {"前": "forward", "左": "left", "右": "right"}
                for word in commands:
                    if word in text:
                        command = commands[word]
                        print(f"✅ 偵測到指令: {commands[word]}")
                        if self.command_callback:
                            self.command_callback(command)
                        break
                else:
                    print(f"🔍 無法辨識指令：{text}")

            self.recorder.clear_old_audio()  # 清除已辨識的音訊

