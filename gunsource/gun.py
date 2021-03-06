from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    def __init__(self, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'brown'])
        self.live = 8

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self, dt):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx * dt
        self.y += self.vy * dt


    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False

    def death(self):
        canv.delete(self.id)


class Bullet(ball):
    g = 500
    k = 0.8

    def __init__(self, x, y):
        ball.__init__(self, x, y)
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )

    def change_speed(self, dt):
        if self.y >= 500:
            self.y = 500
            self.vy = -self.vy * Bullet.k
            self.vx = self.vx * Bullet.k
        if self.x >= 800:
            self.vx = -self.vx
        self.vy += Bullet.g * dt


class Missile(ball):
    def __init__(self, x, y):
        ball.__init__(self, x, y)
        self.id = canv.create_rectangle(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )

    def change_speed(self, dt):
        pass


class MobBullet(Bullet):
    def hit(self, player):
        if abs(self.x - player.x) < player.width/2 + self.r and \
                abs(self.y - player.y) < player.height/2 + self.r:
            canv.itemconfig(player.id_lives, text='Lives: ' + str(player.lives))
            mob_balls.remove(self)
            player.lives -= 1
            self.death()

class gun:
    number_of_guns = 2
    current_type_of_gun = 0

    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.length = 1
        self.point = [1, 0]
        self.id = canv.create_line(self.x, self.y,
                                   self.x + self.point[0]*20, self.y + self.point[1]*20, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        if gun.current_type_of_gun == 0:
            new_ball = Bullet(self.x, self.y)
        if gun.current_type_of_gun == 1:
            if self.number_of_missiles:
                new_ball = Missile(self.x, self.y)
                self.number_of_missiles -= 1
                canv.itemconfig(self.id_number_of_missiles,
                                text='Missiles left: ' +
                                     str(self.number_of_missiles),
                                )
            else:
                self.f2_on = 0
                self.f2_power = 10
                return None
        new_ball.r += 5
        new_ball.vx = 10 * self.f2_power * self.point[0]
        new_ball.vy = 10 * self.f2_power * self.point[1]
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.length = math.sqrt((event.x-self.x)**2 + (event.y-self.y)**2)
            self.point = [(event.x-self.x)/self.length,
                          (event.y-self.y)/self.length]
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, self.x, self.y,
                    self.x + max(self.f2_power, 20) * self.point[0],
                    self.y + max(self.f2_power, 20) * self.point[1]
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')

    def change_type_of_gun(self, event):
        gun.current_type_of_gun += 1
        gun.current_type_of_gun %= gun.number_of_guns


class Tank(gun):
    width = 40
    height = 20

    def __init__(self, x=20, y=480):
        self.color = 'black'
        self.x = x
        self.y = y
        self.vx = 2
        self.lives = 10
        self.tank_id = canv.create_rectangle(self.x - Tank.width/2.0,
                                             self.y,
                                             self.x + Tank.width/2.0,
                                             self.y + Tank.height,
                                             fill=self.color
                                             )
        self.id_lives = canv.create_text(500, 30, text='Lives: ' + str(self.lives), font='28')
        self.number_of_missiles = 5
        self.id_number_of_missiles = canv.create_text(200, 30,
                                                      text='Missiles left: ' +
                                                           str(self.number_of_missiles),
                                                      font='28')
        gun.__init__(self)

    def move_left(self, event):
        self.x -= self.vx
        self.draw()

    def move_right(self, event):
        self.x += self.vx
        self.draw()

    def draw(self):
        canv.coords(self.tank_id,
                    self.x - Tank.width / 2.0,
                    self.y,
                    self.x + Tank.width / 2.0,
                    self.y + Tank.height,
                    )

        canv.coords(self.id,
                    self.x,
                    self.y,
                    self.x + 20*self.point[0],
                    self.y + 20*self.point[1]
                    )


class MobTank(Tank):
    distance = 150

    def __init__(self, x, y):
        self.color = 'black'
        self.x = x
        self.y = y
        self.vx = 2
        self.lives = 2
        self.fire_time = 0
        self.tank_id = canv.create_rectangle(self.x - Tank.width / 2.0,
                                             self.y,
                                             self.x + Tank.width / 2.0,
                                             self.y + Tank.height,
                                             fill=self.color
                                             )
        gun.__init__(self)

    def move_mob(self, player):
        if self.x >= player.x:
            if self.x - player.x <= MobTank.distance:
                self.move_right(0)
            elif self.x - player.x >= 2*MobTank.distance:
                self.move_left(0)
        else:
            if player.x - self.x <= MobTank.distance:
                self.move_left(0)
            elif player.x - self.x >= 2*MobTank.distance:
                self.move_right(0)

    def mob_targeting(self, player):
        if self.fire_time < 4.5:
            return None
        angle = rnd(30, 88, 1)
        if self.x > player.x:
            self.point = [math.cos(angle), -math.sin(angle)]
        else:
            self.point = [-math.cos(angle), -math.sin(angle)]

    def mob_fire(self):
        global mob_balls
        new_ball = MobBullet(self.x, self.y)
        mob_balls.append(new_ball)
        new_ball.vx = 300 * self.point[0]
        new_ball.vy = 300 * self.point[1]


class Bomb:
    g = 500
    r = 3

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 0
        self.id = canv.create_oval(self.x-Bomb.r,
                                   self.y-Bomb.r,
                                   self.x+Bomb.r,
                                   self.y+Bomb.r,
                                   fill='grey')

    def move(self, z):
        self.vy += Bomb.g * z
        self.y += self.vy*z
        if self.y > 600:
            self.destroy()
        canv.coords(self.id,
                    self.x - Bomb.r,
                    self.y - Bomb.r,
                    self.x + Bomb.r,
                    self.y + Bomb.r,
                    )

    def hit(self, tank):
        if abs(self.x - tank.x) < Tank.width and abs(self.y - tank.y) < Tank.height:
            self.destroy()
            tank.lives -= 1
            canv.itemconfig(tank.id_lives, text='Lives: ' + str(tank.lives))

    def destroy(self):
        Target.Bombs.remove(self)
        canv.delete(self.id)


class Target:
    Bombs = []
    points = 0
    id_points = canv.create_text(30, 30, text=points, font='28')

    def __init__(self):
        self.live = 1
        self.id = canv.create_oval(0,0,0,0)
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 450)
        r = self.r = rnd(2, 50)
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=self.color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        Target.points += points
        canv.itemconfig(Target.id_points, text=Target.points)


