import pygame
import sys

# Initialize pygame
pygame.init()

# Set up initial display size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Image Viewer")

# Function to resize the display
def resize_display(width, height):
    global screen, screen_width, screen_height
    screen_width = width
    screen_height = height
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Image Viewer")

# Function to convert image to monochrome
def monochrome(image):
    # Create a new surface with the same size and convert it to grayscale
    monochrome_image = pygame.Surface(image.get_size()).convert_alpha()
    
    # Iterate through each pixel and calculate the luminance value
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            r, g, b, _ = image.get_at((x, y))
            # Calculate luminance value using standard formula
            luminance = int(0.3 * r + 0.59 * g + 0.11 * b)
            # Set the pixel value in the monochrome image
            monochrome_image.set_at((x, y), (luminance, luminance, luminance))
    
    return monochrome_image

# Function to pick color from image
def pick_color(image, pos):
    # Get color at the clicked position
    color = image.get_at(pos)
    return color

# Function to adjust image based on last picked color
def boost_image(image, last_color):
    # Create a copy of the image to modify
    modified_image = image.copy()
    # Iterate through each pixel
    for x in range(modified_image.get_width()):
        for y in range(modified_image.get_height()):
            r, g, b, a = modified_image.get_at((x, y))
            # If the pixel color is the same or darker than the last color picked, set it to black
            if r <= last_color[0] and g <= last_color[1] and b <= last_color[2]:
                modified_image.set_at((x, y), (0, 0, 0, 255))
    return modified_image

# Function to save black pixels to a transparent image
def save_black_pixels(image):
    # Create a new surface with the same size and convert it to transparent
    transparent_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    
    # Iterate through each pixel and set black pixels to opaque
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            r, g, b, _ = image.get_at((x, y))
            if r == 0 and g == 0 and b == 0:
                transparent_image.set_at((x, y), (0, 0, 0, 255))
    
    # Save the transparent image
    pygame.image.save(transparent_image, "Lineart.png")

# Get image path from user input
image_path = input("Enter the path to the image (e.g., image.jpg): ")

try:
    # Load original image
    original_image = pygame.image.load(image_path)

    # Check if the image loaded successfully
    if original_image is None:
        raise ValueError("Unable to load image. Make sure the file path is correct.")
except pygame.error as e:
    print("Error loading image:", e)
    pygame.quit()
    sys.exit()
except Exception as e:
    print("An error occurred:", e)
    pygame.quit()
    sys.exit()

# Create monochrome image
monochrome_image = monochrome(original_image)

# Initialize last picked color to black
last_picked_color = (0, 0, 0)

# Main loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            # Resize the display if the window is resized
            resize_display(event.w, event.h)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If the left mouse button is clicked, pick the color from the image
            if event.button == 1:
                # Adjust the mouse position to account for the position of the image
                adjusted_pos = (event.pos[0] - (screen_width - monochrome_image.get_width()) // 2, 
                                event.pos[1] - (screen_height - monochrome_image.get_height()) // 2)
                color_picked = pick_color(monochrome_image, adjusted_pos)
                last_picked_color = color_picked
                print("Color picked:", color_picked)
        elif event.type == pygame.KEYDOWN:
            # If the user presses the 'b' key, update the image with boosted colors
            if event.key == pygame.K_b:
                monochrome_image = boost_image(monochrome_image, last_picked_color)
            # If the user presses the 's' key, save black pixels to a transparent image
            elif event.key == pygame.K_s:
                save_black_pixels(monochrome_image)

    # Fill screen with white background
    screen.fill((255, 255, 255))

    # Calculate the position to center the image
    image_x = (screen_width - monochrome_image.get_width()) // 2
    image_y = (screen_height - monochrome_image.get_height()) // 2

    # Display monochrome image
    screen.blit(monochrome_image, (image_x, image_y))

    # Update display
    pygame.display.update()
