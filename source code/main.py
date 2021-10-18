import pygame
import random

# Initiating pygame and mixer
pygame.mixer.pre_init(frequency=44100, size=16, channels=1 , buffer=1024)
pygame.init()

# Variables:
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 128, 0)

not_started = True
not_spawning = True

ORIGIN = (0, 0)
ground_X_pos = 0

run = True
not_collided = True

BIRD_STARTING_POS = (50, 280)
bird_pos = 0
gravity = 0.3

pipe_list = []
available_pipe_height = [300, 310, 320, 330, 340, 350,
                         360, 370, 380, 390, 400, 410, 420, 430, 440, 450]

SPAWN_PIPE = ''
BIRD_FLAP = ''

GAP = 200

score = 0
score_sound_countdown = 100

high_score = 0

# Setting the display window
pygame.display.set_caption("Crappy Bird")
pygame.display.set_icon(pygame.image.load("assets/sprites/flappy-bird.png"))

SCREEN_DIMENSIONS = (352, 600)
SCREEN = pygame.display.set_mode(SCREEN_DIMENSIONS)

# Loading sounds
bird_wing = pygame.mixer.Sound("assets/audio/wing.wav")
point_scored = pygame.mixer.Sound("assets/audio/point.wav")
die = pygame.mixer.Sound("assets/audio/die.wav")

# Loading required images as surfaces
START_SCREEN = pygame.image.load("assets/sprites/message.png").convert_alpha()
START_SCREEN = pygame.transform.scale(START_SCREEN, (342, 582))

bg = pygame.image.load("assets/sprites/background-day.png").convert()
bg = pygame.transform.scale(bg, SCREEN_DIMENSIONS)

ground = pygame.image.load("assets/sprites/base.png").convert()
ground = pygame.transform.scale(ground, (352, 75))

bird_down = pygame.image.load("assets/sprites/yellowbird-downflap.png").convert_alpha()
bird_down = pygame.transform.scale(bird_down, (50, 34))

bird_mid = pygame.image.load("assets/sprites/yellowbird-midflap.png").convert_alpha()
bird_mid = pygame.transform.scale(bird_mid, (50, 34))

bird_up = pygame.image.load("assets/sprites/yellowbird-upflap.png").convert_alpha()
bird_up = pygame.transform.scale(bird_up, (50, 34))

bird_frames = [bird_down, bird_mid, bird_up]
bird_index = 0

bird = bird_frames[bird_index]

pipe = pygame.image.load("assets/sprites/pipe-red.png").convert()
pipe = pygame.transform.scale(pipe, (72, 320))

font = pygame.font.Font("assets/fonts/04B_19__.TTF", 40)

_game_over = pygame.image.load("assets/sprites/gameover.png").convert_alpha()
_game_over = pygame.transform.scale(_game_over, (342, 73))

GAME_TITLE = font.render("Crappy Bird", False, ORANGE)
GAME_START_MSG = font.render("Press any key", False, BLACK)
GAME_END_MESSAGE = font.render("Press any key", False, BLACK)

# Loading required rectangles
bird_rect = bird.get_rect(center=BIRD_STARTING_POS)

GAME_TITLE_RECT = GAME_TITLE.get_rect(center=(176, 200))
GAME_START_MSG_RECT = GAME_START_MSG.get_rect(center=(176, 525))
GAME_END_MESSAGE_RECT = GAME_END_MESSAGE.get_rect(center=(176, 475))


# Start screen
def start():
    SCREEN.fill(WHITE)
    SCREEN.blit(START_SCREEN, (5, 9))

    SCREEN.blit(GAME_TITLE, GAME_TITLE_RECT)
    SCREEN.blit(GAME_START_MSG, GAME_START_MSG_RECT)


# Animations
def rotate_bird(_bird):
    new_bird = pygame.transform.rotozoom(_bird, bird_pos * -4, 1)
    return new_bird


# This shows the score
def score_update():
    score_surface = font.render("Score = " + str(int(score)), False, WHITE)
    score_rect = score_surface.get_rect(center=(176, 75))

    SCREEN.blit(score_surface, score_rect)


# This updates the high score
def high_score_update(_high_score):
    if score > _high_score:
        _high_score = score
    else:
        pass

    return _high_score


