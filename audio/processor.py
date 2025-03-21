import vosk
import json
import numpy as np
from audio.recorder import Recorder

class SpeechProcessor:
    def __init__(self, model_path="models/vosk_model"):
        """初始化語音辨識模組"""
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)  # 取樣率 16kHz
        self.recorder = Recorder()  # 建立錄音器

    def start_recording(self):
        """啟動錄音"""
        self.recorder.start()

    def stop_recording(self):
        """停止錄音"""
        self.recorder.stop()

    def get_command(self):
        """從錄音 buffer 取得語音指令"""
        audio_data = self.recorder.get_audio_buffer()  # 取得錄音 buffer
        if len(audio_data) == 0:
            return None  # 沒有音訊可辨識
        # 轉換音訊為 bytes 格式（符合 Vosk 需求）
        audio_bytes = np.array(audio_data, dtype=np.int16).tobytes()

        # 進行語音辨識
        if self.recognizer.AcceptWaveform(audio_bytes):
            result = json.loads(self.recognizer.Result())
            text = result["text"]  # 取得辨識文字（保持原樣）

            # 定義關鍵詞
            commands = {"前": "forward", "左": "left", "右": "right"}

            # **檢查 text 中是否包含任何關鍵詞**
            for word in commands:
                if word in text:  # 如果關鍵詞出現在 `text` 裡
                    return commands[word]  # 回傳對應的指令
            else:
                print(f"🔍 無法辨識指令：{text}")
        return None  # 沒有偵測到有效指令

