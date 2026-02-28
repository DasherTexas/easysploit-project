import customtkinter as ctk
import subprocess
import platform

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

MSF = "msfconsole"

class EasySploit(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("easySploit")
        self.geometry("1100x700")

        self.target = ctk.StringVar()

        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="easySploit", font=("Consolas", 22)).pack(pady=15)

        ctk.CTkEntry(self.sidebar, textvariable=self.target, placeholder_text="TARGET IP").pack(pady=10, padx=10)

        self.add_btn("Port Scan", "auxiliary/scanner/portscan/tcp")
        self.add_btn("SMB Scan", "auxiliary/scanner/smb/smb_version")
        self.add_btn("FTP Login", "auxiliary/scanner/ftp/ftp_login")
        self.add_btn("Multi Handler", "exploit/multi/handler")

        ctk.CTkButton(self.sidebar, text="Sessions",
                      command=lambda: self.run_msf("sessions")).pack(pady=10, fill="x")

        self.main = ctk.CTkFrame(self)
        self.main.pack(expand=True, fill="both")

        self.terminal = ctk.CTkTextbox(self, height=150)
        self.terminal.pack(fill="x")

    def add_btn(self, name, module):
        ctk.CTkButton(self.sidebar, text=name,
                      command=lambda: self.load_module(module)).pack(pady=5, fill="x")

    # =============================

    def run_msf(self, command):
        self.terminal.insert("end", f"\n> {command}\n")
        subprocess.Popen([MSF, "-q", "-x", command])

    # =============================

    def load_module(self, module):

        for w in self.main.winfo_children():
            w.destroy()

        ctk.CTkLabel(self.main, text=module, font=("Consolas", 18)).pack(pady=10)

        output = subprocess.getoutput(f"{MSF} -q -x 'use {module}; show options; exit'")

        self.entries = {}

        for line in output.split("\n"):
            if "required" in line.lower():
                parts = line.split()
                opt = parts[0]

                frame = ctk.CTkFrame(self.main)
                frame.pack(fill="x", padx=20, pady=2)

                ctk.CTkLabel(frame, text=opt, width=150, anchor="w").pack(side="left")

                entry = ctk.CTkEntry(frame)
                entry.pack(side="right", expand=True, fill="x")

                if opt.upper() == "RHOSTS" and self.target.get():
                    entry.insert(0, self.target.get())

                self.entries[opt] = entry

        ctk.CTkButton(self.main, text="RUN", fg_color="green",
                      command=lambda: self.execute(module)).pack(pady=15)

    # =============================

    def execute(self, module):

        cmd = f"use {module}; "

        for opt, entry in self.entries.items():
            val = entry.get()
            if val:
                cmd += f"set {opt} {val}; "

        cmd += "run"

        self.run_msf(cmd)

# =============================

if __name__ == "__main__":
    print("Running on:", platform.system())
    app = EasySploit()
    app.mainloop()