# This updates the bird
def get_bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))

    return new_bird, new_bird_rect


# This will load all the required surfaces of entities
def update(_pipe_list):
    # Loading in background surfaces
    SCREEN.blit(bg, ORIGIN)

    # Loading in the bird
    SCREEN.blit(rotated_bird, bird_rect)

    # Loading in the pipes
    for _pipe in _pipe_list:
        if _pipe.bottom >= 600:
            SCREEN.blit(pipe, _pipe)
        else:
            _pipe_ = pygame.transform.flip(pipe, False, True)
            SCREEN.blit(_pipe_, _pipe)

    # Loading in the ground
    SCREEN.blit(ground, (ground_X_pos, 525))
    SCREEN.blit(ground, (ground_X_pos + 352, 525))


# This will spawn in pipes
def spawn_pipe():
    seed = random.choice(available_pipe_height)

    bottom_pipe = pipe.get_rect(midtop=(360, seed))
    top_pipe = pipe.get_rect(midbottom=(360, seed - GAP))

    return bottom_pipe, top_pipe


# Puts the pipe in their correct positions
def pipe_pos(_pipe_list):
    for _pipe in _pipe_list:
        _pipe.centerx -= 5

    return _pipe_list


# This checks if the bird has collided with anything or not
def collision_checker(_pipe_list):
    for _pipe in _pipe_list:
        if bird_rect.colliderect(_pipe):
            die.play()
            return False
        else:
            pass

        if bird_rect.bottom >= 520 or bird_rect.top <= 5:
            die.play()
            return False
        else:
            pass

    return True


# This updates the game over screen
def game_over():
    SCREEN.fill(WHITE)
    SCREEN.blit(_game_over, (5, 261.5))

    score_surface = font.render(f"Score = {str(int(score))}", False, BLACK)
    score_rect = score_surface.get_rect(center=(176, 75))

    high_score_surface = font.render(f"High Score = {str(int(high_score))}", False, BLACK)
    high_score_rect = high_score_surface.get_rect(center=(176, 150))

    SCREEN.blit(high_score_surface, high_score_rect)
    SCREEN.blit(score_surface, score_rect)

    SCREEN.blit(GAME_END_MESSAGE, GAME_END_MESSAGE_RECT)


# This is the main loop for running the game
while run:
    # Setting a fixed frame rate
    pygame.time.Clock().tick(FPS)

    # Starting the spawning
    if not not_started and not_spawning:
        # Spawning pipes
        SPAWN_PIPE = pygame.USEREVENT
        pygame.time.set_timer(SPAWN_PIPE, 1010)

        # Cycling through the frames
        BIRD_FLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(BIRD_FLAP, 125)

        # To NOT restart the spawning
        not_spawning = False

    # Start screen
    if not_started:
        start()

    # Running the game
    elif not_collided:
        rotated_bird = rotate_bird(bird)
        bird, bird_rect = get_bird_animation()

        update(pipe_list)

        score_update()
        score += 0.02
        score_sound_countdown -= 1.98

        if score_sound_countdown <= 0:
            point_scored.play()
            score_sound_countdown = 100

        ground_X_pos -= 5

        if ground_X_pos <= -352:
            ground_X_pos = 0
        else:
            pass

        bird_pos += gravity
        bird_rect.centery += bird_pos

        pipe_list = pipe_pos(pipe_list)

        not_collided = collision_checker(pipe_list)

    # Ending the game
    elif not not_collided:
        high_score = high_score_update(high_score)

        game_over()


    # Checking if the game needs to be closed
    for event in pygame.event.get():
        if event.type == SPAWN_PIPE:
            pipe_list.extend(spawn_pipe())
        else:
            pass

        if event.type == pygame.KEYDOWN:
            if not_started:
                not_started = False
            else:
                pass

            if event.key == pygame.K_SPACE and not_collided:
                bird_wing.play()
                bird_pos = 0
                bird_pos -= 8.25
            else:
                pass

            if not not_collided:
                bird_pos = 0
                bird_rect.center = BIRD_STARTING_POS

                pipe_list.clear()

                score = 0

                not_collided = True
            else:
                pass
        else:
            pass

        if event.type == pygame.QUIT:
            run = False
        else:
            pass

        if event.type == BIRD_FLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

    pygame.display.update()

pygame.quit()
