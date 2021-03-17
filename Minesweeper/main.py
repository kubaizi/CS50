import sqlite3
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.constants import N, W
from random import random


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
            current_seconds = 300
            current_score.set(f"{current_seconds * 5}")
            mmap.drawMines(level.get())
            countdown(current_seconds)
            self.drawMines(self.level)
        elif self.lands[r][c].cget("text") != 'X':
            self.free_land -= 1
            if self.free_land <= 0:
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
                                            winning()
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


WIDTH = 700
HEIGHT = 500
rows, cols = (10, 10)
root = tk.Tk()

# initilize database
db = sqlite3.connect('./hs.db')
cur = db.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS hs(name TEXT,score INTEGER, level INTEGER)")

# remove 11 and more positions
count = cur.execute("SELECT COUNT(*) FROM hs").fetchone()
if count[0] > 10:
    min = cur.execute("SELECT score FROM hs ORDER BY score DESC").fetchall()
    min_score = min[9][0]
    db.execute(f"DELETE FROM hs WHERE score<{min_score}")
    db.commit()
# Fetch Scores

scores = []


def fetch_scores():
    scores = cur.execute("SELECT * FROM hs ORDER By score DESC").fetchall()
    index = 0
    for row in scores:
        try:
            score_labels[index].config(
                text=f"{index + 1} - {row[0]} {row[1]} Level-{row[2]}")
            index += 1
        except:
            pass


# Level Menu
level = tk.IntVar()
level.set(0)
current_seconds = 300
current_score = tk.StringVar()
current_score.set(f"{current_seconds * 5}")

finish = tk.BooleanVar(value=False)


def winning():
    finish.set(True)
    messagebox.showinfo("Yeeeeh", "You Win")
    name = "?"
    while len(name) != 3:
        name = askstring('Name', 'What is your name? use 3 letters')
    db.execute("INSERT INTO hs(name,score,level) VALUES(?,?,?)",
               (name, current_score.get(), level.get()+1))
    db.commit()

    fetch_scores()
    # mmap.drawMines(level.get())


def level_changed():
    current_seconds = 300
    current_score.set(f"{current_seconds * 5}")
    finish.set(False)
    countdown(current_seconds)
    mmap.drawMines(level.get())


rad1 = tk.Radiobutton(root, variable=level, width=8, command=level_changed,
                      text='easy', value=0).grid(row=0, column=0)
rad2 = tk.Radiobutton(root, variable=level, width=8, command=level_changed,
                      text='medium', value=1).grid(row=0, column=1)
rad3 = tk.Radiobutton(root, variable=level, width=8, command=level_changed,
                      text='hard', value=2).grid(row=0, column=2)
lbl_score = tk.Label(root, textvariable=current_score,
                     text="asda").grid(row=0, column=3)


# Mines Frame
minesFarame = tk.Frame(root, height=HEIGHT, width=WIDTH,
                       bg='green', padx=10, pady=10)
minesFarame.grid(row=1, column=0, columnspan=5)

mmap = init(root, minesFarame, rows, cols)
mmap.drawMines(level.get())
# start = time.time()

scoreFrame = tk.Frame(root, height=HEIGHT, padx=10, pady=10, bg='#aaaaaa')
scoreFrame.grid(row=1, column=6, sticky=N)
score_title = tk.Label(scoreFrame, text='Height Scores', font='Arial 24', bg='#aaaaaa',
                       fg='red').grid(row=0, column=0, sticky=N)

score_labels = []
for i in range(10):
    lbl = tk.Label(scoreFrame, text=f"{i+1} - ", font='Arial 20', pady=6,
                   bg='#aaaaaa')
    lbl.grid(row=i+2, column=0, sticky=W)
    score_labels.append(lbl)


def countdown(current_seconds):
    # stop if finish
    if finish.get() == True:
        return
    # change text in label
    current_score.set(f"{current_seconds * 5}")

    if current_seconds > 0:
        # call countdown again after 1000ms (1s)
        root.after(1000, countdown, current_seconds-1)


fetch_scores()
countdown(current_seconds)

root.mainloop()
