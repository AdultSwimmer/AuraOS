import tkinter as tk
import math

class AuraOS(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AuraOS")
        self.geometry("520x720")
        self.configure(bg="#0a0a0f")
        self.resizable(False, False)

        self.pulse_t = 0.0

        # ---------- HEADER ----------
        title = tk.Label(
            self,
            text="Hello, welcome to AuraOS",
            font=("Helvetica", 18, "bold"),
            fg="#f0ece4",
            bg="#0a0a0f"
        )
        title.pack(pady=18)

        sub = tk.Label(
            self,
            text="Persistent Context Interface",
            font=("Courier New", 10),
            fg="#6a6a7a",
            bg="#0a0a0f"
        )
        sub.pack()

        # ---------- MAIN ----------
        main = tk.Frame(self, bg="#0a0a0f")
        main.pack(expand=True)

        self.canvas = tk.Canvas(
            main,
            width=220,
            height=220,
            bg="#0a0a0f",
            highlightthickness=0
        )
        self.canvas.pack(pady=40)

        self.orb = self.canvas.create_oval(40, 40, 180, 180, fill="#c8a96e", outline="")
        self.glow = self.canvas.create_oval(25, 25, 195, 195, outline="#c8a96e", width=2)

        # ---------- INPUTS ----------
        input_frame = tk.Frame(main, bg="#0a0a0f")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="USERNAME", fg="#d8d4cc", bg="#0a0a0f",
                 font=("Courier New", 10)).grid(row=0, column=0, sticky="e", padx=8, pady=6)

        self.username_entry = tk.Entry(
            input_frame,
            bg="#111118",
            fg="#f0ece4",
            insertbackground="#f0ece4",
            width=22,
            relief="flat"
        )
        self.username_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="PASSWORD", fg="#d8d4cc", bg="#0a0a0f",
                 font=("Courier New", 10)).grid(row=1, column=0, sticky="e", padx=8, pady=6)

        self.password_entry = tk.Entry(
            input_frame,
            bg="#111118",
            fg="#f0ece4",
            insertbackground="#f0ece4",
            width=22,
            show="*",
            relief="flat"
        )
        self.password_entry.grid(row=1, column=1)

        # ---------- BUTTON ----------
        start_button = tk.Button(
            input_frame,
            text="START",
            command=self.start,
            font=("Courier New", 11, "bold"),
            bg="#c8a96e",
            fg="#0a0a0f",
            relief="flat",
            padx=20,
            pady=6
        )
        start_button.grid(row=2, column=0, columnspan=2, pady=18)

        # ---------- FOOTER ----------
        footer = tk.Label(
            self,
            text="© 2026 AuraOS • github.com/AdultSwimmer/AuraOS",
            font=("Courier New", 9),
            fg="#6a6a7a",
            bg="#0a0a0f"
        )
        footer.pack(side="bottom", pady=10)

        self.animate()

    def animate(self):
        self.pulse_t += 0.08

        scale = 1 + 0.04 * math.sin(self.pulse_t)

        self.canvas.coords(
            self.orb,
            40 - 20*(scale-1),
            40 - 20*(scale-1),
            180 + 20*(scale-1),
            180 + 20*(scale-1),
        )

        self.canvas.coords(
            self.glow,
            25 - 25*(scale-1),
            25 - 25*(scale-1),
            195 + 25*(scale-1),
            195 + 25*(scale-1),
        )

        self.after(30, self.animate)

    def start(self):
        print("Username:", self.username_entry.get())
        print("Password:", self.password_entry.get())


if __name__ == "__main__":
    app = AuraOS()
    app.mainloop()