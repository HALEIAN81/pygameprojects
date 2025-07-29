import pygame
import sys

# 1. Initialize Pygame
pygame.init()

# 2. Set up Screen Dimensions and Caption
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Sci-Fi Gator") # Updated caption

# 3. Define Colors (RGB Tuples) - Still useful for background
BLACK = (0, 0, 0)

# 4. Character Properties (using an image)
image_filename = "scifigator.png" # The name of your local image file

# Desired character dimensions
CHARACTER_WIDTH = 100  # Set your desired width
CHARACTER_HEIGHT = 100 # Set your desired height

try:
    original_image = pygame.image.load(image_filename).convert_alpha()
    # Scale the image to the desired dimensions
    character_image = pygame.transform.scale(original_image, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
except pygame.error as e: # Catch specific Pygame error for image loading
    print(f"Error loading image '{image_filename}': {e}. Ensure the image is in the same folder as main.py.")
    # Fallback: Create a surface and draw a red square if image loading fails
    character_image = pygame.Surface((CHARACTER_WIDTH, CHARACTER_HEIGHT)) # Use desired size for fallback
    character_image.fill((255, 0, 0)) # Red color
    character_image.set_colorkey((0,0,0)) # Make black transparent if using fill

# Get the rectangle of the (scaled) image for positioning
character_rect = character_image.get_rect()
character_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) # Start in the center

character_speed = 7 # Increased speed for more noticeable movement

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# 5. Game Loop
running = True
while running:
    # Event handling: Check for QUIT event and other single-press events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Debugging: Uncomment these lines to see if key presses are registered
        if event.type == pygame.KEYDOWN:
            print(f"Key pressed: {pygame.key.name(event.key)}")


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

    # Debugging: Uncomment these lines to see if character_rect position changes
    # print(f"Character position: x={character_rect.x}, y={character_rect.y}")


    # Keep character within screen bounds
    character_rect.x = max(0, min(character_rect.x, SCREEN_WIDTH - character_rect.width))
    character_rect.y = max(0, min(character_rect.y, SCREEN_HEIGHT - character_rect.height))

    # Drawing
    screen.fill(BLACK)  # Clear the screen with black
    screen.blit(character_image, character_rect) # Draw the character image

    # Update display
    pygame.display.flip() # Or pygame.display.update()

    # Control frame rate
    clock.tick(60) # Limits the game to 60 frames per second

# 6. Quit Pygame
pygame.quit()
sys.exit()
