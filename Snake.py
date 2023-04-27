import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 300
HEIGHT = 300
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Set up the snake
SNAKE_SIZE = 20
snake = [(100, 100), (80, 100), (60, 100)]
direction = "right"
face = "right"


def game_over_screen(score):
    # Create a font object to render the text
    font = pygame.font.SysFont(None, 48)
    # Create a text surface for the score
    score_text = font.render("Your score: " + str(score), True, (255, 255, 255))
    # Create a rectangle to center the score text
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2-50))
    # Create a rectangle for the replay button
    replay_button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2, 120, 50)
    # Display the score and game over message
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Fill the screen with black
        window.fill((0, 0, 0))
        # Blit the score text to the screen
        window.blit(score_text, score_rect)
        # Draw the replay button
        pygame.draw.rect(window, (255, 255, 255), replay_button_rect)
        replay_text = font.render("  Replay", True, (0, 0, 0))
        window.blit(replay_text, (replay_button_rect.x - 15, replay_button_rect.y + 10))
        # Check if the mouse is hovering over the replay button
        mouse_pos = pygame.mouse.get_pos()
        if replay_button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                # Reset the game
                global snake, direction, face, food_pos
                snake = [(100, 100), (80, 100), (60, 100)]
                direction = "right"
                face = "right"
                food_pos = generate_food()
                return
            else:
                pygame.draw.rect(window, (0, 0, 0), replay_button_rect)
                replay_text = font.render("  Replay", True, (255, 255, 255))
                window.blit(replay_text, (replay_button_rect.x - 15, replay_button_rect.y + 10))

        # Update the display
        pygame.display.update()


# Function to generate a new location for the food
def generate_food():
    x = random.randrange(0, WIDTH-10, 20)
    y = random.randrange(0, HEIGHT-10, 20)
    while (x % 10 != 0) or (y % 10 != 0):
        x = random.randrange(0, WIDTH-10, 20)
        y = random.randrange(0, HEIGHT-10, 20)
    return x, y


# Set up the food
food_size = 20
food_pos = generate_food()

# Set up the font
font = pygame.font.SysFont(None, 24)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over_screen(len(snake) - 3)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and face != "left":
                direction = "right"
            elif event.key == pygame.K_LEFT and face != "right":
                direction = "left"
            elif event.key == pygame.K_UP and face != "down":
                direction = "up"
            elif event.key == pygame.K_DOWN and face != "up":
                direction = "down"
    flag = False
    # Update the snake's position based on the player's input
    if direction == "right":
        new_head = (snake[0][0] + SNAKE_SIZE, snake[0][1])
        face = "right"
    elif direction == "left":
        new_head = (snake[0][0] - SNAKE_SIZE, snake[0][1])
        face = "left"
    elif direction == "up":
        new_head = (snake[0][0], snake[0][1] - SNAKE_SIZE)
        face = "up"
    elif direction == "down":
        new_head = (snake[0][0], snake[0][1] + SNAKE_SIZE)
        face = "down"
    else:
        flag = True

    # If food generated on snake, add a new segment to the snake and generate a new location for the food
    for body_part in snake:
        if food_pos[0] == body_part[0] and food_pos[1] == body_part[1]:
            food_pos = generate_food()
            break

    # Check for collisions with the edges of the screen
    if new_head[0] >= WIDTH or new_head[0] < 0 or new_head[1] >= HEIGHT or new_head[1] < 0:
        game_over_screen(len(snake) - 3)
        continue
    # Check for collisions with the food
    if new_head[0] == food_pos[0] and new_head[1] == food_pos[1]:
        snake.insert(0, new_head)  # Add a new segment to the snake
        food_pos = generate_food()  # Generate a new location for the food
    else:
        snake.pop()  # Remove the tail segment of the snake
        snake.insert(0, new_head)  # Add the new head segment of the snake

    # Check for collisions with the snake's body exclude turning back
    for body_part in snake[1:]:
        if new_head == body_part and not flag:
            game_over_screen(len(snake) - 3)
            continue
    # Draw the snake
    window.fill((0, 0, 0))  # Black
    for body_part in snake:
        pygame.draw.rect(window, (0, 255, 0), (body_part[0], body_part[1], SNAKE_SIZE, SNAKE_SIZE))

    # Draw the food
    pygame.draw.rect(window, (255, 0, 0), (food_pos[0], food_pos[1], food_size, food_size))

    # Draw the score
    score_text = font.render("Score: " + str(len(snake) - 3), True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    # Update the screen
    pygame.display.update()

    # Add a delay to slow down the game
    pygame.time.delay(200)
