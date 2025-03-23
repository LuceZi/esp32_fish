import os
import time
import threading
from audio.recorder import Recorder
from audio.processor import SpeechProcessor
from control.control import Control
from audio.data_pool import Pool

# **全局狀態變數**
END_FLAG = False
RECORDING_FLAG = False
PROCEED_FINISH_FLAG = True
COMMAND_SEND_FLAG = False

recorder_status = "等待錄音..."
processor_status = "等待處理..."
control_status = "等待指令..."

# ✅ 創建錄音器、辨識器、控制器
recorder = Recorder()
speech_processor = SpeechProcessor()
control = Control()
pool = Pool()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def record_task(record_time = 5, refresh_time = 0.1):
    """錄音任務"""
    global RECORDING_FLAG, recorder_status
    while not END_FLAG:
        if not RECORDING_FLAG:
            RECORDING_FLAG = True
            recorder_status = f"🎤 錄音中... {record_time} 秒"
            audio_arr = recorder.record(record_time)
            pool.set_rec_data(audio_arr)
            recorder_status = "✅ 錄音完成      "
            RECORDING_FLAG = False
        time.sleep(refresh_time)

def proceed_task(refresh_time = 0.1):
    """處理任務"""
    global PROCEED_FINISH_FLAG, processor_status
    while not END_FLAG:        
        audio_arr = pool.get_rec_data()

        if audio_arr is None:
            time.sleep(refresh_time)
            continue  

        if PROCEED_FINISH_FLAG:
            PROCEED_FINISH_FLAG = False
            processor_status = "🎙️ 語音辨識中..."
            proc_data = speech_processor.process_audio(audio_arr)
            pool.set_proc_data(proc_data)
            processor_status = f"✅ 辨識結果: {proc_data}" if proc_data else "🔍 無法辨識"
            PROCEED_FINISH_FLAG = True
        
        time.sleep(refresh_time)

def send_command_task(refresh_time = 0.1):
    """發送指令任務"""
    global COMMAND_SEND_FLAG, control_status
    while not END_FLAG:
        proc_data = pool.get_proc_data()
        
        if proc_data is None:  # ✅ 避免變數未初始化錯誤
            time.sleep(refresh_time)
            continue
        
        if not COMMAND_SEND_FLAG:
            COMMAND_SEND_FLAG = True
            control_status = "🚀 發送指令中..."
            command = control.send_command(proc_data)
            if command:
                control_status = f"✅ 指令發送: {command}"
            else:
                control_status = "🔍 無法辨識指令"        
            COMMAND_SEND_FLAG = False
        
        time.sleep(refresh_time)

def console_display_task(refresh_time=0.5):
    """統一管理 Console 顯示，避免刷屏"""
    global recorder_status, processor_status, control_status
    rec_buffer = ""
    proc_buffer = ""
    ctrl_buffer = ""

    while not END_FLAG:    
        if ((rec_buffer!=recorder_status)|(proc_buffer!=proc_buffer)|(ctrl_buffer!=control_status)):
            clear_screen()
            print(f"\r{recorder_status} | {processor_status} | {control_status}", end="", flush=True)
        rec_buffer = recorder_status
        proc_buffer = processor_status
        ctrl_buffer = control_status
        time.sleep(refresh_time)

def main():
    print("🚀 啟動語音辨識系統...")    

    threading.Thread(target=record_task, args=(3,1) ,daemon=True).start()
    print("🎤 語音辨識系統啟動，正在暖機...")
    time.sleep(2)  # 等待錄音器初始化完成
    threading.Thread(target=proceed_task, daemon=True).start()
    time.sleep(2)  # 等待辨識器初始化完成
    threading.Thread(target=send_command_task, daemon=True).start()
    threading.Thread(target=console_display_task, args=(0.1, ), daemon=True).start()

    while True:
        time.sleep(1)  # 避免過度執行佔用 CPU

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\n🛑 停止語音辨識")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

    finally:
        END_FLAG = True
        control.close()
        time.sleep(1) # 等待執行緒結束
        print("🔚 程式結束 =====================================")
