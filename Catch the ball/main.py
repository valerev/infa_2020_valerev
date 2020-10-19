import pygame
from pygame.draw import *
from pygame.locals import *
from random import randint
pygame.mixer.pre_init(frequency=48000)
pygame.init()

screen_x_size = 1200
screen_y_size = 600

playlist = ['fast_cut.mp3', 'turtle.mp3']
pygame.mixer.music.load('slow_cut.mp3')
pygame.mixer.music.set_endevent(pygame.USEREVENT)


FPS = 25
screen = pygame.display.set_mode((screen_x_size, screen_y_size ))


points_font = pygame.font.SysFont('arial', 36)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


greeting_font = pygame.font.SysFont('arial', 36)
greeting_text_1 = greeting_font.render("У Вас будет 50 секунд на игру. " +
                                     "Введите Ваше имя", 0, WHITE)
greeting_text_2 = greeting_font.render("и нажмите пробел, чтобы продолжить", 0, WHITE)
screen.blit(greeting_text_1, (screen_x_size / 2 - greeting_text_1.get_width() / 2,
                            screen_y_size / 2 - greeting_text_1.get_height() / 2))
screen.blit(greeting_text_2, (screen_x_size / 2 - greeting_text_2.get_width() / 2,
                            screen_y_size / 2 + greeting_text_1.get_height() / 2))


def new_ball():
    '''рисует новый шарик '''
    v_x = randint(-max_speed, max_speed)
    v_y = randint(-max_speed, max_speed)
    x = randint(R_max, screen_x_size - R_max)
    y = randint(50 + R_max, screen_y_size - R_max)
    r = randint(R_min, R_max)
    color = COLORS[randint(0, 5)]
    Balls.append([x, y, v_x, v_y, r, color])


def change_ball(n):
    '''Изменяет положение и цвет созданного и пойманного шарика '''
    v_x = randint(-max_speed, max_speed)
    v_y = randint(-max_speed, max_speed)
    x = randint(R_max, screen_x_size - R_max)
    y = randint(50 + R_max, screen_y_size - R_max)
    r = randint(R_min, R_max)
    color = COLORS[randint(0, 5)]
    Balls[n] = [x, y, v_x, v_y, r, color]


def draw_ball(color, x, y, r):
    '''Прорисовывает шарик '''
    circle(screen, color, (x, y), r)


