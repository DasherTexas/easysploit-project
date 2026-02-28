import customtkinter as ctk
import subprocess
import platform
import sys
import requests
import time

ctk.set_appearance_mode("dark")

MSF = "msfconsole"

ASCII = """
███████╗ █████╗ ███████╗██╗   ██╗███████╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
█████╗  ███████║███████╗ ╚████╔╝ █████╗  ██████╔╝██║     ██║   ██║██║   ██║
██╔══╝  ██╔══██║╚════██║  ╚██╔╝  ██╔══╝  ██╔═══╝ ██║     ██║   ██║██║   ██║
███████╗██║  ██║███████║   ██║   ███████╗██║     ███████╗╚██████╔╝██║   ██║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═════╝ ╚═════╝ ╚═╝   ╚═╝
"""

class EasySploit(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("1100x720")
        self.title("easySploit")

        # TARGET BAR
        self.target = ctk.CTkEntry(self, placeholder_text="TARGET")
        self.target.pack(fill="x", padx=10, pady=5)

        # MENU
        menu = ctk.CTkFrame(self)
        menu.pack(pady=5)

        buttons = ["HOME","PAYLOADS","EXPLOITS","SCANNERS","SESSIONS",
                   "WEB TEST","MSFCONSOLE","HELP","DEBUG"]

        for name in buttons:
            ctk.CTkButton(menu, text=name,
                          command=lambda n=name: self.load(n)).pack(side="left", padx=4)

        # ASCII BANNER
        self.banner = ctk.CTkTextbox(self, height=200)
        self.banner.pack(fill="x", padx=10)
        self.banner.insert("0.0", ASCII)

        # MAIN PANEL
        self.main = ctk.CTkScrollableFrame(self)
        self.main.pack(expand=True, fill="both", padx=10, pady=10)

        self.home()

    # ================= HOME =================

    def home(self):

        for w in self.main.winfo_children():
            w.destroy()

        status = self.check_msf()

        ctk.CTkLabel(self.main, text="WELCOME TO easySploit", font=("Consolas", 20)).pack(pady=10)
        ctk.CTkLabel(self.main, text=f"Metasploit Status: {status}").pack(pady=5)
        ctk.CTkLabel(self.main, text=f"OS: {platform.system()}").pack(pady=5)
        ctk.CTkLabel(self.main, text=f"Python: {sys.version.split()[0]}").pack(pady=5)

        ctk.CTkButton(self.main, text="Start msfconsole",
                      command=lambda: subprocess.Popen([MSF])).pack(pady=10)

    # ================= MENU LOADER =================

    def load(self, section):

        if section == "HOME":
            self.home()
            return

        for w in self.main.winfo_children():
            w.destroy()

        if section == "PAYLOADS":
            data = self.msf("show payloads")

        elif section == "EXPLOITS":
            data = self.msf("search type:exploit")

        elif section == "SCANNERS":
            data = self.msf("search type:auxiliary")

        elif section == "SESSIONS":
            subprocess.Popen([MSF, "-q", "-x", "sessions"])
            return

        elif section == "WEB TEST":
            self.web_test_ui()
            return

        elif section == "MSFCONSOLE":
            subprocess.Popen([MSF])
            return

        elif section == "HELP":
            data = self.help_text()

        elif section == "DEBUG":
            data = self.debug_info()

        else:
            data = ""

        box = ctk.CTkTextbox(self.main)
        box.pack(expand=True, fill="both")
        box.insert("0.0", data)

    # ================= MSF =================

    def msf(self, cmd):
        return subprocess.getoutput(f"{MSF} -q -x '{cmd}; exit'")

    def check_msf(self):
        try:
            out = subprocess.getoutput(f"{MSF} -v")
            return "🟢 READY" if "Framework" in out else "🔴 NOT FOUND"
        except:
            return "🔴 NOT FOUND"

    # ================= HELP =================

    def help_text(self):
        return """
scan → find service → exploit → session → post

PAYLOADS = shells
EXPLOITS = break in
SCANNERS = discovery
SESSIONS = control target
WEB TEST = test your website security
"""

    # ================= DEBUG =================

    def debug_info(self):

        pip = subprocess.getoutput("python -m pip --version")

        msf = subprocess.getoutput(f"{MSF} -v")

        return f"""
OS: {platform.system()}
Python: {sys.version}

Pip:
{pip}

Metasploit:
{msf}
"""

    # ================= WEB TEST =================

    def web_test_ui(self):

        url = ctk.CTkEntry(self.main, placeholder_text="https://target-site.com")
        url.pack(fill="x", pady=5)

        output = ctk.CTkTextbox(self.main, height=350)
        output.pack(expand=True, fill="both", pady=10)

        def status():
            try:
                start = time.time()
                r = requests.get(url.get(), timeout=10)
                ms = round((time.time() - start) * 1000, 2)
                output.insert("end", f"\nStatus: {r.status_code} | {ms} ms\n")
            except Exception as e:
                output.insert("end", f"\nError: {e}\n")

        def headers():
            try:
                r = requests.get(url.get(), timeout=10)
                output.insert("end", "\n--- HEADERS ---\n")
                for h in ["Content-Security-Policy","X-Frame-Options",
                          "Strict-Transport-Security"]:
                    output.insert("end", f"{h}: {r.headers.get(h,'Missing')}\n")
            except Exception as e:
                output.insert("end", f"\nError: {e}\n")

        ctk.CTkButton(self.main, text="Check Status", command=status).pack(pady=2)
        ctk.CTkButton(self.main, text="Analyze Headers", command=headers).pack(pady=2)

# ================= RUN =================

EasySploit().mainloop()
