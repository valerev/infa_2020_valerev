import random
import pygame
import tkinter

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

x_screen_size = 1200
y_screen_size = 600


def new_ball():
    """
    This function draws new ball on the screen. Each ball have parameters - color, coordinate, radius and velocity.
    Function returns parameters, so i can change coordinate later
    :no incoming data:
    return: parameters of the new ball
    """
    global x, y, r, color, v_x, v_y
    r = random.randint(30, 50)
    x = random.randint(51, x_screen_size - 51)
    y = random.randint(51, y_screen_size - 51)
    v_x = random.randint(-10, 10)
    v_y = random.randint(-10, 10)
    is_clicked = False
    color = COLORS[random.randint(0, 5)]
    parameters = [color, [x, y], r, v_x, v_y]
    pygame.draw.circle(screen, color, (x, y), r)
    return parameters


def boss_mob():
    """
    function creates boss surface. Image of boss loads from my directory. You can change directory and
    your image will be different. As new_ball() function it returns boss parameters
    :no incoming data:
    return: parameters of boss
    """
    global x, y, v_x, v_y
    x = random.randint(100, 800)
    y = random.randint(100, 800)
    v_x = random.randint(-20, 20)
    v_y = random.randint(-20, 20)

    boss_image_surf = pygame.image.load('fly-1.png')
    boss_image_surf.set_colorkey(BLACK)
    boss_image_surf_scale = pygame.transform.scale(boss_image_surf,
                                                   (boss_image_surf.get_width() // 5,
                                                   boss_image_surf.get_height() // 5)
                                                   )
    boss_image_rect = boss_image_surf_scale.get_rect()
    boss_image_rect.center = (x, y)

    boss_parameters = [boss_image_rect, v_x, v_y, boss_image_surf_scale]
    return boss_parameters


def draw_boss_on_the_screen(boss, time_indicate):
    """
    This function draws boss on the screen as a surface. Boss reflects from walls. Boss changes velocity every time
    when time_indicate is True -- this is a special thing
    :boss: parameters of the boss (image rectangle, speed_x, speed_y, image scale)
    :time_indicate: if True, boss changes his velocity
    return: nothing
    """
    boss[0].x += boss[1]
    boss[0].y += boss[2]

    if boss[0].x <= 0 or boss[0].x >= 800:
        boss[1] *= -1
        boss[3] = pygame.transform.rotate(boss[3], 180)
    if boss[0].y <= 50 or boss[0].y >= 600:
        boss[2] *= -1

    if time_indicate:
        boss[1] = random.randint(-20, 20)
        boss[2] = random.randint(-20, 20)

    screen.blit(boss[3], boss[0])


def draw_ball(surf, color, cor, radius):
    """
    This function draws a ball on current surface with current color, position and radius
    :surf: surface you want to draw ball on
    :color: color of drawing ball
    :cor: coordinates of the ball (x, y)
    :radius: radius of the ball
    return: nothing
    """
    pygame.draw.circle(surf, color, cor, radius)


def draw_balls_on_the_screen(surf, list):
    """
    This function draws balls on the surf. It takes surf, where it should draw balls. list - ball list
    where is new_ball() parameters.
    :surf: surface you want to draw balls on
    :list: lit of balls, which you want to draw on
    return: nothing
    """
    for i in range(len(list)):
        list[i][1][0] += list[i][3]
        list[i][1][1] += list[i][4]
        if list[i][1][0] >= x_screen_size-51 or list[i][1][0] <= 51:
            list[i][3] *= -1 # Reverse peed, if ball goes away in x direction
        if list[i][1][1] >= y_screen_size-51 or list[i][1][1] <= 51:
            list[i][4] *= -1 # # Reverse peed, if ball goes away in y direction
        draw_ball(surf, list[i][0], list[i][1], list[i][2])


def draw_score(score):
    """
    Takes score and draws it on the screen
    :score: score you want to draw
    return: nothing
    """
    score_obj = pygame.font.SysFont(None, 36)
    text = score_obj.render('score = {}'.format(score), 1, YELLOW)
    screen.blit(text, (500, 50))


def draw_timer(time):
    """
    This function takes time and draws it on the screen
    :time: time you want to draw
    return: nothing
    """
    time_obj = pygame.font.SysFont(None, 36)
    time_text = time_obj.render('time = {}'.format(time), 1, YELLOW)
    screen.blit(time_text, (100, 50))


def draw_number_of_balls(list_1):
    """
    Ths function takes list of balls and draws on the screen number of balls
    :list_1: list of the existing ball, number of which you want to draw on the screen
    return: nothing
    """
    num_obj = pygame.font.SysFont(None, 36)
    num_text = num_obj.render('number of balls = {}'.format(len(balls_list)), 1, YELLOW)
    screen.blit(num_text, (800, 50))


def player_name():
    """
    Creates window where you should put your name and press button to play. It was made on tkinter
    When player clicks on the button window destroys and game begins
    :no incoming data:
    return: nothing
    """

    def command_button():
        name = field_to_write.get()
        print(name, file=list_of_the_best_players, end=' ')
        window.destroy()

    window = tkinter.Tk()
    window.geometry('400x200')
    text_window = tkinter.Label(window, text='Put your name and press ready ', font=('Arial', 20))
    text_window.grid(column=1, row=0)
    field_to_write = tkinter.Entry(window, width=36)
    field_to_write.grid(column=1, row=1)
    button_to_click = tkinter.Button(window, text='Ready', command=command_button)
    button_to_click.grid(column=1, row=2)
    window.mainloop()


def old_list_of_the_best_players():
    """
    This function reads file with the best players
    :no incoming data:
    return: list of players have ever played (list of strings)
    """
    list_of_the_best_players = open('list_of_the_best_players.txt', 'r')
    players_list_lines = list_of_the_best_players.readlines()
    players_list_lines_format = []
    for line in players_list_lines:
        players_list_lines_format.append(line.split())
    list_of_the_best_players.close()
    return players_list_lines_format


def add_new_player():
    """This function adds new player`s name and score
    :no incoming data:
    return: nothing
    """
    list_of_the_best_players = open('list_of_the_best_players.txt', 'r')
    new_player = list_of_the_best_players.readline().split()

    players_list_lines.append(new_player)
    list_of_the_best_players.close()

    list_of_the_best_players = open('list_of_the_best_players.txt', 'a')
    for line in players_list_lines:
        print(line, file=list_of_the_best_players)

    list_of_the_best_players.close()


players_list_lines = old_list_of_the_best_players()
list_of_the_best_players = open('list_of_the_best_players.txt', 'a')

player_name()
pygame.init()
FPS = 30

screen = pygame.display.set_mode((x_screen_size, y_screen_size))

pygame.display.update()
clock = pygame.time.Clock()
finished = False
score = 0
balls_list = []  # list, where will be all balls. There will be new_ball() parameters
time_create_new_mob = 4  # this variable responds for creating new ball
does_boss_exist = False
ind = True  # set up a indication of readiness to create a boss
time_to_change_boss_move = 12
change_boss_move = False  # time_indicate, which will be in the boss_mob() function
start_number_of_balls = 3  # number of balls in the very beginning
time = 0  # Just set up counter of time in zero
time_after_what_boss_can_exist = 10
max_score_to_boss_appear = 20
max_number_of_balls = 20 # If more - you lose
end_time = 50 # When time get this value - game stops
score_for_boss = 5 # Score that you get after killing boss

# create first three balls
for i in range(start_number_of_balls):
    balls_list.append(new_ball())

# Main part of the game
while not finished:
    clock.tick(FPS)
    time += 1/FPS
    num = len(balls_list)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(num):
                # gets score if you clicked on the ball
                if (event.pos[0] - balls_list[i][1][0]) ** 2 + \
                        (event.pos[1] - balls_list[i][1][1]) ** 2 \
                        <= \
                        balls_list[i][2] ** 2:
                    balls_list.pop(i)
                    score += 1
                    break
            if does_boss_exist:
                # it gives more score for the click on boss
                if (event.pos[0] - fly_boss[0].x) ** 2 + \
                        (event.pos[1] - fly_boss[0].y) ** 2 \
                        <= \
                        fly_boss[3].get_width() ** 2:
                    score += score_for_boss

    if time >= time_create_new_mob:
        balls_list.append(new_ball())
        time_create_new_mob += 1  # to create new ball through 1 time
    if time >= end_time or len(balls_list) >= max_number_of_balls:
        finished = True

    if time >= time_after_what_boss_can_exist and ind:
        # ind variable responds to not create more bosses on the screen. Default - ind = True. When boss
        # exists ind = False and its not create more bosses
        does_boss_exist = True
        fly_boss = boss_mob()
        ind = False

    if does_boss_exist and score <= max_score_to_boss_appear:
        draw_boss_on_the_screen(fly_boss, change_boss_move)
        change_boss_move = False
        if time >= time_to_change_boss_move:
            change_boss_move = True
            time_to_change_boss_move += 2

    draw_number_of_balls(balls_list)
    draw_balls_on_the_screen(screen, balls_list)
    draw_score(score)
    draw_timer(int(time))

    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()

print(score, file=list_of_the_best_players)
list_of_the_best_players.close()

add_new_player()

