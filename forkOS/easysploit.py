import customtkinter as ctk
import subprocess

ctk.set_appearance_mode("dark")
MSF = "msfconsole"

class EasySploit(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("easySploit")
        self.geometry("1100x720")

        self.target = ctk.CTkEntry(self, placeholder_text="TARGET")
        self.target.pack(fill="x", padx=10, pady=5)

        self.panel = ctk.CTkFrame(self)
        self.panel.pack(expand=True, fill="both", padx=10, pady=10)

        self.home()

    # ---------------- HOME ----------------
    def home(self):
        self.clear()

        buttons = [
            ("PAYLOADS", self.payload_menu),
            ("EXPLOITS", self.exploit_menu),
            ("SCANNERS", self.scanner_menu),
            ("SESSIONS", self.sessions_menu),
        ]

        for text, cmd in buttons:
            ctk.CTkButton(self.panel, text=text, height=60, command=cmd).pack(fill="x", pady=10)

    # ---------------- PAYLOADS ----------------
    def payload_menu(self):
        self.clear()

        search = ctk.CTkEntry(self.panel, placeholder_text="Search payload")
        search.pack(fill="x", pady=5)

        result_box = ctk.CTkTextbox(self.panel)
        result_box.pack(expand=True, fill="both")

        def search_payload():
            data = subprocess.getoutput(
                f"{MSF} -q -x 'search {search.get()} type:payload; exit'"
            )
            result_box.delete("0.0", "end")
            result_box.insert("0.0", data)

        def show_all():
            data = subprocess.getoutput(
                f"{MSF} -q -x 'show payloads; exit'"
            )
            result_box.delete("0.0", "end")
            result_box.insert("0.0", data)

        ctk.CTkButton(self.panel, text="SEARCH", command=search_payload).pack(pady=5)
        ctk.CTkButton(self.panel, text="SHOW ALL", command=show_all).pack(pady=5)
        ctk.CTkButton(self.panel, text="BACK", command=self.home).pack(pady=10)

    # ---------------- EXPLOITS ----------------
    def exploit_menu(self):
        self.clear()

        search = ctk.CTkEntry(self.panel, placeholder_text="Search exploit")
        search.pack(fill="x", pady=5)

        result_box = ctk.CTkTextbox(self.panel)
        result_box.pack(expand=True, fill="both")

        def search_exploit():
            data = subprocess.getoutput(
                f"{MSF} -q -x 'search {search.get()} type:exploit; exit'"
            )
            result_box.delete("0.0", "end")
            result_box.insert("0.0", data)

        ctk.CTkButton(self.panel, text="SEARCH", command=search_exploit).pack(pady=5)
        ctk.CTkButton(self.panel, text="BACK", command=self.home).pack(pady=10)

    # ---------------- SCANNERS ----------------
    def scanner_menu(self):
        self.clear()

        result_box = ctk.CTkTextbox(self.panel)
        result_box.pack(expand=True, fill="both")

        def scan_network():
            target = self.target.get()
            cmd = f"use auxiliary/scanner/portscan/tcp; set RHOSTS {target}; run"
            subprocess.Popen([MSF, "-q", "-x", cmd])

        def list_scanners():
            data = subprocess.getoutput(
                f"{MSF} -q -x 'search type:auxiliary scanner; exit'"
            )
            result_box.insert("0.0", data)

        ctk.CTkButton(self.panel, text="QUICK PORT SCAN", command=scan_network).pack(pady=5)
        ctk.CTkButton(self.panel, text="SHOW SCANNERS", command=list_scanners).pack(pady=5)
        ctk.CTkButton(self.panel, text="BACK", command=self.home).pack(pady=10)

    # ---------------- SESSIONS ----------------
    def sessions_menu(self):
        self.clear()

        box = ctk.CTkTextbox(self.panel)
        box.pack(expand=True, fill="both")

        def refresh():
            data = subprocess.getoutput(
                f"{MSF} -q -x 'sessions; exit'"
            )
            box.delete("0.0", "end")
            box.insert("0.0", data)

        ctk.CTkButton(self.panel, text="REFRESH SESSIONS", command=refresh).pack(pady=10)
        ctk.CTkButton(self.panel, text="BACK", command=self.home).pack(pady=10)

    # ---------------- HELPERS ----------------
    def clear(self):
        for w in self.panel.winfo_children():
            w.destroy()

EasySploit().mainloop()
