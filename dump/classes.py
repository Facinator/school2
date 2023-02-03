from tkinter import *
from tkinter import ttk
import time, random


class Player:
    def __init__(self, name, level, cost, color, speed):
        self.name = name
        self.level = level

        self.cost_kit = cost
        self.color_kit = color
        self.speed_kit = speed

        self.cost = self.cost_kit[self.level - 1]
        self.color = self.color_kit[self.level - 1]
        self.speed = self.speed_kit[self.level - 1]

        self.x = 0
        self.y = 0

    def __end__(self):
        return {"level":self.level, "name": self.name, "cost": self.cost_kit, "color": self.color_kit, "speed": self.speed_kit}

    def update(self):
        self.cost = self.cost_kit[self.level - 1]
        self.color = self.color_kit[self.level - 1]
        self.speed = self.speed_kit[self.level - 1]


class Enemy:
    def __init__(self):
        self.color = "green"
        self.x = random.randint(0, 540)
        self.y = random.randint(0, 590)

    def collision(self, x1, y1, x2, y2):
        if self.x <= x1 <= self.x + 10 or self.x <= x2 <= self.x + 10:
            x1 = True
        else:
            x1 = False
        if self.y <= y1 <= self.y + 10 or self.y <= y2 <= self.y +10:
            y1 = True
        else:
            y1 = False

        if x1 and y1:
            return True
        else:
            return False


class Window:
    root = Tk()
    frame = ttk.Frame(root)
    alive = True
    money = 0
    key = None
    move_keys = [False, False, False, False]

    def __init__(self, PLAYER):
        self.player = PLAYER
        self.__ui__()

        self.enemy = []
        self.enemy_plus = []

        for i in range(100):
            e = Enemy()
            self.enemy_plus.append(e)
            f = self.canvas.create_rectangle(e.x, e.y, e.x + 10, e.y + 10, fill=e.color)
            self.enemy.append(f)

    def __ui__(self):
        self.root.title("Hello")
        self.frame.grid()

        self.label_var = StringVar()
        self.set_string()

        self.label = Label(textvariable=self.label_var)
        self.label.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

        self.canvas = Canvas(self.root, width=550, height=600, background='white')
        self.canvas.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

        self.rect = self.canvas.create_rectangle(self.player.x, self.player.y, self.player.x + 10, self.player.y + 10, fill=self.player.color)

    def __die__(self):
        self.alive = False

    def mainloop(self):
        while self.alive:
            self.root.bind('<KeyPress>', self.set_key)
            self.root.bind('<KeyRelease>', self.reset_key)
            self.root.protocol("WM_DELETE_WINDOW", self.__die__)
            self.collision()
            self.draw()
            time.sleep(1/20)

    def draw(self):
        self.player.update()
        self.move()
        self.canvas.itemconfig(self.rect, fill=self.player.color)
        self.set_string()
        self.root.update()

    def move(self):
        x, y, useless1, useless2 = self.canvas.coords(self.rect)

        if x < 5:
            self.canvas.move(self.rect, 10, 0)
        elif x > 535:
            self.canvas.move(self.rect, -10, 0)
        if y < 5:
            self.canvas.move(self.rect, 0, 10)
        elif y > 585:
            self.canvas.move(self.rect, 0, -10)

        if self.move_keys[0]:
            self.canvas.move(self.rect, 0, - self.player.speed)
        if self.move_keys[1]:
            self.canvas.move(self.rect, - self.player.speed, 0)
        if self.move_keys[2]:
            self.canvas.move(self.rect, 0, self.player.speed)
        if self.move_keys[3]:
            self.canvas.move(self.rect, self.player.speed, 0)

    def set_string(self):
        self.label_var.set(
            f"""
                    w - up
                    a - left   
                    s - down
                    d - right

                    u - upgrade
                    q - quit

                    Name:
                    {self.player.name}
                    Level:
                    {self.player.level}
                    
                    cost for next level
                    {self.player.cost}
                    current money
                    {self.money}
                    
                    pressed key
                    {self.key}
                    """
        )

    def set_key(self, event):
        self.key = event.keysym

        if self.key == "w":
            self.move_keys[0] = True
        elif self.key == "a":
            self.move_keys[1] = True
        elif self.key == "s":
            self.move_keys[2] = True
        elif self.key == "d":
            self.move_keys[3] = True
        elif self.key == "u":
            if self.player.level < len(self.player.color_kit) and self.money >= self.player.cost:
                self.player.level += 1
                self.money -= self.player.cost
        elif self.key == "q":
            self.__die__()

    def reset_key(self, event):
        self.key = event.keysym

        if self.key == "w":
            self.move_keys[0] = False
        elif self.key == "a":
            self.move_keys[1] = False
        elif self.key == "s":
            self.move_keys[2] = False
        elif self.key == "d":
            self.move_keys[3] = False

    def collision(self):
        for i in self.enemy_plus:
            x1, y1, x2, y2 = self.canvas.coords(self.rect)

            a = i.collision(x1, y1, x2, y2)
            if a:
                index = self.enemy_plus.index(i)
                e = self.enemy[index]

                self.money += 5
                self.canvas.delete(e)
                self.enemy.remove(e)
                self.enemy_plus.remove(i)
