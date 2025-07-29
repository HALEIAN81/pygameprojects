import pygame
import sys
import random # Import the random module for power-up positioning

# 1. Initialize Pygame
pygame.init()

# 2. Set up Screen Dimensions and Caption
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Sci-Fi Gator with Power-ups") # Updated caption for clarity

# 3. Define Colors (RGB Tuples)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255) # Added for text feedback

# 4. Character Properties (using an image)
image_filename = "scifigator.png" # The name of your local character image file

# Desired character dimensions
CHARACTER_WIDTH = 75
CHARACTER_HEIGHT = 75

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

# Get the rectangle of the (scaled) character image for positioning
character_rect = character_image.get_rect()
character_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) # Start in the center

character_speed = 7 # Increased speed for more noticeable movement

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

# --- NEW: Power-up Item Properties ---
powerup_image_filename = "powerup.png" # Name of your power-up image file
POWERUP_WIDTH = 50
POWERUP_HEIGHT = 50

try:
    original_powerup_image = pygame.image.load(powerup_image_filename).convert_alpha()
    powerup_image = pygame.transform.scale(original_powerup_image, (POWERUP_WIDTH, POWERUP_HEIGHT))
except pygame.error as e:
    print(f"Error loading power-up image '{powerup_image_filename}': {e}. Using a default green square.")
    # Fallback: Create a green square if power-up image loading fails
    powerup_image = pygame.Surface((POWERUP_WIDTH, POWERUP_HEIGHT))
    powerup_image.fill((0, 255, 0)) # Green color for power-up
    powerup_image.set_colorkey((0,0,0)) # Make black transparent if using fill

# Function to get a random position for the power-up within screen bounds
def get_random_powerup_position():
    # Ensure the power-up is fully visible within the screen
    x = random.randint(0, SCREEN_WIDTH - POWERUP_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT - POWERUP_HEIGHT)
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
    if keys[pygame.K_LEFT]:
        character_rect.x -= character_speed
    if keys[pygame.K_RIGHT]:
        character_rect.x += character_speed
    if keys[pygame.K_UP]:
        character_rect.y -= character_speed
    if keys[pygame.K_DOWN]:
        character_rect.y += character_speed

    # Keep character within screen bounds
    character_rect.x = max(0, min(character_rect.x, SCREEN_WIDTH - character_rect.width))
    character_rect.y = max(0, min(character_rect.y, SCREEN_HEIGHT - character_rect.height))

    # --- NEW: Collision Detection for Power-up ---
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

    # Drawing order is important: background first, then character, then power-up
    screen.blit(background_image, (0, 0)) # Draw the background image at (0,0)
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