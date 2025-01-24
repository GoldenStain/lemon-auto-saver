import pyautogui
from threading import Timer, Thread, Event
import psutil
import win32com.client
import logging
import pythoncom
from pywinauto import findwindows
from lemon_auto_saver.logger_config import setup_logger
from lemon_auto_saver.config.config import get_config_value

setup_logger()

class SaveWorker(Thread):
    def __init__(self, save_callback):
        super().__init__()
        self.save_callback = save_callback

    def run(self):
        pythoncom.CoInitialize()  # 初始化 COM 库
        self.save_callback()
        pythoncom.CoUninitialize()  # 取消初始化 COM 库

class AutoSaveManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.timer = None
        self.stop_event = Event()
        self.monitored_window = None

    def start_timer(self, interval):
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(interval, self.auto_save)
        self.timer.start()

    def stop(self):
        self.stop_event.set()
        if self.timer:
            self.timer.cancel()

    def auto_save(self):
        if self.main_window.auto_save_var.get():
            self.save_document()
        if not self.stop_event.is_set():
            self.start_timer(int(self.main_window.period_spinbox.get()))

    def get_active_window_process_info(self):
        try:
            active_window = findwindows.find_window(active_only=True)
            pid = findwindows.find_element(handle=active_window).process_id
            process = psutil.Process(pid)
            executable = process.exe()
            return pid, executable
        except Exception as e:
            logging.error(f"获取活动窗口信息时出错: {e}")
            return None, None

    def save_document(self):
        pid, executable = self.get_active_window_process_info()
        if pid and executable:
            if 'WINWORD.EXE' in executable:
                self.run_in_thread(self.save_word_document)
            elif 'EXCEL.EXE' in executable:
                self.run_in_thread(self.save_excel_document)
            elif 'POWERPNT.EXE' in executable:
                self.run_in_thread(self.save_powerpoint_document)
            elif self.monitored_window:
                self.run_in_thread(self.save_with_keys)
        else:
            logging.warning("无法获取当前活动窗口的进程信息")

    def save_word_document(self):
        try:
            word = win32com.client.Dispatch("Word.Application")
            for doc in word.Documents:
                logging.info(f"自动保存执行: Word 文档 {doc.Name} ({doc.FullName})")
                doc.Save()
                logging.info(f"Word 文档 {doc.Name} 已保存")
        except Exception as e:
            logging.error(f"保存 Word 文档时出错: {e}")

    def save_excel_document(self):
        try:
            excel = win32com.client.Dispatch("Excel.Application")
            for workbook in excel.Workbooks:
                logging.info(f"自动保存执行: Excel 工作簿 {workbook.Name} ({workbook.FullName})")
                workbook.Save()
                logging.info(f"Excel 工作簿 {workbook.Name} 已保存")
        except Exception as e:
            logging.error(f"保存 Excel 工作簿时出错: {e}")

    def save_powerpoint_document(self):
        try:
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            for presentation in powerpoint.Presentations:
                logging.info(f"自动保存执行: PowerPoint 演示文稿 {presentation.Name} ({presentation.FullName})")
                presentation.Save()
                logging.info(f"PowerPoint 演示文稿 {presentation.Name} 已保存")
        except Exception as e:
            logging.error(f"保存 PowerPoint 演示文稿时出错: {e}")

    def save_with_keys(self):
        try:
            active_window = findwindows.find_window(active_only=True)
            current_window = findwindows.find_element(handle=active_window).name
            if current_window == self.monitored_window:
                shortcut = get_config_value('save_shortcut')
                logging.info(f"自动保存执行: 使用快捷键 {shortcut} 保存当前窗口 {current_window}")
                keys = shortcut.split('+')
                pyautogui.hotkey(*keys)
                logging.info("使用快捷键保存文档")
        except Exception as e:
            logging.error(f"使用快捷键保存文档时出错: {e}")

    def run_in_thread(self, save_callback):
        worker = SaveWorker(save_callback)
        worker.start()

    def run(self):
        self.start_timer(int(self.main_window.period_spinbox.get()))
        self.stop_event.wait()  # 等待 stop_event 被设置