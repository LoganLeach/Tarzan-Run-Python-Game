import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
PLAYER_SIZE = 80
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 30
POWER_UP_SIZE = 20
FPS = 60

# Difficulty settings
DIFFICULTY_SETTINGS = {
    "easy": {"obstacle_speed": 5, "obstacle_spawn_chance": 5, "power_up_spawn_chance": 2},
    "medium": {"obstacle_speed": 7, "obstacle_spawn_chance": 7, "power_up_spawn_chance": 4},
    "hard": {"obstacle_speed": 10, "obstacle_spawn_chance": 10, "power_up_spawn_chance": 6},
}

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.Font(None, 36)

# Load player image
player_image = pygame.image.load("images/player.png")
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

# Load power-up image
power_up_image = pygame.image.load("images/coin.png")
power_up_image = pygame.transform.scale(power_up_image, (POWER_UP_SIZE, POWER_UP_SIZE))

# Player position
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT - PLAYER_SIZE - 10

# Obstacles
obstacles = []

# Power-ups
power_ups = []

# Score
score = 0

# High score
high_score = 0

# Difficulty
current_difficulty = None

# Load background image
background_image = pygame.image.load("images/background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Function to render outlined text
def render_text(text, font, color, outline_color, position):
    base_text = font.render(text, True, color)
    outline_text = font.render(text, True, outline_color)
    outline_rect = outline_text.get_rect(topleft=position)
    screen.blit(outline_text, (outline_rect.x - 2, outline_rect.y - 2))
    screen.blit(base_text, outline_rect)

# Function to set up a new game
def setup_game():
    global player_x, player_y, obstacles, power_ups, score
    player_x = WIDTH // 2 - PLAYER_SIZE // 2
    player_y = HEIGHT - PLAYER_SIZE - 10
    obstacles = []
    power_ups = []
    score = 0

# Function to display instructions
def display_instructions():
    screen.fill((0, 0, 0))  # Fill screen with black background

    instructions = [
        "Instructions:",
        " - Use LEFT and RIGHT arrow keys to move.",
        " - Avoid red obstacles.",
        " - Collect coins for points.",
        " - Power-ups give bonus points.",
        " - Select difficulty at the start.",
        " - Have fun!",
        " - Press space bar to select difficulty",

    ]

    y_offset = 20
    x_offset = WIDTH // 6  # Adjusted x-coordinate for instructions
    for line in instructions:
        render_text(line, font, (255, 255, 255), (0, 0, 0), (x_offset, y_offset))
        y_offset += 40

    pygame.display.flip()

# Function to display difficulty options
def display_difficulty_options():
    render_text("Select Difficulty:", font, (255, 255, 255), (0, 0, 0), (WIDTH // 4, HEIGHT // 2 + 20))
    render_text("1. Easy", font, (255, 255, 255), (0, 0, 0), (WIDTH // 4, HEIGHT // 2 + 60))
    render_text("2. Medium", font, (255, 255, 255), (0, 0, 0), (WIDTH // 4, HEIGHT // 2 + 100))
    render_text("3. Hard", font, (255, 255, 255), (0, 0, 0), (WIDTH // 4, HEIGHT // 2 + 140))

# Instructions and Difficulty selection loop
selection_complete = False
while not selection_complete:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    display_instructions()

    if keys[pygame.K_SPACE]:
        selection_complete = True

    pygame.display.flip()
    clock.tick(FPS)

# Difficulty selection loop
difficulty_selected = False
while not difficulty_selected:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))  # Fill screen with black background

    display_difficulty_options()

    if keys[pygame.K_1]:
        current_difficulty = "easy"
        difficulty_selected = True

    elif keys[pygame.K_2]:
        current_difficulty = "medium"
        difficulty_selected = True

    elif keys[pygame.K_3]:
        current_difficulty = "hard"
        difficulty_selected = True

    pygame.display.flip()
    clock.tick(FPS)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Move player
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE:
        player_x += 5

    # Generate obstacles based on difficulty settings
    if random.randint(0, 100) < DIFFICULTY_SETTINGS[current_difficulty]["obstacle_spawn_chance"]:
        obstacle_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
        obstacle_y = 0
        obstacles.append([obstacle_x, obstacle_y])

    # Generate power-ups based on difficulty settings
    if random.randint(0, 100) < DIFFICULTY_SETTINGS[current_difficulty]["power_up_spawn_chance"]:
        power_up_x = random.randint(0, WIDTH - POWER_UP_SIZE)
        power_up_y = 0
        power_ups.append([power_up_x, power_up_y])

    # Move obstacles based on difficulty settings
    for obstacle in obstacles:
        obstacle[1] += DIFFICULTY_SETTINGS[current_difficulty]["obstacle_speed"]

    # Move power-ups based on difficulty settings
    for power_up in power_ups:
        power_up[1] += DIFFICULTY_SETTINGS[current_difficulty]["obstacle_speed"]

    # Remove off-screen obstacles
    obstacles = [obstacle for obstacle in obstacles if obstacle[1] < HEIGHT]

    # Remove off-screen power-ups
    power_ups = [power_up for power_up in power_ups if power_up[1] < HEIGHT]

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if (
            player_x < obstacle[0] + OBSTACLE_WIDTH
            and player_x + PLAYER_SIZE > obstacle[0]
            and player_y < obstacle[1] + OBSTACLE_HEIGHT
            and player_y + PLAYER_SIZE > obstacle[1]
        ):
            # Player collided with an obstacle
            game_over_text = "YOU DIED! Score: {}".format(score)
            render_text(game_over_text, font, (255, 255, 255), (0, 0, 0), (WIDTH // 4, HEIGHT // 2))
            pygame.display.flip()

            pygame.time.delay(2000)  # Pause for 2 seconds

            # Update high score if necessary
            if score > high_score:
                high_score = score

            obstacles = []
            power_ups = []
            setup_game()

    # Check for collisions with power-ups
    for power_up in power_ups:
        if (
            player_x < power_up[0] + POWER_UP_SIZE
            and player_x + PLAYER_SIZE > power_up[0]
            and player_y < power_up[1] + POWER_UP_SIZE
            and player_y + PLAYER_SIZE > power_up[1]
        ):
            # Player collected a power-up
            score += 10
            power_ups.remove(power_up)

    # Update score
    score += 1

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw score and high score
    render_text("Score: {}".format(score), font, (255, 255, 255), (0, 0, 0), (10, 10))
    render_text("High Score: {}".format(high_score), font, (255, 255, 255), (0, 0, 0), (10, 50))
    render_text("Difficulty: {}".format(current_difficulty.capitalize()), font, (255, 255, 255), (0, 0, 0), (10, 90))

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), (obstacle[0], obstacle[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

    # Draw power-ups
    for power_up in power_ups:
        screen.blit(power_up_image, (power_up[0], power_up[1]))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)
