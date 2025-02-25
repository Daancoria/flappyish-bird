import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_X, BIRD_Y = 50, HEIGHT // 2
BIRD_RADIUS = 15
gravity = 0.5
jump_strength = -8
pipe_width = 70
gap_height = 150
pipe_speed = 3
score = 0

# Colors
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (34, 139, 34)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Clock for frame rate
clock = pygame.time.Clock()

# Bird attributes
bird_y = BIRD_Y
bird_velocity = 0

# Pipe attributes
pipes = []
pipe_movements = {}

def create_pipe():
    height = random.randint(100, 400)
    pipes.append([WIDTH, height])
    pipe_movements[WIDTH] = random.choice([-1, 1])

def move_pipes():
    global score
    for pipe in pipes:
        pipe[0] -= pipe_speed
        if pipe[0] in pipe_movements:
            pipe[1] += pipe_movements[pipe[0]] * 2  # Move pipes up and down
            if pipe[1] <= 50 or pipe[1] >= HEIGHT - gap_height - 50:
                pipe_movements[pipe[0]] *= -1  # Reverse direction
    
    if pipes and pipes[0][0] + pipe_width < 0:
        pipe_movements.pop(pipes[0][0], None)
        pipes.pop(0)
        score += 1

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, DARK_GREEN, (pipe[0], 0, pipe_width, pipe[1]))
        pygame.draw.rect(screen, DARK_GREEN, (pipe[0], pipe[1] + gap_height, pipe_width, HEIGHT - pipe[1] - gap_height))

def check_collision():
    if bird_y - BIRD_RADIUS <= 0 or bird_y + BIRD_RADIUS >= HEIGHT:
        return True
    for pipe in pipes:
        if (BIRD_X + BIRD_RADIUS > pipe[0] and BIRD_X - BIRD_RADIUS < pipe[0] + pipe_width):
            if bird_y - BIRD_RADIUS < pipe[1] or bird_y + BIRD_RADIUS > pipe[1] + gap_height:
                return True
    return False

def draw_bird():
    pygame.draw.circle(screen, ORANGE, (BIRD_X, int(bird_y)), BIRD_RADIUS)

def show_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

# Game loop
running = True
frame_count = 0
while running:
    screen.fill(LIGHT_BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = jump_strength
    
    # Bird physics
    bird_velocity += gravity
    bird_y += bird_velocity
    
    # Pipe handling
    if frame_count % 90 == 0:
        create_pipe()
    move_pipes()
    
    # Drawing
    draw_pipes()
    draw_bird()
    show_score()
    
    # Check for collisions
    if check_collision():
        running = False
    
    pygame.display.update()
    clock.tick(30)
    frame_count += 1

pygame.quit()
