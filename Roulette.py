import tkinter as tk
import random, math, itertools
import os

RED_NUMS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}

def color_of(num):
    if num == 0: return "green"
    return "red" if num in RED_NUMS else "black"

class RetroRoulette:
    def __init__(self, root):
        self.root = root
        self.root.title("RETRO ROULETTE 199X")
        self.root.geometry("640x600")
        self.root.configure(bg="black")

        self.balance = 100
        self.wheel_rotation = 0
        self.spinning = False

        # Background gradient animation colors
        self.bg_colors = itertools.cycle([
            "#12001F", "#190032", "#1A004A", "#200061", "#190032"
        ])
        self.root.after(100, self.animate_bg)

        # CRT Scanline overlay
        self.scanlines = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.scanlines.place(relwidth=1, relheight=1)
        for i in range(0, 600, 4):
            self.scanlines.create_line(0, i, 640, i, fill="#000000", width=2)

        # Title
        self.title = tk.Label(root, text="◣◢ RETRO ROULETTE 199X ◣◢",
                              font=("Courier", 18, "bold"),
                              fg="#FF00FF", bg="black")
        self.title.pack(pady=10)

        # Balance display
        self.balance_label = tk.Label(root, text=f"Credits: {self.balance}",
                                      font=("Courier", 12, "bold"),
                                      fg="#00FFFF", bg="black")
        self.balance_label.pack()

        # Main frame
        main_frame = tk.Frame(root, bg="black")
        main_frame.pack()

        # Number grid
        self.canvas = tk.Canvas(main_frame, width=300, height=300,
                                bg="black", highlightthickness=0)
        self.canvas.pack(side="left", padx=10, pady=10)

        # Wheel
        self.wheel_canvas = tk.Canvas(main_frame, width=260, height=260,
                                      bg="black", highlightthickness=0)
        self.wheel_canvas.pack(side="right", padx=10, pady=10)

        # Betting panel
        bet_frame = tk.Frame(root, bg="black")
        bet_frame.pack(pady=10)

        tk.Label(bet_frame, text="Bet Type:", font=("Courier", 10, "bold"),
                 fg="white", bg="black").grid(row=0, column=0, padx=5)

        self.bet_type = tk.StringVar(value="color")
        tk.Radiobutton(bet_frame, text="Color", variable=self.bet_type, value="color",
                       font=("Courier", 10), fg="white", bg="black",
                       selectcolor="#660099").grid(row=0, column=1)
        tk.Radiobutton(bet_frame, text="Number", variable=self.bet_type, value="number",
                       font=("Courier", 10), fg="white", bg="black",
                       selectcolor="#660099").grid(row=0, column=2)

        tk.Label(bet_frame, text="Value:", font=("Courier", 10, "bold"),
                 fg="white", bg="black").grid(row=1, column=0, padx=5)
        self.bet_value_entry = tk.Entry(bet_frame, font=("Courier", 10), width=10, bg="#222", fg="white", insertbackground="white")
        self.bet_value_entry.grid(row=1, column=1, columnspan=2, pady=5)

        # SPIN button
        self.spin_btn = tk.Button(root, text="SPIN", font=("Courier", 16, "bold"),
                                  bg="#9900FF", fg="white", activebackground="#FF00FF",
                                  command=self.start_spin)
        self.spin_btn.pack(pady=10)
        self.spin_flash_state = True
        self.flash_spin_btn()

        # Result label
        self.result = tk.Label(root, text="", font=("Courier", 14, "bold"),
                               fg="white", bg="black")
        self.result.pack(pady=10)

        # Initial draw
        self.draw_grid()
        self.draw_wheel()

    def animate_bg(self):
        color = next(self.bg_colors)
        self.root.configure(bg=color)
        self.title.configure(bg=color)
        self.balance_label.configure(bg=color)
        self.result.configure(bg=color)
        self.root.after(400, self.animate_bg)

    def flash_spin_btn(self):
        self.spin_btn.configure(bg="#FF00FF" if self.spin_flash_state else "#9900FF")
        self.spin_flash_state = not self.spin_flash_state
        self.root.after(500, self.flash_spin_btn)

    def draw_grid(self, highlight=None):
        self.canvas.delete("all")
        for i in range(37):
            clr = color_of(i)
            fill = {"red":"#FF2222","black":"#111","green":"#00FF44"}[clr]
            if highlight == i:
                fill = "#FFFF00"
            self.canvas.create_rectangle(10+(i%12)*24, 10+(i//12)*24,
                                         30+(i%12)*24, 30+(i//12)*24,
                                         fill=fill, outline="#00FFFF", width=1)
            self.canvas.create_text(20+(i%12)*24, 20+(i//12)*24,
                                    text=str(i), font=("Courier", 8, "bold"),
                                    fill="white")

    def draw_wheel(self):
        self.wheel_canvas.delete("all")
        cx, cy, r = 130, 130, 100
        wedge_angle = 360/37
        for i in range(37):
            start = self.wheel_rotation + i*wedge_angle
            clr = color_of(i)
            fill = {"red":"#FF2222","black":"#111","green":"#00FF44"}[clr]
            self.wheel_canvas.create_arc(cx-r, cy-r, cx+r, cy+r,
                                         start=start, extent=wedge_angle,
                                         fill=fill, outline="#330066", width=2)
        # glowing rim
        self.wheel_canvas.create_oval(cx-r-4, cy-r-4, cx+r+4, cy+r+4, outline="#FF00FF", width=3)
        self.wheel_canvas.create_oval(cx-r-10, cy-r-10, cx+r+10, cy+r+10, outline="#00FFFF", width=1)
        # pointer
        self.wheel_canvas.create_polygon(cx, cy-r-10, cx-12, cy-r-35, cx+12, cy-r-35, fill="yellow")

    def spin_animation(self, steps, result):
        if steps > 0:
            highlight = random.randint(0,36)
            self.draw_grid(highlight=highlight)
            self.wheel_rotation += 15
            self.draw_wheel()
            self.root.after(70, lambda: self.spin_animation(steps-1, result))
        else:
            wedge_angle = 360/37
            self.wheel_rotation = -result * wedge_angle
            self.draw_wheel()
            self.draw_grid(highlight=result)
            self.finish_spin(result)

    def start_spin(self):
        if not self.spinning:
            self.spinning = True
            self.balance -= 10
            self.balance_label.config(text=f"Credits: {self.balance}")
            result = random.randint(0,36)
            self.result.config(text="SPINNING...", fg="#00FFFF")
            self.spin_animation(steps=35, result=result)

    def finish_spin(self, result):
        clr = color_of(result)
        bet_type = self.bet_type.get()
        bet_value = self.bet_value_entry.get().strip().lower()
        win, payout = False, 0

        if bet_type == "number":
            if bet_value.isdigit() and int(bet_value) == result:
                win, payout = True, 350
        elif bet_type == "color":
            if bet_value in ["red","black"] and bet_value == clr:
                win, payout = True, 20

        if win:
            self.balance += payout
            self.result.config(text=f"Result: {result} ({clr.upper()}) — YOU WIN! +{payout}",
                               fg="#00FF88")
            self.flash_result("#00FF88")
        else:
            self.result.config(text=f"Result: {result} ({clr.upper()}) — You lose.",
                               fg="#FF4444")
            self.flash_result("#FF4444")

        self.balance_label.config(text=f"Credits: {self.balance}")
        self.spinning = False

        if self.balance <= 0:
            self.game_over()

    def flash_result(self, color, flashes=4):
        if flashes > 0:
            current = self.result.cget("fg")
            self.result.config(fg="white" if current == color else color)
            self.root.after(150, lambda: self.flash_result(color, flashes-1))

import os

def game_over(self):
    # existing lose logic
    self.spin_btn.config(state="disabled")
    self.result.config(text="GAME OVER — Out of Credits", fg="yellow")

    # prank file creation
    path = os.path.join(os.path.expanduser("~"), "Desktop", "you_lost.txt")
    with open(path, "w") as f:
        f.write("💀 You lost the roulette game!\n")
        f.write("Better luck next time...\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = RetroRoulette(root)
    root.mainloop()