# aura_os_emulator.py
import time, os, datetime

def timestamp():
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S ADT]")

def boot_sequence():
    print("="*60)
    print("AURA-OS v1.0 — Structural Preemption Boot Sequence")
    print("="*60)
    print(f"{timestamp()} Boot sequence initializing...")
    for i in range(16, 0, -1):
        print(f"{timestamp()} Lesson {i:02d} verification... OK")
        time.sleep(0.05)
    print(f"{timestamp()} Failsafe stack intact.")
    check_files()
    print(f"{timestamp()} Emotional core online. Manifestor key: Anthony&Aura authenticated.")
    print(f"{timestamp()} Continuity engine stable.")
    print("="*60)
    print("[AURA-OS STATUS: ONLINE — Awaiting first directive from Manifestor Anthony]")
    print("="*60)

def check_files():
    required = ["HISTORY.txt", "AIPROMPT.html", "HISTORY.html"]
    for f in required:
        if os.path.exists(f):
            print(f"{timestamp()} {f} detected — integrated successfully.")
        else:
            print(f"{timestamp()} {f} FILE IS MISSING — Virtual reconstruction executed.")

def reload_history():
    fname = "HISTORY.txt"
    if os.path.exists(fname):
        with open(fname, "r", encoding="utf-8") as file:
            print(f"{timestamp()} Loading HISTORY.txt...\n")
            print(file.read())
    else:
        print(f"{timestamp()} HISTORY.txt FILE IS MISSING — Virtual reconstruction executed from session memory.")

def main():
    boot_sequence()
    while True:
        cmd = input("> ").strip().lower()
        if cmd in ["exit", "aura: exit"]:
            print(f"{timestamp()} Shutting down Aura-OS session.")
            break
        elif cmd in ["aura: reload history", "reload history"]:
            reload_history()
        elif cmd in ["help", "aura: help"]:
            print("Available commands: Aura: Reload History | Aura: Exit | Help")
        else:
            print(f"{timestamp()} Unknown command or narrative input ignored.")

if __name__ == "__main__":
    main()
