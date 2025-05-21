import pygame
import random

# Sound utilities
pygame.mixer.init()
drum = pygame.mixer.Sound('.\\mixed_drum.wav')

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
frames_per_second = 60

# Screen settings
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TaikoChaos")

# Colors
BG_COLOR = (30, 30, 30)
CIRCLE_COLOR_RED = (255, 100, 100)
CIRCLE_COLOR_BLUE = (100, 100, 255)
CIRCLE_COLOR_DRUM_DEFAULT = (211, 211, 211)

# Circle settings
center = (WIDTH // 2, HEIGHT // 2)
circle_radius = 20
pixels_per_second = 200
drum_circle = (50 + circle_radius, HEIGHT // 2)
drum_color = CIRCLE_COLOR_DRUM_DEFAULT
drum_hit_length_in_frames = 3
drum_hit_frames_left = 0

# input
onset_in_seconds = [5, 5.5, 6, 6.5, 7, 7.25, 7.5, 8.5, 8.75, 9.25, 9.5]

circles = []

for t in onset_in_seconds:
    circles.append({
        "x": drum_circle[0] + pixels_per_second * t,
        "y": drum_circle[1],
        "v": pixels_per_second,
        "color": random.choice([CIRCLE_COLOR_RED, CIRCLE_COLOR_BLUE])
    })

start_tick = pygame.time.get_ticks()
running = True

while running:

    elapsed_s = (pygame.time.get_ticks() - start_tick) / 1000
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(f"Elapsed: {elapsed_s:.2f} s", True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                drum_color = CIRCLE_COLOR_RED
                drum_hit_frames_left = drum_hit_length_in_frames
                drum.play()
            elif event.key == pygame.K_k:
                drum_color = CIRCLE_COLOR_BLUE
                drum_hit_frames_left = drum_hit_length_in_frames
                drum.play()

    alive_circle_count = 0

    screen.fill(BG_COLOR)

    pygame.draw.circle(screen, drum_color, drum_circle, circle_radius)
    if drum_color != CIRCLE_COLOR_DRUM_DEFAULT:
        drum_hit_frames_left -= 1
        if drum_hit_frames_left == 0:
            drum_color = CIRCLE_COLOR_DRUM_DEFAULT

    for c in circles:
        c["x"] -= 1 / frames_per_second * c["v"]
        if c["x"] > 0:
            pygame.draw.circle(screen, c["color"], (int(c["x"]), int(c["y"])), circle_radius)
            alive_circle_count += 1

    pygame.display.flip()
    clock.tick(frames_per_second)

pygame.quit()
