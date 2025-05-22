import os
import pygame
import math
import random
import argparse
from core import get_note_onsets

parser = argparse.ArgumentParser(prog='TaikoChaos')
parser.add_argument('--track', help='.mp3 track file in \input to generate chart')
args = parser.parse_args()
track_file = args.track

# input
onset_in_seconds = get_note_onsets(track_file, None)
assert(sorted(onset_in_seconds))

optimal_beat_per_second = None
optimal_sos = math.inf
bps_candidates = [1 / x for x in range(1, 17)]

for beat_per_second in bps_candidates:
    sum_of_squares = 0
    for t in onset_in_seconds:
        d_lo = math.floor(t / beat_per_second) * beat_per_second
        d_hi = math.ceil(t / beat_per_second) * beat_per_second
        sum_of_squares += (min(abs(d_lo - t), abs(d_hi - t))) ** 2
    if sum_of_squares < optimal_sos:
        optimal_sos = sum_of_squares
        optimal_beat_per_second = beat_per_second

assert(optimal_beat_per_second is not None)

for i in range(len(onset_in_seconds)):
    t = onset_in_seconds[i]
    d_lo = math.floor(t / beat_per_second) * beat_per_second
    d_hi = math.ceil(t / beat_per_second) * beat_per_second
    onset_in_seconds[i] = d_lo if abs(d_lo - t) < abs(d_hi - t) else d_hi

onset_in_seconds =  list(set(onset_in_seconds))
onset_in_seconds.sort()

# Sound utilities
pygame.mixer.init()
pygame.mixer.music.load(os.path.join("input", track_file))
face = pygame.mixer.Sound('.\\drum_sounds\\face.wav')
rim = pygame.mixer.Sound('.\\drum_sounds\\rim.wav')

# Adjust volumes
pygame.mixer.music.set_volume(0.1)
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
NOTE_BAND_COLOR = (255, 255, 255)
CIRCLE_COLOR_RED = (255, 100, 100)
CIRCLE_COLOR_BLUE = (100, 100, 255)
CIRCLE_COLOR_DRUM_DEFAULT = (211, 211, 211)
CIRCLE_COLOR_BAD = (128, 0, 128)

# Game settings
READ_RANGE = 15
HIT_RANGE = 12

# Circle settings
circle_radius = 20
pixels_per_second = 200
drum_circle = (100 + circle_radius, HEIGHT // 2)
drum_circle_radious = circle_radius + 8
drum_color = CIRCLE_COLOR_DRUM_DEFAULT
drum_hit_length_in_frames = 3
drum_hit_frames_left = 0
border_thickness = 5
border_color = (0, 0, 0)

circles = []

for t in onset_in_seconds:
    circles.append({
        "x": drum_circle[0] + pixels_per_second * t,
        "y": drum_circle[1],
        "v": pixels_per_second,
        "color": random.choice([CIRCLE_COLOR_RED, CIRCLE_COLOR_BLUE]),
        "disabled": False,
        "visible": True,
    })

# GAME LOOP

clock.tick(frames_per_second)

pygame.mixer.music.play()

start_tick = pygame.time.get_ticks()
running = True
combo = 0
score = 0

while running:
    
    delta_ms = clock.tick(frames_per_second)
    delta_s = delta_ms / 1000

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

    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, NOTE_BAND_COLOR, ((0, HEIGHT // 2 - circle_radius - 10, WIDTH, 2 * circle_radius + 20)))

    elapsed_s = (pygame.time.get_ticks() - start_tick) / 1000
    alive_circle_count = 0

    font = pygame.font.SysFont(None, 36)
    elapsed_text = font.render(f"Elapsed: {elapsed_s:.2f} s", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    combo_text = font.render(f"Combo: {combo}", True, (255, 255, 255))
    screen.blit(elapsed_text, (10, 10))
    screen.blit(score_text, (10, 50))
    screen.blit(combo_text, (10, 100))

    pygame.draw.circle(screen, drum_color, drum_circle, drum_circle_radious)
    if drum_color != CIRCLE_COLOR_DRUM_DEFAULT:
        drum_hit_frames_left -= 1
        if drum_hit_frames_left == 0:
            drum_color = CIRCLE_COLOR_DRUM_DEFAULT

    for c in circles:
        c["x"] -= delta_s * c["v"]

        if c["x"] > 0 and c["visible"]:
            pygame.draw.circle(screen, border_color, (c["x"], c["y"]), circle_radius + border_thickness)
            pygame.draw.circle(screen, c["color"], (c["x"], c["y"]), circle_radius)
            alive_circle_count += 1

        drum_hit = (drum_hit_frames_left == drum_hit_length_in_frames - 1)
        is_correct_note = (drum_color == c["color"])
        is_within_range = (abs(c["x"] - drum_circle[0]) <= READ_RANGE)
        is_within_scoring_range = (abs(c["x"] - drum_circle[0]) <= HIT_RANGE)

        if not c["disabled"] and drum_hit and is_within_range:
            if is_within_scoring_range and is_correct_note:
                score += 1
                combo += 1
                c["visible"] = False
            else:
                combo = 0
                c["color"] = CIRCLE_COLOR_BAD
                print("rip", abs(c["x"] - drum_circle[0]))
                # c["visible"] = False
            c["disabled"] = True

        if not c["disabled"] and c["x"] < drum_circle[0] - READ_RANGE:
            c["disabled"] = True
            combo = 0

        if c["x"] < 0:
            c["visible"] = False

    pygame.display.flip()

pygame.quit()
