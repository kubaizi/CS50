import tkinter as tk
from tkinter import messagebox
from random import random
import shared
from main import winning


class init:
    def __init__(self, root, container, rows, cols):
        self.root = root
        self.container = container
        self.rows = rows
        self.cols = cols
        self.btns = [[None]*cols for _ in range(rows)]
        self.lands = [[None]*cols for _ in range(rows)]
        self.free_land = 0
        self.x_count = 0
        self.mines_text = tk.StringVar()
        self.mines_text.set("Test")

    def open_land(self, r, c):
        self.btns[r][c].grid_forget()
        if self.lands[r][c].cget("text") == 'X':
            messagebox.showinfo("OOPS !!!", "You Lost!! try again")
            self.drawMines(self.level)
        elif self.lands[r][c].cget("text") != 'X':
            self.free_land -= 1
            if self.free_land <= 0:
                messagebox.showinfo("Yeeeeh", "You Win")
                winning()
            empty_lands = []
            empty_lands.append(self.lands[r][c])
            while len(empty_lands) > 0:
                info = empty_lands[0].grid_info()
                nr = info["row"]
                nc = info["column"]
                for sr in [nr-1, nr, nr+1]:
                    for sc in [nc-1, nc, nc+1]:
                        if not (sr == nr and sc == nc):
                            try:
                                if self.lands[sr][sc].cget("text") != 'X' and self.btns[sr][sc].grid_info():
                                    if sr >= 0 and sr <= self.rows - 1 and sc >= 0 and sc <= self.cols-1:
                                        self.btns[sr][sc].grid_forget()
                                        self.free_land -= 1
                                        if self.free_land <= 0:
                                            messagebox.showinfo(
                                                "Yeeeeh", "You Win")
                                    if self.lands[sr][sc].cget("text") == ' ':
                                        if sr >= 0 and sr <= self.rows - 1 and sc >= 0 and sc <= self.cols-1:
                                            empty_lands.append(
                                                self.lands[sr][sc])
                                else:
                                    pass
                            except IndexError:
                                pass
                empty_lands.pop(0)

    def mark_land(self, r, c):
        if self.btns[r][c]["text"] == "X":
            self.btns[r][c]["text"] = " "
            self.x_count += 1
            self.mines_text.set(f"X : {self.x_count}")
        else:
            self.btns[r][c]["text"] = "X"
            self.x_count -= 1
            self.mines_text.set(f"X : {self.x_count}")

    def drawMines(self,  level):
        self.level = level
        self.x_count = 0
        self.free_land = 0
        for r in range(self.rows):
            for c in range(self.cols):
                dificulty = random()
                min_bar = (0.1 if level == 0 else (
                    0.2 if level == 1 else (0.3 if level == 2 else 0.4)))
                label_text = 'X' if dificulty <= min_bar else ' '
                self.lands[r][c] = tk.Label(self.container, width=4, height=2, font='Helvetica 14 bold',
                                            text=label_text, bg='#bbbbbb', fg='white')
                self.lands[r][c].grid(row=r, column=c)
                if label_text == 'X':
                    self.x_count += 1
                else:
                    self.free_land += 1

        self.mines_label = tk.Label(
            self.root, textvariable=self.mines_text).grid(row=0, column=4)
        self.mines_text.set(f"X : {self.x_count}")
        for r in range(self.rows):
            for c in range(self.cols):
                if self.lands[r][c].cget("text") != 'X':
                    tl = 0 if (
                        r == 0 or c == 0) else 1 if self.lands[r-1][c-1].cget("text") == 'X' else 0
                    t = 0 if (
                        r == 0) else 1 if self.lands[r-1][c].cget("text") == 'X' else 0
                    tr = 0 if (
                        r == 0 or c == self.cols-1) else 1 if self.lands[r-1][c+1].cget("text") == 'X' else 0
                    l = 0 if (
                        c == 0) else 1 if self.lands[r][c-1].cget("text") == 'X' else 0
                    y = 0 if (
                        c == self.cols-1) else 1 if self.lands[r][c+1].cget("text") == 'X' else 0
                    bl = 0 if (
                        r == self.rows-1 or c == 0) else 1 if self.lands[r+1][c-1].cget("text") == 'X' else 0
                    b = 0 if (
                        r == self.rows-1) else 1 if self.lands[r+1][c].cget("text") == 'X' else 0
                    br = 0 if (
                        r == self.rows-1 or c == self.cols-1) else 1 if self.lands[r+1][c+1].cget("text") == 'X' else 0
                    sum = tl + t + tr + l + y + bl + b + br
                    self.lands[r][c]["text"] = ' ' if sum == 0 else sum
                    if sum == 7:
                        self.lands[r][c]["fg"] = '#000000'
                    elif sum == 6:
                        self.lands[r][c]["fg"] = '#550000'
                    elif sum == 5:
                        self.lands[r][c]["fg"] = '#770000'
                    elif sum == 4:
                        self.lands[r][c]["fg"] = '#aa2222'
                    elif sum == 3:
                        self.lands[r][c]["fg"] = '#FF0000'
                    elif sum == 2:
                        self.lands[r][c]["fg"] = '#FFFFFF'
                    elif sum == 1:
                        self.lands[r][c]["fg"] = '#00aa00'
                    # print(
                    #     f"row {r}, col={c} -- tl={tl}, t={t}, tr={tr}, l={l}, y={y}, bl={bl}, b={b}, br={br}")
        for r in range(self.rows):
            for c in range(self.cols):
                self.btns[r][c] = tk.Button(self.container, width=4, height=2,
                                            text=' ', border=6)
                self.btns[r][c].grid(row=r, column=c)
                self.btns[r][c].bind(
                    "<Button-1>", lambda event, rr=r, cc=c: self.open_land(r=rr, c=cc))
                self.btns[r][c].bind(
                    "<Button-2>", lambda event, rr=r, cc=c: self.mark_land(r=rr, c=cc))
                self.btns[r][c].bind(
                    "<Button-3>", lambda event, rr=r, cc=c: self.mark_land(r=rr, c=cc))
