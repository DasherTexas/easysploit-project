import customtkinter as ctk
import subprocess
import platform
import sys
import requests

ctk.set_appearance_mode("dark")
MSF = "msfconsole"

class EasySploit(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("easySploit")
        self.geometry("1100x720")

        self.target = ctk.CTkEntry(self, placeholder_text="TARGET (lab machine)")
        self.target.pack(fill="x", padx=10, pady=5)

        self.menu = ctk.CTkFrame(self)
        self.menu.pack(pady=5)

        for name in ["HOME","PAYLOADS","EXPLOITS","SCANNERS",
                     "SESSIONS","WEB TEST","MSFCONSOLE","HELP","DEBUG"]:
            ctk.CTkButton(self.menu, text=name, width=120,
                          command=lambda n=name:self.load(n)).pack(side="left", padx=3)

        self.panel = ctk.CTkFrame(self)
        self.panel.pack(expand=True, fill="both", padx=10, pady=10)

        self.home()

    # ---------------- CORE ----------------

    def clear(self):
        for w in self.panel.winfo_children():
            w.destroy()

    def back(self):
        ctk.CTkButton(self.panel, text="⬅ BACK", command=self.home).pack(pady=15)

    def load(self, name):
        self.clear()
        getattr(self, name.lower().replace(" ","_"))()

    def run_msf_module(self, module):
        target = self.target.get()
        cmd = f"use {module}; set RHOSTS {target}"
        subprocess.Popen([MSF, "-q", "-x", cmd])

    # ---------------- HOME ----------------

    def home(self):
        self.clear()

        ctk.CTkLabel(self.panel, text="WELCOME TO easySploit", font=("Arial", 24)).pack(pady=15)

        msf_status = subprocess.getoutput(f"{MSF} -v")
        status = "READY" if "Framework" in msf_status else "NOT FOUND"

        ctk.CTkLabel(self.panel, text=f"Metasploit: {status}").pack()
        ctk.CTkLabel(self.panel, text=f"OS: {platform.system()}").pack()
        ctk.CTkLabel(self.panel, text=f"Python: {sys.version.split()[0]}").pack()

        ctk.CTkButton(self.panel, text="Launch Metasploit Console",
                      command=lambda: subprocess.Popen([MSF])).pack(pady=20)

    # ---------------- PAYLOADS ----------------

    def payloads(self):
        self.module_browser("payload")

    def exploits(self):
        self.module_browser("exploit")

    def scanners(self):
        self.module_browser("auxiliary")

    def module_browser(self, mtype):
        search = ctk.CTkEntry(self.panel, placeholder_text=f"Search {mtype}")
        search.pack(fill="x", padx=20, pady=5)

        box = ctk.CTkTextbox(self.panel)
        box.pack(expand=True, fill="both", padx=20, pady=10)

        def run_search():
            data = subprocess.getoutput(
                f"{MSF} -q -x 'search {search.get()} type:{mtype}; exit'"
            )
            box.delete("0.0","end")
            box.insert("0.0",data)

        ctk.CTkButton(self.panel, text="Search", command=run_search).pack(pady=5)

        self.back()

    # ---------------- SESSIONS ----------------

    def sessions(self):
        box = ctk.CTkTextbox(self.panel)
        box.pack(expand=True, fill="both", padx=20, pady=10)

        def refresh():
            data = subprocess.getoutput(f"{MSF} -q -x 'sessions; exit'")
            box.delete("0.0","end")
            box.insert("0.0",data)

        ctk.CTkButton(self.panel, text="Refresh Sessions", command=refresh).pack(pady=10)

        self.back()

    # ---------------- WEB TEST ----------------

    def web_test(self):
        url = ctk.CTkEntry(self.panel, placeholder_text="https://your-lab-site")
        url.pack(fill="x", padx=20, pady=5)

        box = ctk.CTkTextbox(self.panel)
        box.pack(expand=True, fill="both", padx=20, pady=10)

        def status():
            try:
                r = requests.get(url.get())
                box.insert("end", f"Status: {r.status_code}\n")
            except Exception as e:
                box.insert("end", f"Error: {e}\n")

        def headers():
            try:
                r = requests.get(url.get())
                for h in ["Content-Security-Policy","X-Frame-Options"]:
                    box.insert("end", f"{h}: {r.headers.get(h,'Missing')}\n")
            except Exception as e:
                box.insert("end", f"Error: {e}\n")

        ctk.CTkButton(self.panel, text="Check Status", command=status).pack(pady=5)
        ctk.CTkButton(self.panel, text="Check Security Headers", command=headers).pack(pady=5)

        self.back()

    # ---------------- HELP ----------------

    def help(self):
        text = """
Workflow (legal lab use):
1. Set TARGET
2. Search module
3. Open in msfconsole
4. Configure & run manually
5. Check sessions
"""
        box = ctk.CTkTextbox(self.panel)
        box.pack(expand=True, fill="both", padx=20, pady=10)
        box.insert("0.0", text)
        box.configure(state="disabled")

        self.back()

    # ---------------- DEBUG ----------------

    def debug(self):
        info = f"""
OS: {platform.system()} {platform.release()}
Python: {sys.version}
Pip: {subprocess.getoutput('python -m pip --version')}
Metasploit: {subprocess.getoutput(f'{MSF} -v')}
"""
        box = ctk.CTkTextbox(self.panel)
        box.pack(expand=True, fill="both", padx=20, pady=10)
        box.insert("0.0", info)
        box.configure(state="disabled")

        self.back()

    # ---------------- MSFCONSOLE ----------------

    def msfconsole(self):
        subprocess.Popen([MSF])


EasySploit().mainloop()
