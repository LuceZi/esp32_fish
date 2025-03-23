# 🎤 聲控機器魚（Voice-Controlled Robotic Fish）

## 📌 專案簡介
本專案旨在開發一個 **透過語音指令控制的機器魚**，
透過電腦端辨識語音指令，並透過 ESP32 控制機器魚的行為。
目前支援的語音指令包含：
✅ **前進**
✅ **左轉**
✅ **右轉**

本專案採用 **模組化設計**，確保未來可以擴展更多功能，例如 **藍牙通訊** 或 **有線通訊**。

---

## 📁 專案架構
```
voice_control_fish/  # 專案根目錄
│── main.py          # 主程式，負責語音辨識與控制機器魚
│── config.py        # 設定檔（包含模型路徑與參數）
│── requirements.txt # 依賴庫列表（pip 安裝用）
│── models/          # 語音模型存放處
│   ├── vosk_model/  # Vosk 語音辨識模型（請手動下載）
│── audio/           # 音訊處理模組
│   ├── recorder.py  # 負責錄音
│   ├── processor.py # 語音辨識處理
│   ├── data_pool.py # 資料池
│── control/         # 控制機器魚
│   ├── control.py   # 發指令
│── utils/           # 工具函數（如日誌、錯誤處理）
│   ├── logger.py    # 日誌紀錄
│   ├── helper.py    # 其他輔助函數
│── tests/           # 測試用例
│   ├── test_audio.py  # 測試音訊模組
│   ├── test_control.py # 測試控制指令
│── README.md        # 本文件
```

---

## 🔹 環境設定與安裝
### **1️⃣ 安裝 Python 依賴**
請確保你已安裝 Python，然後執行：
```sh
pip install -r requirements.txt
```

### **2️⃣ 下載 Vosk 中文語音模型**
由於 Vosk 語音模型較大，請手動下載並放入 `models/` 目錄內：
```sh
models/
├── vosk_model/  # 這裡放模型檔案
```
📥 **[下載 Vosk 中文模型](https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip)**

### **3️⃣ 執行 `main.py` 測試語音辨識**
```sh
python main.py
```
說出 **「前進」、「左轉」、「右轉」**，確認辨識效果。

---

## 🚀 未來擴展
- ✅ **ESP32 通訊整合（藍牙 / 有線）**
- ✅ **多語音指令支援**
- ✅ **更強的雜訊過濾與準確度優化**

歡迎大家一起參與這個專案！🐟🎤