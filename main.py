import pygame
import random
import argparse
from core import get_note_onsets

parser = argparse.ArgumentParser(prog='TaikoChaos')
parser.add_argument('--track', help='.mp3 track file to generate chart')
args = parser.parse_args()
track_file = args.track

# Sound utilities
pygame.mixer.init()
pygame.mixer.music.load(track_file)
face = pygame.mixer.Sound('.\\drum_sounds\\face.wav')
rim = pygame.mixer.Sound('.\\drum_sounds\\rim.wav')

# Adjust volumes
pygame.mixer.music.set_volume(0.5)
face.set_volume(1)
rim.set_volume(1)

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
circle_radius = 20
pixels_per_second = 200
drum_circle = (50 + circle_radius, HEIGHT // 2)
drum_color = CIRCLE_COLOR_DRUM_DEFAULT
drum_hit_length_in_frames = 3
drum_hit_frames_left = 0
border_thickness = 5
border_color = (0, 0, 0)

# input
onset_in_seconds = get_note_onsets(track_file, None)

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

pygame.mixer.music.play()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f or event.key == pygame.K_j:
                drum_color = CIRCLE_COLOR_RED
                drum_hit_frames_left = drum_hit_length_in_frames
                face.play()
            elif event.key == pygame.K_d or event.key == pygame.K_k:
                drum_color = CIRCLE_COLOR_BLUE
                drum_hit_frames_left = drum_hit_length_in_frames
                rim.play()

    elapsed_s = (pygame.time.get_ticks() - start_tick) / 1000
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(f"Elapsed: {elapsed_s:.2f} s", True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

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
            pygame.draw.circle(screen, border_color, (c["x"], c["y"]), circle_radius + border_thickness)
            pygame.draw.circle(screen, c["color"], (c["x"], c["y"]), circle_radius)
            alive_circle_count += 1

    pygame.display.flip()
    clock.tick(frames_per_second)

pygame.quit()
