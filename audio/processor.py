import vosk
import json
import numpy as np

class SpeechProcessor:
    def __init__(self, model_path="models/vosk_model"):
        """初始化語音辨識模組"""
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)

    def process_audio(self, audio_arr):
        """處理音訊陣列，並回傳辨識結果"""
        #print("🎙️ 進行語音辨識...")
        audio_bytes = np.array(audio_arr, dtype=np.int16).tobytes()

        text = ""
        if self.recognizer.AcceptWaveform(audio_bytes):
            result = json.loads(self.recognizer.Result())
            text = result["text"]
            
        #print(f"📝 辨識結果: {text}")
        return text  # ✅ 直接回傳數據，讓 `main.py` 處理
            
