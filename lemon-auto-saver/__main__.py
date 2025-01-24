from .gui.main_window import MainWindow
import tkinter as tk
import os

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
    if os.path.exists(icon_path):
        root.iconphoto(True, tk.PhotoImage(file=icon_path))
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()