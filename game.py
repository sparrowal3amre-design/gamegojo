# ==========================================
# GOJO VS SUKUNA ONLINE
# FULL ONLINE VERSION
# ==========================================

import pygame
import sys
import random
import os
import socket
import pickle
import threading

# ==========================================
# INIT
# ==========================================
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

pygame.init()

# ==========================================
# ONLINE
# ==========================================
SERVER_IP = "YOUR_RENDER_SERVER.onrender.com"
PORT = 5555

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

online = False
player_id = 0

try:

    client.connect((SERVER_IP, PORT))

    player_id = pickle.loads(
        client.recv(2048)
    )

    online = True

    print("CONNECTED TO SERVER")

except Exception as e:

    print("FAILED TO CONNECT")
    print(e)

# ==========================================
# SCREEN
# ==========================================
WIDTH = 1080
HEIGHT = 1300

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("GOJO VS SUKUNA ONLINE")

clock = pygame.time.Clock()

FPS = 60

# ==========================================
# GAME AREA
# ==========================================
GAME_HEIGHT = 980

# ==========================================
# COLORS
# ==========================================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (220, 20, 60)
BLUE = (30, 144, 255)

GREEN = (0, 255, 0)

YELLOW = (255, 215, 0)

PURPLE = (138, 43, 226)

CYAN = (0, 255, 255)

GRAY = (70, 70, 70)

ORANGE = (255, 165, 0)

# ==========================================
# PATHS
# ==========================================
current_path = os.path.dirname(
    os.path.abspath(__file__)
)

images_path = os.path.join(
    current_path,
    "images"
)

if not os.path.exists(images_path):
    os.makedirs(images_path)

# ==========================================
# LOAD IMAGE
# ==========================================
def load_image(filename, color, size):

    path = os.path.join(images_path, filename)

    if os.path.exists(path):

        try:

            img = pygame.image.load(path).convert_alpha()

            img = pygame.transform.scale(img, size)

            return img

        except:
            pass

    surf = pygame.Surface(size)

    surf.fill(color)

    return surf

# ==========================================
# BACKGROUND
# ==========================================
background = None

for bg in ["background.png", "background.jpg"]:

    path = os.path.join(images_path, bg)

    if os.path.exists(path):

        try:

            background = pygame.image.load(path).convert()

            background = pygame.transform.scale(
                background,
                (WIDTH, GAME_HEIGHT)
            )

            break

        except:
            background = None

# ==========================================
# FONTS
# ==========================================
font = pygame.font.SysFont("Arial", 42)

small_font = pygame.font.SysFont("Arial", 28)

# ==========================================
# CHARACTER
# ==========================================
CHAR_SIZE = 220

GROUND_Y = GAME_HEIGHT - 320

gojo_img = load_image(
    "gojo.png",
    BLUE,
    (CHAR_SIZE, CHAR_SIZE)
)

sukuna_img = load_image(
    "sukuna.png",
    RED,
    (CHAR_SIZE, CHAR_SIZE)
)

gojo_attack_img = load_image(
    "gojo_attack_0.png",
    BLUE,
    (CHAR_SIZE + 20, CHAR_SIZE + 20)
)

sukuna_attack_img = load_image(
    "sukuna_attack_0.png",
    RED,
    (CHAR_SIZE + 20, CHAR_SIZE + 20)
)

# ==========================================
# BUTTONS
# ==========================================
BTN_SIZE = 120

BUTTON_AREA_Y = GAME_HEIGHT + 40

left_btn = pygame.Rect(
    40,
    BUTTON_AREA_Y + 80,
    BTN_SIZE,
    BTN_SIZE
)

right_btn = pygame.Rect(
    190,
    BUTTON_AREA_Y + 80,
    BTN_SIZE,
    BTN_SIZE
)

jump_btn = pygame.Rect(
    WIDTH - 330,
    BUTTON_AREA_Y,
    BTN_SIZE,
    BTN_SIZE
)

power_btn = pygame.Rect(
    WIDTH - 470,
    BUTTON_AREA_Y + 120,
    BTN_SIZE,
    BTN_SIZE
)

skill_btn = pygame.Rect(
    WIDTH - 190,
    BUTTON_AREA_Y + 120,
    BTN_SIZE,
    BTN_SIZE
)

attack_btn = pygame.Rect(
    WIDTH - 330,
    BUTTON_AREA_Y + 240,
    BTN_SIZE,
    BTN_SIZE
)

menu_btn = pygame.Rect(
    WIDTH // 2 - 100,
    GAME_HEIGHT + 90,
    200,
    70
)

# ==========================================
# VARIABLES
# ==========================================
PLAYER_SPEED = 9

ENEMY_SPEED = 5

BALL_SPEED = 24

GRAVITY = 1.2

JUMP_POWER = -24

left_pressed = False

right_pressed = False

running = True

show_menu = False

cooldown = 0

attack_timer = 0

power = 0

ball_active = False

jumping = False

jump_speed = 0

player_hp = 100

enemy_hp = 100

player_y = GROUND_Y

enemy_y = GROUND_Y

# ==========================================
# PLAYER POSITION
# ==========================================
if player_id == 0:

    player_x = 100

    enemy_x = WIDTH - 320

