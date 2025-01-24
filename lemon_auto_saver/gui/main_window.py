import tkinter as tk
from tkinter import ttk
from threading import Thread
from lemon_auto_saver.config.config import set_config_value, get_config_value
from lemon_auto_saver.backend.auto_save import AutoSaveManager
import pygetwindow as gw
from lemon_auto_saver.logger_config import setup_logger
import logging

setup_logger()


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Save!")
        self.initUI()
        self.auto_save_manager = AutoSaveManager(self)
        self.auto_save_thread = Thread(target=self.auto_save_manager.run)
        self.auto_save_thread.start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def initUI(self):
        self.auto_save_var = tk.BooleanVar()
        self.auto_save_checkbox = tk.Checkbutton(self.root, text='启用自动保存', variable=self.auto_save_var, command=self.save_configuration)
        self.auto_save_checkbox.grid(row=0, column=0, sticky='w')

        self.period_label = tk.Label(self.root, text='自动保存间隔（秒）：')
        self.period_label.grid(row=1, column=0, sticky='w')

        self.period_spinbox = tk.Spinbox(self.root, from_=1, to=3600, command=self.save_configuration)
        self.period_spinbox.grid(row=1, column=1, sticky='w')
        self.period_spinbox.bind("<KeyRelease>", self.save_configuration)  # 绑定键盘事件

        self.shortcut_label = tk.Label(self.root, text='自定义保存快捷键：')
        self.shortcut_label.grid(row=2, column=0, sticky='w')

        self.shortcut_entry = tk.Entry(self.root)
        self.shortcut_entry.grid(row=2, column=1, sticky='w')

        self.set_shortcut_button = tk.Button(self.root, text='设置快捷键', command=self.set_shortcut)
        self.set_shortcut_button.grid(row=2, column=2, sticky='w')

        self.select_window_button = tk.Button(self.root, text='选择要监控的窗口', command=self.populate_window_list)
        self.select_window_button.grid(row=3, column=0, sticky='w')

        self.window_combo_box = ttk.Combobox(self.root)
        self.window_combo_box.grid(row=4, column=0, sticky='w')
        self.window_combo_box.bind("<<ComboboxSelected>>", self.window_selected)

        # Load initial configuration
        self.load_configuration()

    def load_configuration(self):
        self.auto_save_var.set(get_config_value('auto_save_enabled'))
        self.period_spinbox.delete(0, 'end')
        self.period_spinbox.insert(0, get_config_value('auto_save_period'))
        self.shortcut_entry.delete(0, 'end')
        self.shortcut_entry.insert(0, get_config_value('save_shortcut'))

    def save_configuration(self, event=None):
        set_config_value('auto_save_enabled', self.auto_save_var.get())
        set_config_value('auto_save_period', int(self.period_spinbox.get()))
        set_config_value('save_shortcut', self.shortcut_entry.get())
        logging.info("配置已保存")
        self.auto_save_manager.start_timer(int(self.period_spinbox.get()))

    def set_shortcut(self):
        self.shortcut_entry.delete(0, 'end')
        self.shortcut_entry.insert(0, "按下快捷键...")
        self.root.bind("<KeyPress>", self.record_shortcut)

    def record_shortcut(self, event):
        keysym = event.keysym
        if keysym not in ["Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R"]:
            shortcut = []
            if event.state & 0x0001:
                shortcut.append("shift")
            if event.state & 0x0004:
                shortcut.append("ctrl")
            if event.state & 0x0008:
                shortcut.append("alt")
            shortcut.append(keysym)
            shortcut_str = "+".join(shortcut)
            self.shortcut_entry.delete(0, 'end')
            self.shortcut_entry.insert(0, shortcut_str)
            self.root.unbind("<KeyPress>")
            self.save_configuration()
            logging.info(f"已设置自定义保存快捷键: {shortcut_str}")

    def populate_window_list(self):
        windows = gw.getAllTitles()
        self.window_combo_box['values'] = [window for window in windows if window]
        logging.info("窗口列表已更新")

    def window_selected(self, event):
        selected_window = self.window_combo_box.get()
        if selected_window:
            logging.info(f"选择的监控窗口: {selected_window}")
            self.auto_save_manager.monitored_window = selected_window  # 设置监控窗口

    def on_closing(self):
        self.auto_save_manager.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()