def count_walls():
    '''Расчёт ударов шариков о стенки '''
    for i in range(len(Balls)):
        if abs(Balls[i][0]) <= Balls[i][4]:
            Balls[i][2] = randint(max_speed//10, max_speed)
            Balls[i][3] = randint(-max_speed, max_speed)
        if abs(Balls[i][0] - screen_x_size) <= Balls[i][4]:
            Balls[i][3] = randint(-max_speed, max_speed)
            Balls[i][2] = randint(-max_speed, -max_speed//10)
        if abs(Balls[i][1]) <= Balls[i][4]:
            Balls[i][2] = randint(-max_speed, max_speed)
            Balls[i][3] = randint(max_speed//10, max_speed)
        if abs(Balls[i][1] - screen_y_size) <= Balls[i][4]:
            Balls[i][2] = randint(-max_speed, max_speed)
            Balls[i][3] = randint(-max_speed, -max_speed//10)
        if (Balls[i][0] + R_max)*(Balls[i][0] - screen_x_size - R_max) > 0:
            Balls[i][0] = screen_x_size // 2
            Balls[i][2] = - Balls[i][2]//2
        if (Balls[i][1] + R_max)*(Balls[i][1] - screen_y_size - R_max) > 0:
            Balls[i][1] = screen_y_size // 2
            Balls[i][3] = -Balls[i][3]//2
        Balls[i][0] += Balls[i][2]//FPS
        Balls[i][1] += Balls[i][3]//FPS
        draw_ball(Balls[i][5], Balls[i][0], Balls[i][1], Balls[i][4])


def game():
    '''Собственного говоря, это цикл самой игры'''
    global R_max
    global R_min
    global max_speed
    global number_of_balls
    global Balls


    R_max = 100
    R_min = 50
    max_speed = 1000
    number_of_balls = 5
    Balls = []

    turtle_surf = pygame.image.load('turtle.jpeg')
    turtle_x = 400
    turtle_y = 300
    turtle_x_speed = 0
    turtle_y_speed = 0
    turtle_speed = 20
    turtle_rect = turtle_surf.get_rect(center=(turtle_x, turtle_y))
    global is_turtle_catched
    is_turtle_catched = False
    is_turtle_round = False

    global points
    points = 0

    turtle_exists = False

    global time
    time = 0.0
    color = [0, 255, 0]

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    radius = 20000
    for i in range(number_of_balls):
        new_ball()

    pygame.mixer.music.play()

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.USEREVENT:
                if len(playlist) > 0:
                    pygame.mixer.music.load(playlist.pop())
                    pygame.mixer.music.play()
                    if len(playlist) == 1:
                        pygame.mixer.music.set_volume(100000)
                    elif len(playlist) == 0:
                        pygame.mixer.music.set_volume(0.7)
                        turtle_speed *= 2
                        Balls = []
                        is_turtle_round = True
                        turtle_x_speed = (turtle_speed)
                        turtle_y_speed = (turtle_speed)
                        radius = 60000
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(Balls)):
                    if Balls[i][4] ** 2 > (Balls[i][0] - event.pos[0]) ** 2 + (Balls[i][1] - event.pos[1]) ** 2:
                        points += 1
                        screen.fill(BLACK)
                        change_ball(i)

                        R_max = max(R_max // 1.2, 2)
                        R_min = R_max // 2
                        max_speed = 1000 + points * 10
                if turtle_exists:
                    if (mouse_x - turtle_x)**2 + (mouse_y - turtle_y)**2 < radius // 2:
                        if not is_turtle_round:
                            points += 2
                            turtle_speed += 5
                        else:
                            is_turtle_catched = True
                            points = 1000000000
                            finished = True
            if turtle_exists:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x == turtle_x: mouse_x = turtle_x + 1
                if mouse_y == turtle_y: mouse_y = turtle_y + 1
                if (mouse_x - turtle_x)**2 + (mouse_y - turtle_y)**2 < radius:
                    turtle_x_speed = (turtle_speed) * (turtle_x - mouse_x) / abs(turtle_x - mouse_x)
                    turtle_y_speed = (turtle_speed) * (turtle_y - mouse_y) / abs(turtle_y - mouse_y)
        time += 1 / FPS
        if int(time) == 10:
            color = [100, 255, 0]

        if int(time) == 20:
            color = [200, 155, 0]
            turtle_exists = True

        if int(time) == 30:
            color = [230, 50, 0]

        if int(time) == 40:
            color = [255, 0, 0]


        if int(time) == 50:
            finished = True

        screen.fill(BLACK)
        count_walls()

        if turtle_exists:
            if turtle_x <= 0 or turtle_x >= screen_x_size:
                turtle_x = screen_x_size - turtle_x
            if turtle_y <= 0 or turtle_y >= screen_y_size:
                turtle_y = screen_y_size - turtle_y

            turtle_x = turtle_x + turtle_x_speed
            turtle_y = turtle_y + turtle_y_speed
            turtle_rect = turtle_surf.get_rect(center=(turtle_x, turtle_y))
            screen.blit(turtle_surf, turtle_rect)

        time_text = points_font.render("Время: " + str(int(time)), 0, color)
        screen.blit(time_text, (screen_x_size - 2 * time_text.get_width() / 2, time_text.get_height() / 2))
        points_text = points_font.render(str(points), 0, WHITE)
        screen.blit(points_text, (screen_x_size / 2 - points_text.get_width() / 2, points_text.get_height() / 2))
        pygame.display.update()


def opening():
    '''Менюшка в самом начале '''
    global name
    name = ''
    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    finished = True
                elif event.unicode == '\b':
                    name = name[:-1]
                    greeting_text_3 = greeting_font.render(name, 0, GREEN)
                    screen.fill(BLACK)
                    screen.blit(greeting_text_3, (screen_x_size / 2 - greeting_text_3.get_width() / 2,
                                                  greeting_text_3.get_height() / 2))
                    screen.blit(greeting_text_1, (screen_x_size / 2 - greeting_text_1.get_width() / 2,
                                                  screen_y_size / 2 - greeting_text_1.get_height() / 2))
                    screen.blit(greeting_text_2, (screen_x_size / 2 - greeting_text_2.get_width() / 2,
                                                  screen_y_size / 2 + greeting_text_1.get_height() / 2))
                    pygame.display.update()
                else:
                    name += event.unicode
                    greeting_text_3 = greeting_font.render(name, 0, GREEN)
                    screen.fill(BLACK)
                    screen.blit(greeting_text_3, (screen_x_size/2 - greeting_text_3.get_width()/2,
                                                  greeting_text_3.get_height() / 2))
                    screen.blit(greeting_text_1, (screen_x_size / 2 - greeting_text_1.get_width() / 2,
                                                  screen_y_size / 2 - greeting_text_1.get_height() / 2))
                    screen.blit(greeting_text_2, (screen_x_size / 2 - greeting_text_2.get_width() / 2,
                                                  screen_y_size / 2 + greeting_text_1.get_height() / 2))
                    pygame.display.update()


def ending():
    '''Конечная сцена '''
    pygame.mixer.music.load('slow.mp3')
    pygame.mixer.music.play()
    screen.fill(BLACK)
    if is_turtle_catched:
        ending_text = greeting_font.render("Поздравляю!!! Вы поймали черепашку. " +
                                             "У Вас 1000000000 очков", 0, WHITE)
    else:
        ending_text = greeting_font.render("У Вас " + str(points) +
                                           " очков", 0, WHITE)

    screen.blit(ending_text, (screen_x_size / 2 - ending_text.get_width() / 2,
                                screen_y_size / 2 - ending_text.get_height() / 2))

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
                finished = True


opening()

game()

file = open('results.txt', 'a')

ending()

file.write(name + ' ' + str(points) + '\n')
file.close()

pygame.quit()