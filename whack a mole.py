import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Mole")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Load mole image
mole_image = pygame.image.load("mole.png")  # Replace with your mole image file
mole_image = pygame.transform.scale(mole_image, (80, 80))  # Resize the mole
mole_rect = mole_image.get_rect()
mole_visible = False
mole_last_spawn_time = 0
mole_visible_duration = 1.0  # seconds
mole_spawn_interval = 1.5  # seconds

# Load hit sound effect
hit_sound = pygame.mixer.Sound("hit.wav")  # Replace with your hit sound file

# Holes
holes = [
    pygame.Rect(100, 200, 100, 50),
    pygame.Rect(300, 200, 100, 50),
    pygame.Rect(500, 200, 100, 50),
    pygame.Rect(100, 400, 100, 50),
    pygame.Rect(300, 400, 100, 50),
    pygame.Rect(500, 400, 100, 50),
]

# Speed control bar
speed_bar = pygame.Rect(50, 550, 200, 20)
speed_knob = pygame.Rect(50, 545, 10, 30)
min_speed = 0.5
max_speed = 3.0
current_speed = 1.5

# Restart button
restart_button = pygame.Rect(600, 530, 120, 50)

# Score and counters
score = 0
hit_count = 0
miss_count = 0

# Clock
clock = pygame.time.Clock()

def spawn_mole():
    global mole_rect, mole_visible, mole_last_spawn_time
    hole = random.choice(holes)
    mole_rect.center = hole.center
    mole_visible = True
    mole_last_spawn_time = time.time()

def hide_mole():
    global mole_visible
    mole_visible = False

def draw_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def draw_counters():
    hit_text = font.render(f"Hits: {hit_count}", True, GREEN)
    miss_text = font.render(f"Misses: {miss_count}", True, RED)
    screen.blit(hit_text, (10, 50))
    screen.blit(miss_text, (10, 90))

def draw_holes():
    for hole in holes:
        pygame.draw.ellipse(screen, BLACK, hole)

def draw_mole():
    if mole_visible:
        screen.blit(mole_image, mole_rect)

def draw_speed_bar():
    pygame.draw.rect(screen, GRAY, speed_bar)
    pygame.draw.rect(screen, BLACK, speed_knob)
    speed_text = font.render(f"Speed: {current_speed:.1f}x", True, BLACK)
    screen.blit(speed_text, (50, 520))

def draw_restart_button():
    pygame.draw.rect(screen, BLUE, restart_button)
    restart_text = font.render("Restart", True, WHITE)
    screen.blit(restart_text, (restart_button.x + 20, restart_button.y + 15))

def update_speed(pos):
    global current_speed
    if speed_bar.collidepoint(pos):
        current_speed = min_speed + (max_speed - min_speed) * ((pos[0] - speed_bar.x) / speed_bar.width)
        speed_knob.x = pos[0] - speed_knob.width // 2

def check_whack(pos):
    global score, hit_count, miss_count, mole_visible
    if mole_visible and mole_rect.collidepoint(pos):
        score += 1
        hit_count += 1
        mole_visible = False
        hit_sound.play()  # Play hit sound effect
    else:
        miss_count += 1

def reset_game():
    global score, hit_count, miss_count, mole_visible
    score = 0
    hit_count = 0
    miss_count = 0
    mole_visible = False

# Main game loop
running = True
dragging_speed_knob = False
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if speed_knob.collidepoint(event.pos):
                dragging_speed_knob = True
            elif restart_button.collidepoint(event.pos):
                reset_game()
            else:
                check_whack(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_speed_knob = False
        elif event.type == pygame.MOUSEMOTION and dragging_speed_knob:
            update_speed(event.pos)

    # Spawn mole if it's time
    current_time = time.time()
    if not mole_visible and current_time - mole_last_spawn_time >= mole_spawn_interval / current_speed:
        spawn_mole()

    # Hide mole if it's been visible for too long
    if mole_visible and current_time - mole_last_spawn_time >= mole_visible_duration / current_speed:
        hide_mole()

    # Draw everything
    draw_holes()
    draw_mole()
    draw_score()
    draw_counters()
    draw_speed_bar()
    draw_restart_button()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit pygame
pygame.quit()