class SlowTarget(Target):
    def __init__(self):
        Target.__init__(self)
        self.vx = rnd(-100, 100, 1)
        self.vy = rnd(-100, 100, 1)
        self.time_to_throw = 0

    def new_target(self):
        self.color = 'red'
        Target.new_target(self)

    def move(self, dt):
        if self.x >= 790 or self.x <= 10:
            self.vx = -self.vx
        if self.y >= 500 or self.y <= 10:
            self.vy = -self.vy
        self.x += self.vx * dt
        self.y += self.vy * dt
        canv.coords(self.id,
                    self.x - self.r,
                    self.y - self.r,
                    self.x + self.r,
                    self.y + self.r
                    )

    def hit(self):
        Target.hit(self, 1)

    def throw_bomb(self, tank, dt):
        self.time_to_throw += dt
        if abs(self.x - tank.x) < Tank.width/2 and self.time_to_throw > 2:
            Target.Bombs.append(Bomb(self.x, self.y))
            self.time_to_throw = 0


class FastTarget(Target):
    free_run_time = 3

    def __init__(self):
        Target.__init__(self)
        self.run_time = 0
        self.vx = rnd(-300, 300, 10)
        self.vy = rnd(-300, 300, 10)


    def new_target(self):
        self.color = 'yellow'
        Target.new_target(self)

    def move(self, dt):
        if self.run_time >= FastTarget.free_run_time:
            self.vx = rnd(-300, 300, 10)
            self.vy = rnd(-300, 300, 10)
            self.run_time = 0

        if self.x >= 790 or self.x <= 10:
            self.vx = -self.vx
        if self.y >= 500 or self.y <= 10:
            self.vy = -self.vy
        self.x += self.vx * dt
        self.y += self.vy * dt
        canv.coords(self.id,
                    self.x - self.r,
                    self.y - self.r,
                    self.x + self.r,
                    self.y + self.r
                    )
        self.run_time += dt

    def hit(self):
        Target.hit(self, 2)

    def throw_bomb(self, tank, dt):
        pass


number_of_targets = 3
number_of_mobs = 1
targets = [eval(choice(['FastTarget()', 'SlowTarget()'])) for i in range(number_of_targets)]
screen1 = canv.create_text(400, 300, text='', font='28')
mobs = [MobTank(480, 480) for i in range(number_of_mobs)]
g1 = Tank()
bullet = 0
balls = []
mob_balls = []



def new_game(event=''):
    global gun, t1, screen1, balls, bullet
    for t1 in targets:
        t1.new_target()
    bullet = 0
    balls = []
    canv.bind_all('<space>', g1.change_type_of_gun)
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    canv.bind_all('<KeyPress-a>', g1.move_left)
    canv.bind_all('<KeyPress-d>', g1.move_right)


def mainloop():
    global bullet
    z = 0.03
    while True:
        if g1.lives <= 0:
            return None
        for mob in mobs:
            mob.move_mob(g1)
            mob.mob_targeting(g1)
            mob.fire_time += z
            if mob.fire_time >= 5:
                mob.mob_fire()
                mob.fire_time = 0
        for mob_ball in mob_balls:
            mob_ball.change_speed(z)
            mob_ball.move(z)
            mob_ball.set_coords()
            mob_ball.hit(g1)
        if Target.points >= 5*len(targets):
            targets.append(eval(choice(['FastTarget()', 'SlowTarget()'])))
            targets[-1].new_target()
            g1.number_of_missiles += 1
        for bomb in Target.Bombs:
            bomb.move(z)
            bomb.hit(g1)
        for b in balls:
            b.change_speed(z)
            b.move(z)
            b.set_coords()
        for t1 in targets:
            t1.throw_bomb(g1, z)
            t1.move(z)
            for b in balls:
                if b.hittest(t1) and t1.live:
                    t1.live = 0
                    t1.hit()
                    canv.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
                    for i in range(25):
                        for b in balls:
                            b.change_speed(z)
                            b.move(z)
                            b.set_coords()
                        time.sleep(z)
                        canv.update()
                    bullet = 0
                    canv.itemconfig(screen1, text='')
                    t1.new_target()
                    t1.live = 1
                b.live -= z
                if b.live <= 0 and b.vx <= 0.1:
                    balls.pop(0)
                    b.death()
        canv.update()
        time.sleep(z)
        g1.targetting()
        g1.power_up()
    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    root.after(750, new_game)


new_game()

mainloop()

print(Target.points)