import customtkinter as ctk
import subprocess
import platform
import sys
import requests
import time

ctk.set_appearance_mode("dark")

MSF = "msfconsole"

ASCII_BANNER = """
███████╗ █████╗ ███████╗██╗   ██╗███████╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
█████╗  ███████║███████╗ ╚████╔╝ █████╗  ██████╔╝██║     ██║   ██║██║   ██║
██╔══╝  ██╔══██║╚════██║  ╚██╔╝  ██╔══╝  ██╔═══╝ ██║     ██║   ██║██║   ██║
███████╗██║  ██║███████║   ██║   ███████╗██║     ███████╗╚██████╔╝██║   ██║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝
"""

HELP_TEXT = """
PAYLOADS → List all Metasploit payloads.
SCANNERS → Network discovery & service scanning modules.
EXPLOITS → Vulnerability exploitation modules.
SESSIONS → View active shells.
WEB TEST → Website security testing panel (safe & legal).
TARGET FIELD → Used by modules that require RHOSTS.
TIP → Always start a handler before running reverse payloads.
"""

class EasySploitGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("easySploit")
        self.geometry("1100x720")

        # Target entry
        self.target_entry = ctk.CTkEntry(self, placeholder_text="TARGET")
        self.target_entry.pack(fill="x", padx=10, pady=5)

        # Menu
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack(pady=5)

        self.buttons = [
            "HOME","PAYLOADS","EXPLOITS","SCANNERS",
            "SESSIONS","WEB TEST","MSFCONSOLE","HELP","DEBUG"
        ]

        for btn in self.buttons:
            ctk.CTkButton(self.menu_frame, text=btn, width=120,
                          command=lambda b=btn: self.load_menu(b)).pack(side="left", padx=3)

        # ASCII banner
        self.banner = ctk.CTkTextbox(self, height=180)
        self.banner.pack(fill="x", padx=10)
        self.banner.insert("0.0", ASCII_BANNER)
        self.banner.configure(state="disabled")  # prevent editing

        # Main content panel
        self.main_panel = ctk.CTkScrollableFrame(self)
        self.main_panel.pack(expand=True, fill="both", padx=10, pady=10)

        self.load_menu("HOME")

    # ----------------- MENU LOADER -----------------
    def load_menu(self, menu_name):
        # Clear main panel
        for widget in self.main_panel.winfo_children():
            widget.destroy()

        # Decide what to show
        if menu_name == "HOME":
            self.show_home()
        elif menu_name == "PAYLOADS":
            self.show_payloads()
        elif menu_name == "EXPLOITS":
            self.show_exploits()
        elif menu_name == "SCANNERS":
            self.show_scanners()
        elif menu_name == "SESSIONS":
            self.show_sessions()
        elif menu_name == "WEB TEST":
            self.show_web_test()
        elif menu_name == "MSFCONSOLE":
            subprocess.Popen([MSF])
        elif menu_name == "HELP":
            self.show_help()
        elif menu_name == "DEBUG":
            self.show_debug()

    # ----------------- HOME -----------------
    def show_home(self):
        ctk.CTkLabel(self.main_panel, text="WELCOME TO easySploit", font=("Consolas", 20)).pack(pady=10)
        msf_status = self.check_msf()
        ctk.CTkLabel(self.main_panel, text=f"Metasploit Status: {msf_status}").pack(pady=5)
        ctk.CTkLabel(self.main_panel, text=f"OS: {platform.system()}").pack(pady=5)
        ctk.CTkLabel(self.main_panel, text=f"Python: {sys.version.split()[0]}").pack(pady=5)
        ctk.CTkButton(self.main_panel, text="Launch Metasploit Console",
                      command=lambda: subprocess.Popen([MSF])).pack(pady=10)

    # ----------------- HELP -----------------
    def show_help(self):
        box = ctk.CTkTextbox(self.main_panel)
        box.pack(expand=True, fill="both")
        box.insert("0.0", HELP_TEXT)
        box.configure(state="disabled")

    # ----------------- DEBUG -----------------
    def show_debug(self):
        info = f"OS: {platform.system()} {platform.release()}\n"
        info += f"Python: {sys.version}\n"
        pip_version = subprocess.getoutput("python -m pip --version")
        info += f"Pip: {pip_version}\n"
        try:
            msf_version = subprocess.getoutput(f"{MSF} -v")
        except:
            msf_version = "Metasploit not found"
        info += f"Metasploit:\n{msf_version}"

        box = ctk.CTkTextbox(self.main_panel)
        box.pack(expand=True, fill="both")
        box.insert("0.0", info)
        box.configure(state="disabled")

    # ----------------- PAYLOADS -----------------
    def show_payloads(self):
        data = subprocess.getoutput(f"{MSF} -q -x 'show payloads; exit'")
        self.show_textbox(data, back=True)

    # ----------------- EXPLOITS -----------------
    def show_exploits(self):
        data = subprocess.getoutput(f"{MSF} -q -x 'search type:exploit; exit'")
        self.show_textbox(data, back=True)

    # ----------------- SCANNERS -----------------
    def show_scanners(self):
        data = subprocess.getoutput(f"{MSF} -q -x 'search type:auxiliary; exit'")
        self.show_textbox(data, back=True)

    # ----------------- SESSIONS -----------------
    def show_sessions(self):
        subprocess.Popen([MSF, "-q", "-x", "sessions"])

    # ----------------- WEB TEST -----------------
    def show_web_test(self):
        url_entry = ctk.CTkEntry(self.main_panel, placeholder_text="https://example.com")
        url_entry.pack(fill="x", pady=5)

        output = ctk.CTkTextbox(self.main_panel, height=300)
        output.pack(expand=True, fill="both", pady=10)

        def check_status():
            try:
                start = time.time()
                r = requests.get(url_entry.get(), timeout=10)
                ms = round((time.time()-start)*1000,2)
                output.insert("end", f"Status: {r.status_code} | {ms} ms\n")
            except Exception as e:
                output.insert("end", f"Error: {e}\n")

        def check_headers():
            try:
                r = requests.get(url_entry.get(), timeout=10)
                output.insert("end", "\n--- HEADERS ---\n")
                for h in ["Content-Security-Policy","Strict-Transport-Security","X-Frame-Options"]:
                    output.insert("end", f"{h}: {r.headers.get(h,'Missing')}\n")
            except Exception as e:
                output.insert("end", f"Error: {e}\n")

        ctk.CTkButton(self.main_panel, text="Check Status", command=check_status).pack(pady=2)
        ctk.CTkButton(self.main_panel, text="Analyze Headers", command=check_headers).pack(pady=2)

        ctk.CTkButton(self.main_panel, text="Back", command=lambda: self.load_menu("HOME")).pack(pady=5)

    # ----------------- HELPER FUNCTIONS -----------------
    def show_textbox(self, text, back=False):
        box = ctk.CTkTextbox(self.main_panel)
        box.pack(expand=True, fill="both")
        box.insert("0.0", text)
        box.configure(state="disabled")
        if back:
            ctk.CTkButton(self.main_panel, text="Back", command=lambda: self.load_menu("HOME")).pack(pady=5)

    def check_msf(self):
        try:
            out = subprocess.getoutput(f"{MSF} -v")
            return "READY" if "Framework" in out else "NOT FOUND"
        except:
            return "NOT FOUND"

# ----------------- RUN -----------------
if __name__ == "__main__":
    EasySploitGUI().mainloop()
