import threading

class Pool:
    def __init__(self):
        """初始化 Pool，提供 rec_data (錄音資料) 和 proc_data (辨識結果)，並加入 flag 機制"""
        self.lock = threading.Lock()
        self.rec_data = None  # 存放錄音資料
        self.proc_data = None  # 存放語音辨識結果
        self.new_rec_flag = False  # 是否有新錄音資料
        self.proc_flag = False  # 是否有新辨識結果

    def set_rec_data(self, data):
        """存入錄音資料，並 raise `new_rec_flag`"""
        with self.lock:
            self.rec_data = data
            self.new_rec_flag = True  # ✅ Raise Flag

    def get_rec_data(self):
        """取出錄音資料，並 `reset new_rec_flag`"""
        with self.lock:
            if not self.new_rec_flag:
                return None  # ❌ 沒有新音訊
            data = self.rec_data
            self.new_rec_flag = False  # ✅ Reset Flag
        return data

    def set_proc_data(self, data):
        """存入辨識結果，並 raise `proc_flag`"""
        with self.lock:
            self.proc_data = data
            self.proc_flag = True  # ✅ Raise Flag

    def get_proc_data(self):
        """取出辨識結果，並 `reset proc_flag`"""
        with self.lock:
            if not self.proc_flag:
                return None  # ❌ 沒有新辨識結果
            data = self.proc_data
            self.proc_flag = False  # ✅ Reset Flag
        return data
