import pygame
import random
import sys

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Constants
WIDTH = 800
HEIGHT = 400
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner")
clock = pygame.time.Clock()

# Player properties
player_normal_width = 40
player_normal_height = 40
player_large_width = 70
player_large_height = 70
player_width = player_normal_width
player_height = player_normal_height
player_x = 100
player_y = HEIGHT - player_height - 60  # Raised to match grass
player_velocity = 0
jump_power = -15
gravity = 0.8
player_large = False

# Obstacle properties
obstacle_width = 30
obstacle_height = 50
obstacle_speed = 5
obstacles = []
min_gap = 200
max_gap = 400
last_obstacle = WIDTH

# Food properties
food_width = 40
food_height = 40
food_speed = 5
foods = []

# Energy properties
energy_width = 50
energy_height = 50
energy_speed = 5
energies = []

# Shit properties
shit_width = 40
shit_height = 40
shit_speed = 5
shits = []

# Game variables
score = 0
game_over = False
font = pygame.font.Font(None, 36)
high_score = 0
frame_count = 0

# Load images ONCE
hero_img_normal = pygame.image.load("hero.png")
hero_img_normal = pygame.transform.scale(hero_img_normal, (player_normal_width, player_normal_height))
hero_img_large = pygame.transform.scale(pygame.image.load("hero.png"), (player_large_width, player_large_height))
background_img = pygame.image.load("background.jpeg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
food_img = pygame.image.load("food.png")
food_img = pygame.transform.scale(food_img, (food_width, food_height))
energy_img = pygame.image.load("Energy.png")
energy_img = pygame.transform.scale(energy_img, (energy_width, energy_height))
shit_img = pygame.image.load("shit.png")
shit_img = pygame.transform.scale(shit_img, (shit_width, shit_height))

# Load sounds
pygame.mixer.music.load("backgroundsound.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop forever

cat_sound = pygame.mixer.Sound("catsound.wav")
cat_sound.set_volume(0.7)

# Background scrolling
bg_x1 = 0
bg_x2 = WIDTH

def spawn_obstacle():
    gap = random.randint(min_gap + obstacle_speed * 10, max_gap + obstacle_speed * 10)
    x = WIDTH + gap
    obstacles.append(pygame.Rect(x, HEIGHT - obstacle_height - 60, obstacle_width, obstacle_height))
    return x

def spawn_food():
    if len(foods) < 2 and random.randint(0, 1000) < 10:
        x = WIDTH + random.randint(200, 500)
        y = HEIGHT - food_height - random.randint(80, 120)
        foods.append(pygame.Rect(x, y, food_width, food_height))

def spawn_energy():
    if len(energies) < 1 and random.randint(0, 1000) < 5:
        x = WIDTH + random.randint(400, 700)
        y = HEIGHT - energy_height - random.randint(120, 180)
        energies.append(pygame.Rect(x, y, energy_width, energy_height))

def spawn_shit():
    if len(shits) < 1 and random.randint(0, 1000) < 7:
        x = WIDTH + random.randint(350, 600)
        y = HEIGHT - shit_height - random.randint(80, 120)
        shits.append(pygame.Rect(x, y, shit_width, shit_height))

def draw_player(x, y, large):
    if large:
        screen.blit(hero_img_large, (x, y - (player_large_height - player_normal_height)))
    else:
        screen.blit(hero_img_normal, (x, y))

def draw_obstacle(obstacle):
    pygame.draw.rect(screen, RED, obstacle)

def draw_food(food):
    screen.blit(food_img, (food.x, food.y))

def draw_energy(energy):
    screen.blit(energy_img, (energy.x, energy.y))

def draw_shit(shit):
    screen.blit(shit_img, (shit.x, shit.y))

def can_jump(player_y, player_large):
    # Only allow jump if on ground
    if player_large:
        return player_y == HEIGHT - player_large_height - 60
    else:
        return player_y == HEIGHT - player_normal_height - 60

def main():
    global player_y, player_velocity, score, game_over, obstacles, last_obstacle
    global foods, high_score, player_width, player_height, player_large, energies, shits, frame_count
    global obstacle_speed, food_speed, energy_speed, shit_speed, jump_power
    global bg_x1, bg_x2

    # Reset game state
    player_width = player_normal_width
    player_height = player_normal_height
    player_large = False
    player_y = HEIGHT - player_height - 60
    player_velocity = 0
    obstacles = []
    last_obstacle = WIDTH
    score = 0
    game_over = False
    foods = []
    energies = []
    shits = []
    frame_count = 0
    obstacle_speed = 5
    food_speed = 5
    energy_speed = 5
    shit_speed = 5
    bg_x1 = 0
    bg_x2 = WIDTH

    running = True
    while running:
        frame_count += 1
        # Gradually increase speed
        speed_increase = frame_count // (FPS * 10)  # Every 10 seconds
        obstacle_speed = 5 + speed_increase
        food_speed = 5 + speed_increase
        energy_speed = 5 + speed_increase
        shit_speed = 5 + speed_increase
        bg_speed = obstacle_speed // 2 + 2

        # Adjust jump power for large character
        if player_large:
            jump_power = -18  # Stronger jump for large character
        else:
            jump_power = -15

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mobile-friendly: jump on SPACE or mouse/touch
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        main()  # Restart game
                    elif can_jump(player_y, player_large):
                        player_velocity = jump_power
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    main()
                elif can_jump(player_y, player_large):
                    player_velocity = jump_power

        if not game_over:
            # Background scroll
            bg_x1 -= bg_speed
            bg_x2 -= bg_speed
            if bg_x1 <= -WIDTH:
                bg_x1 = WIDTH
            if bg_x2 <= -WIDTH:
                bg_x2 = WIDTH

            # Update player
            player_velocity += gravity
            player_y += player_velocity
            ground_y = HEIGHT - player_height - 60 if not player_large else HEIGHT - player_large_height - 60
            if player_y > ground_y:
                player_y = ground_y
                player_velocity = 0

            # Update obstacles
            for obstacle in obstacles[:]:
                obstacle.x -= obstacle_speed
                if obstacle.x < -obstacle_width:
                    obstacles.remove(obstacle)

            # Spawn new obstacles
            if last_obstacle < WIDTH:
                last_obstacle = spawn_obstacle()

            # Food logic
            spawn_food()
            for food in foods[:]:
                food.x -= food_speed
                if food.x < -food_width:
                    foods.remove(food)
                elif pygame.Rect(player_x, player_y, player_width if not player_large else player_large_width, player_height if not player_large else player_large_height).colliderect(food):
                    score += 1
                    cat_sound.play()
                    foods.remove(food)

            # Energy logic
            spawn_energy()
            for energy in energies[:]:
                energy.x -= energy_speed
                if energy.x < -energy_width:
                    energies.remove(energy)
                elif pygame.Rect(player_x, player_y, player_width if not player_large else player_large_width, player_height if not player_large else player_large_height).colliderect(energy):
                    player_large = True
                    player_width = player_large_width
                    player_height = player_large_height
                    energies.remove(energy)
                    # Do NOT reset player_y here! Motion continues.

            # Shit logic
            spawn_shit()
            for shit in shits[:]:
                shit.x -= shit_speed
                if shit.x < -shit_width:
                    shits.remove(shit)
                elif pygame.Rect(player_x, player_y, player_width if not player_large else player_large_width, player_height if not player_large else player_large_height).colliderect(shit):
                    if player_large:
                        player_large = False
                        player_width = player_normal_width
                        player_height = player_normal_height
                        player_y = HEIGHT - player_height - 60
                        shits.remove(shit)
                    else:
                        game_over = True

            # Check collisions with obstacles
            player_rect = pygame.Rect(player_x, player_y, player_width if not player_large else player_large_width, player_height if not player_large else player_large_height)
            for obstacle in obstacles:
                if player_rect.colliderect(obstacle):
                    game_over = True

            # Update high score
            if score > high_score:
                high_score = score

        # Draw everything
        screen.blit(background_img, (bg_x1, 0))
        screen.blit(background_img, (bg_x2, 0))
        draw_player(player_x, player_y, player_large)
        for obstacle in obstacles:
            draw_obstacle(obstacle)
        for food in foods:
            draw_food(food)
        for energy in energies:
            draw_energy(energy)
        for shit in shits:
            draw_shit(shit)

        # Draw score and high score
        score_text = font.render(f"Score: {score}  High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Draw game over screen
        if game_over:
            game_over_text = font.render("Game Over! Tap or Press SPACE to restart", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()