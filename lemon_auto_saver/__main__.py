import sys
import os
# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取父目录（上一级目录）
parent_dir = os.path.dirname(current_dir)

# 将父目录插入 sys.path
sys.path.insert(0, parent_dir)

from lemon_auto_saver.gui.main_window import MainWindow
import tkinter as tk

from .logger_config import LOG_FILE_PATH, setup_logger
MAX_LOG_SIZE = 1 * 1024 * 1024  # 1MB

def check_log_file_size():
    if os.path.exists(LOG_FILE_PATH):
        if os.path.getsize(LOG_FILE_PATH) > MAX_LOG_SIZE:
            with open(LOG_FILE_PATH, 'w') as log_file:
                log_file.truncate(0)
            print(f"日志文件 {LOG_FILE_PATH} 超过 1MB，已清空")

def main():
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    setup_logger()
    check_log_file_size()
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()