else:

    player_x = WIDTH - 320

    enemy_x = 100

# ==========================================
# RECEIVE DATA
# ==========================================
def receive_data():

    global enemy_x
    global enemy_y
    global enemy_hp

    while online:

        try:

            data = pickle.loads(
                client.recv(4096)
            )

            enemy_x = data["x"]

            enemy_y = data["y"]

            enemy_hp = data["hp"]

        except:
            break

threading.Thread(
    target=receive_data,
    daemon=True
).start()

# ==========================================
# MAIN LOOP
# ==========================================
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = pygame.mouse.get_pos()

            if left_btn.collidepoint(mx, my):
                left_pressed = True

            if right_btn.collidepoint(mx, my):
                right_pressed = True

            if jump_btn.collidepoint(mx, my):

                if not jumping:

                    jumping = True

                    jump_speed = JUMP_POWER

            if attack_btn.collidepoint(mx, my):

                if cooldown == 0:

                    if abs(player_x - enemy_x) < 280:

                        enemy_hp -= 10

                        cooldown = 18

                        attack_timer = 10

                        power += 10

            if skill_btn.collidepoint(mx, my):

                if cooldown == 0:

                    if abs(player_x - enemy_x) < 320:

                        enemy_hp -= 20

                        cooldown = 35

                        attack_timer = 14

                        power += 15

            if power_btn.collidepoint(mx, my):

                if power >= 50 and not ball_active:

                    ball_active = True

                    ball_x = player_x + CHAR_SIZE // 2

                    ball_y = player_y + CHAR_SIZE // 2

                    power -= 50

        if event.type == pygame.MOUSEBUTTONUP:

            mx, my = pygame.mouse.get_pos()

            if left_btn.collidepoint(mx, my):
                left_pressed = False

            if right_btn.collidepoint(mx, my):
                right_pressed = False

    # ======================================
    # MOVEMENT
    # ======================================
    if left_pressed:
        player_x -= PLAYER_SPEED

    if right_pressed:
        player_x += PLAYER_SPEED

    player_x = max(
        0,
        min(WIDTH - CHAR_SIZE, player_x)
    )

    # ======================================
    # JUMP
    # ======================================
    if jumping:

        player_y += jump_speed

        jump_speed += GRAVITY

        if player_y >= GROUND_Y:

            player_y = GROUND_Y

            jumping = False

    # ======================================
    # TIMERS
    # ======================================
    if cooldown > 0:
        cooldown -= 1

    if attack_timer > 0:
        attack_timer -= 1

    if power < 100:
        power += 0.08

    # ======================================
    # POWER BALL
    # ======================================
    if ball_active:

        ball_x += BALL_SPEED

        if abs(ball_x - enemy_x) < 80:

            enemy_hp -= 30

            ball_active = False

        if ball_x > WIDTH:
            ball_active = False

    # ======================================
    # SEND DATA
    # ======================================
    if online:

        try:

            data = {

                "x": player_x,

                "y": player_y,

                "hp": player_hp
            }

            client.send(
                pickle.dumps(data)
            )

        except:
            pass

    # ======================================
    # DRAW
    # ======================================
    screen.fill(BLACK)

    if background:
        screen.blit(background, (0, 0))

    pygame.draw.line(
        screen,
        WHITE,
        (0, GAME_HEIGHT),
        (WIDTH, GAME_HEIGHT),
        4
    )

    # HP BARS
    pygame.draw.rect(
        screen,
        GREEN,
        (20, 20, player_hp * 4, 35)
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (20, 20, 400, 35),
        3
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (WIDTH - 420, 20, enemy_hp * 4, 35)
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (WIDTH - 420, 20, 400, 35),
        3
    )

    # PLAYER
    current_player = (
        gojo_attack_img
        if attack_timer > 0
        else gojo_img
    )

    screen.blit(
        current_player,
        (player_x, player_y)
    )

    # ENEMY
    screen.blit(
        sukuna_img,
        (enemy_x, enemy_y)
    )

    # POWER BALL
    if ball_active:

        pygame.draw.circle(
            screen,
            CYAN,
            (int(ball_x), int(ball_y)),
            35
        )

    # BUTTONS
    buttons = [

        (left_btn, GRAY, "LEFT", False),
        (right_btn, GRAY, "RIGHT", False),

        (jump_btn, BLUE, "JUMP", True),

        (power_btn, CYAN, "POWER", True),

        (skill_btn, PURPLE, "SKILL", True),

        (attack_btn, RED, "ATTACK", True)

    ]

    for btn, color, text, circle in buttons:

        if circle:

            pygame.draw.ellipse(
                screen,
                color,
                btn
            )

            pygame.draw.ellipse(
                screen,
                WHITE,
                btn,
                5
            )

        else:

            pygame.draw.rect(
                screen,
                color,
                btn,
                border_radius=30
            )

            pygame.draw.rect(
                screen,
                WHITE,
                btn,
                5,
                border_radius=30
            )

        txt = small_font.render(
            text,
            True,
            WHITE
        )

        screen.blit(
            txt,
            (
                btn.centerx - txt.get_width() // 2,
                btn.centery - txt.get_height() // 2
            )
        )

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()

sys.exit()
