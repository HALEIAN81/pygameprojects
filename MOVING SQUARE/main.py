import pygame
import sys
import random # Import the random module for power-up positioning

# 1. Initialize Pygame
pygame.init()

# 2. Set up Screen Dimensions and Caption
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Sci-Fi Gator with Maze and Power-ups") # Updated caption for clarity

# 3. Define Colors (RGB Tuples)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255) # Added for text feedback
WALL_COLOR = (100, 100, 100) # Color for maze walls (dark gray)

# --- Maze Definition ---
# 0 = path, 1 = wall
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

MAZE_HEIGHT = len(MAZE)
MAZE_WIDTH = len(MAZE[0])

# Calculate tile size to fit the maze within the screen
TILE_SIZE = min(SCREEN_WIDTH // MAZE_WIDTH, SCREEN_HEIGHT // MAZE_HEIGHT)

# Calculate offset to center the maze vertically if it doesn't fill the height
offset_y = (SCREEN_HEIGHT - MAZE_HEIGHT * TILE_SIZE) // 2

# List to store all wall rectangles for collision detection
wall_rects = []
# List to store valid path coordinates (row, col) for placing character/power-ups
path_tiles = []

for r_idx, row in enumerate(MAZE):
    for c_idx, tile in enumerate(row):
        x = c_idx * TILE_SIZE
        y = r_idx * TILE_SIZE + offset_y # Apply vertical offset
        if tile == 1: # It's a wall
            wall_rects.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
        else: # It's a path
            path_tiles.append((r_idx, c_idx))

# Function to draw the maze walls
def draw_maze():
    for wall_rect in wall_rects:
        pygame.draw.rect(screen, WALL_COLOR, wall_rect)

# 4. Character Properties (using an image)
image_filename = "scifigator.png" # The name of your local character image file

# NEW: Character dimensions relative to tile size, ensuring it fits within paths
CHARACTER_WIDTH = int(TILE_SIZE * 0.8)
CHARACTER_HEIGHT = int(TILE_SIZE * 0.8)

try:
    original_character_image = pygame.image.load(image_filename).convert_alpha()
    # Scale the image to the desired dimensions
    character_image = pygame.transform.scale(original_character_image, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
except pygame.error as e: # Catch specific Pygame error for image loading
    print(f"Error loading character image '{image_filename}': {e}. Ensure the image is in the same folder as main.py.")
    # Fallback: Create a surface and draw a red square if image loading fails
    character_image = pygame.Surface((CHARACTER_WIDTH, CHARACTER_HEIGHT)) # Use desired size for fallback
    character_image.fill((255, 0, 0)) # Red color
    character_image.set_colorkey((0,0,0)) # Make black transparent if using fill

character_speed = 7 # Increased speed for more noticeable movement

# Find a starting position for the character on a path tile
start_row, start_col = path_tiles[0] if path_tiles else (0,0) # Default to (0,0) if no path tiles

# Calculate initial character position based on maze grid, centered within the tile
initial_char_x = start_col * TILE_SIZE + (TILE_SIZE - CHARACTER_WIDTH) // 2
initial_char_y = start_row * TILE_SIZE + (TILE_SIZE - CHARACTER_HEIGHT) // 2 + offset_y

character_rect = character_image.get_rect(topleft=(initial_char_x, initial_char_y))


# 5. Background Properties (using an image)
background_image_filename = "mold_img.png" # Name of your background image file

try:
    original_background_image = pygame.image.load(background_image_filename).convert()
    # Scale the background image to fit the screen dimensions
    background_image = pygame.transform.scale(original_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Error loading background image '{background_image_filename}': {e}. Using a solid black background.")
    # Fallback: Create a solid black background if image loading fails
    background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image.fill(BLACK)


# --- Power-up Item Properties ---
powerup_image_filename = "powerup.png" # Name of your power-up image file
# Power-up dimensions relative to tile size, centered within the tile
POWERUP_WIDTH = int(TILE_SIZE * 0.6)
POWERUP_HEIGHT = int(TILE_SIZE * 0.6)

try:
    original_powerup_image = pygame.image.load(powerup_image_filename).convert_alpha()
    powerup_image = pygame.transform.scale(original_powerup_image, (POWERUP_WIDTH, POWERUP_HEIGHT))
except pygame.error as e:
    print(f"Error loading power-up image '{powerup_image_filename}': {e}. Using a default green square.")
    # Fallback: Create a green square if power-up image loading fails
    powerup_image = pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT))
    powerup_image.fill((0, 255, 0)) # Green color for power-up
    powerup_image.set_colorkey((0,0,0)) # Make black transparent if using fill

# Function to get a random position for the power-up within screen bounds on a path tile
def get_random_powerup_position():
    if not path_tiles:
        return pygame.Rect(0,0,0,0) # No valid path, return empty rect

    # Randomly select a path tile
    row, col = random.choice(path_tiles)

    # Convert grid coordinates to pixel coordinates, centered within the tile
    x = col * TILE_SIZE + (TILE_SIZE - POWERUP_WIDTH) // 2
    y = row * TILE_SIZE + (TILE_SIZE - POWERUP_HEIGHT) // 2 + offset_y # Apply vertical offset
    return pygame.Rect(x, y, POWERUP_WIDTH, POWERUP_HEIGHT)

# Initialize the power-up's position
powerup_rect = get_random_powerup_position()

# Font for collision feedback message
font = pygame.font.Font(None, 36) # Use default font, size 36
collision_message = "" # Stores the message to display
message_timer = 0 # Timer to control how long the message is displayed
MESSAGE_DURATION = 60 # Number of frames to display the message (e.g., 60 frames = 1 second at 60 FPS)

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# 6. Game Loop
running = True
while running:
    # Event handling: Check for QUIT event and other single-press events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get all currently pressed keys for continuous movement
    keys = pygame.key.get_pressed()

    # Store current position for collision checking (useful for reverting if both x and y movements are blocked)
    old_x, old_y = character_rect.x, character_rect.y

    # Calculate desired new position
    desired_x = character_rect.x
    desired_y = character_rect.y

    if keys[pygame.K_LEFT]:
        desired_x -= character_speed
    if keys[pygame.K_RIGHT]:
        desired_x += character_speed
    if keys[pygame.K_UP]:
        desired_y -= character_speed
    if keys[pygame.K_DOWN]:
        desired_y += character_speed

    # --- Collision Detection with Walls ---
    # Attempt horizontal movement
    character_rect.x = desired_x # Temporarily move character_rect to desired horizontal position
    for wall in wall_rects:
        if character_rect.colliderect(wall):
            character_rect.x = old_x # Revert x if collision detected
            break

    # Attempt vertical movement (using the potentially corrected x position)
    character_rect.y = desired_y # Temporarily move character_rect to desired vertical position
    for wall in wall_rects:
        if character_rect.colliderect(wall):
            character_rect.y = old_y # Revert y if collision detected
            break

    # Keep character within overall screen bounds (in case maze doesn't fill screen)
    character_rect.x = max(0, min(character_rect.x, SCREEN_WIDTH - character_rect.width))
    character_rect.y = max(0, min(character_rect.y, SCREEN_HEIGHT - character_rect.height))


    # --- Collision Detection for Power-up ---
    if character_rect.colliderect(powerup_rect):
        print("Power-up collected!") # Debug print to console
        collision_message = "Power-up Collected!" # Set the message
        message_timer = MESSAGE_DURATION # Start the message timer
        powerup_rect = get_random_powerup_position() # Move power-up to a new random location

    # Update message timer
    if message_timer > 0:
        message_timer -= 1 # Decrement timer each frame
    else:
        collision_message = "" # Clear message when timer runs out

    # Drawing order is important: background first, then maze, then character, then power-up
    screen.blit(background_image, (0, 0)) # Draw the background image at (0,0)
    draw_maze() # Draw the maze walls
    screen.blit(character_image, character_rect) # Draw the character image
    screen.blit(powerup_image, powerup_rect) # Draw the power-up image

    # Draw collision message if active
    if collision_message:
        text_surface = font.render(collision_message, True, WHITE) # Render text (text, antialias, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50)) # Position at top center
        screen.blit(text_surface, text_rect)

    # Update display
    pygame.display.flip() # Or pygame.display.update()

    # Control frame rate
    clock.tick(60) # Limits the game to 60 frames per second

# 7. Quit Pygame
pygame.quit()
sys.exit()
