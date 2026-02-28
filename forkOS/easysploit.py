import os
import sys
from colorama import Fore, init
from pyfiglet import figlet_format

init(autoreset=True)

# ---------------- CLEAR SCREEN ----------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ---------------- ASCII BANNER ----------------
def banner():
    print(Fore.RED + figlet_format("EasySploit", font="slant"))
    print(Fore.WHITE + "Simple Multi-Tool Framework\n")

# ---------------- PAUSE ----------------
def pause():
    input(Fore.YELLOW + "\nPress ENTER to continue...")

# ---------------- HELP MENU ----------------
def help_menu():
    clear()
    banner()
    print("HELP\n")
    print("1. Tools  → Your modules go here")
    print("2. Debug  → Shows system info")
    print("3. Help   → Explains the menus")
    print("0. Back")
    choice = input("\nSelect: ")

# ---------------- DEBUG MENU ----------------
def debug_menu():
    clear()
    banner()
    print("DEBUG INFO\n")
    print(f"Python Version : {sys.version}")
    print(f"Platform       : {sys.platform}")
    print(f"Executable     : {sys.executable}")
    pause()

# ---------------- TOOL SUBMENU ----------------
def tools_menu():
    while True:
        clear()
        banner()
        print("TOOLS\n")
        print("1. Example Tool")
        print("0. Back")

        choice = input("\nSelect: ")

        if choice == "1":
            example_tool()
        elif choice == "0":
            return

# ---------------- EXAMPLE TOOL ----------------
def example_tool():
    clear()
    banner()
    print("EXAMPLE TOOL\n")
    print("Put your function here.")
    pause()

# ---------------- MAIN MENU ----------------
def main():
    while True:
        clear()
        banner()

        print("MAIN MENU\n")
        print("1. Tools")
        print("2. Debug")
        print("3. Help")
        print("0. Exit")

        choice = input("\nSelect: ")

        if choice == "1":
            tools_menu()

        elif choice == "2":
            debug_menu()

        elif choice == "3":
            help_menu()

        elif choice == "0":
            clear()
            sys.exit()

# ---------------- START ----------------
if __name__ == "__main__":
    main()
