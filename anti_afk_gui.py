import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import win32gui
import win32con
import win32api
from datetime import datetime

class AntiAFKApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Anti-AFK")
        self.root.geometry("380x320")
        self.root.resizable(False, False)
        
        # State Variables
        self.is_running = False
        self.hwnd = None
        self.worker_thread = None
        self.countdown_val = 0
        
        # Minimalist Dark Theme
        self.bg_color = "#121214"
        self.card_bg = "#1a1a1e"
        self.text_color = "#f3f4f6"
        self.accent_green = "#10b981"
        self.accent_red = "#ef4444"
        self.gray_text = "#9ca3af"
        
        self.root.configure(bg=self.bg_color)
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color, pady=10)
        header_frame.pack(fill="x")
        
        title_label = tk.Label(
            header_frame, 
            text="Roblox Anti-AFK", 
            font=("Segoe UI", 13, "bold"), 
            bg=self.bg_color, 
            fg=self.text_color
        )
        title_label.pack()

        # Main Controller Card
        card_frame = tk.Frame(self.root, bg=self.card_bg, bd=0, padx=15, pady=15)
        card_frame.pack(fill="x", padx=15, pady=5)
        
        # Status Row
        status_row = tk.Frame(card_frame, bg=self.card_bg)
        status_row.pack(fill="x", pady=(0, 4))
        
        status_title = tk.Label(
            status_row, 
            text="Status:", 
            font=("Segoe UI", 10), 
            bg=self.card_bg, 
            fg=self.gray_text
        )
        status_title.pack(side="left")
        
        self.status_label = tk.Label(
            status_row, 
            text="Inactive", 
            font=("Segoe UI", 10, "bold"), 
            bg=self.card_bg, 
            fg=self.accent_red
        )
        self.status_label.pack(side="left", padx=5)
        
        # Details
        self.timer_label = tk.Label(
            card_frame, 
            text="Next action: --", 
            font=("Segoe UI", 9), 
            bg=self.card_bg, 
            fg=self.gray_text
        )
        self.timer_label.pack(anchor="w", pady=(0, 15))
        
        # Toggle Button
        self.toggle_btn = tk.Button(
            card_frame,
            text="Start",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_green,
            fg="#121214",
            activebackground="#059669",
            activeforeground="#ffffff",
            bd=0,
            pady=6,
            cursor="hand2",
            command=self.toggle_anti_afk
        )
        self.toggle_btn.pack(fill="x")
        
        # Logs Section
        log_frame = tk.Frame(self.root, bg=self.bg_color)
        log_frame.pack(fill="both", expand=True, padx=15, pady=(15, 15))
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.log_listbox = tk.Listbox(
            log_frame, 
            bg="#18181b", 
            fg=self.text_color, 
            bd=0, 
            highlightthickness=0,
            font=("Consolas", 8),
            yscrollcommand=scrollbar.set
        )
        self.log_listbox.pack(fill="both", expand=True, side="left")
        scrollbar.config(command=self.log_listbox.yview)
        
        self.add_log("Application ready.")
        
    def add_log(self, text):
        now = datetime.now().strftime("%H:%M:%S")
        self.log_listbox.insert(tk.END, f"[{now}] {text}")
        self.log_listbox.see(tk.END)
        
    def cari_jendela_roblox(self):
        hwnd = win32gui.FindWindow(None, "Roblox")
        if not hwnd:
            def callback(h, extra):
                title = win32gui.GetWindowText(h)
                if "roblox" in title.lower():
                    extra.append(h)
                return True
            hwnds = []
            win32gui.EnumWindows(callback, hwnds)
            if hwnds:
                hwnd = hwnds[0]
        return hwnd

    def toggle_anti_afk(self):
        if not self.is_running:
            self.hwnd = self.cari_jendela_roblox()
            if not self.hwnd:
                messagebox.showerror(
                    "Error", 
                    "Roblox window not found! Please open the game first."
                )
                return
                
            self.is_running = True
            self.status_label.config(text="Active", fg=self.accent_green)
            self.toggle_btn.config(text="Stop", bg=self.accent_red, fg=self.text_color)
            self.add_log("Anti-AFK activated.")
            
            self.worker_thread = threading.Thread(target=self.afk_worker, daemon=True)
            self.worker_thread.start()
        else:
            self.is_running = False
            self.status_label.config(text="Inactive", fg=self.accent_red)
            self.timer_label.config(text="Next action: --")
            self.toggle_btn.config(text="Start", bg=self.accent_green, fg="#121214")
            self.add_log("Anti-AFK deactivated.")

    def kirim_mouse_jiggle_background(self):
        """Mengirim pergerakan dan klik mouse di background tanpa memindahkan kursor fisik user."""
        if self.hwnd:
            try:
                # Dapatkan koordinat tengah jendela Roblox secara dinamis
                rect = win32gui.GetClientRect(self.hwnd)
                width = rect[2]
                height = rect[3]
                
                # Buat koordinat acak di sekitar tengah layar
                x = random.randint(int(width * 0.4), int(width * 0.6))
                y = random.randint(int(height * 0.4), int(height * 0.6))
                lParam = (y << 16) | x
                
                # 1. Kirim gerakan mouse
                win32api.PostMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, lParam)
                time.sleep(0.05)
                
                # 2. Kirim Klik Kanan (sangat aman di Roblox dan terbukti mereset timer AFK)
                win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
                time.sleep(0.05)
                win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONUP, 0, lParam)
                
                self.add_log(f"Jiggled mouse at ({x}, {y}) in background.")
            except Exception as e:
                self.add_log(f"Jiggle failed: {str(e)}")

    def afk_worker(self):
        first_run = True
        
        while self.is_running:
            if first_run:
                jeda = 10
                first_run = False
            else:
                jeda = random.randint(120, 240)
                
            self.countdown_val = jeda
            
            while self.countdown_val > 0 and self.is_running:
                self.root.after(0, self.update_timer_ui, self.countdown_val)
                time.sleep(1)
                self.countdown_val -= 1
            
            if self.is_running:
                self.kirim_mouse_jiggle_background()
                
        self.root.after(0, self.update_timer_ui, 0)

    def update_timer_ui(self, val):
        if val > 0:
            menit = val // 60
            detik = val % 60
            self.timer_label.config(text=f"Next action in: {menit:02d}:{detik:02d}")
        else:
            self.timer_label.config(text="Sending action...")

if __name__ == "__main__":
    root = tk.Tk()
    app = AntiAFKApp(root)
    root.mainloop()
