import pygame
import sys

'''
create an instance of pygame
'''
pygame.init()

'''
create window size for image viewer
'''
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Image Viewer")

'''
method that handles screen resizing
'''
def resize_display(width, height):
    global screen, screen_width, screen_height
    screen_width = width
    screen_height = height
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Image Viewer")

'''
method to convert image to monochromatic scale
'''
def monochrome(image):
    '''
    create a new pygame surface using the image dimensions 
    and modify the pixel value to become monochromatic
    '''
    monochrome_image = pygame.Surface(image.get_size()).convert_alpha()
    
    '''
    check each pixel and calculate its new luminance value
    '''
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            r, g, b, _ = image.get_at((x, y))
            '''
            formula for luminance
            '''
            luminance = int(0.3 * r + 0.59 * g + 0.11 * b)
            '''
            apply luminance value to pixels in the new image
            '''
            monochrome_image.set_at((x, y), (luminance, luminance, luminance))
    
    return monochrome_image

'''
method to allow user to pick color
'''
def pick_color(image, pos):
    '''
    get color where the user clicked 
    '''
    color = image.get_at(pos)
    return color

'''
method to boost selected color 
'''
def boost_image(image, last_color):
    '''
    make a copy of the image so we can modify
    it without harming the original
    '''
    modified_image = image.copy()
    '''
    check pixel color at each position
    '''
    for x in range(modified_image.get_width()):
        for y in range(modified_image.get_height()):
            r, g, b, a = modified_image.get_at((x, y))
            '''
            if the pixel color is the same or darker 
            than the last color picked by the user 
            set it to black
            '''
            if r <= last_color[0] and g <= last_color[1] and b <= last_color[2]:
                modified_image.set_at((x, y), (0, 0, 0, 255))
    return modified_image

'''
method to extract lineart from monochromatic version of image
'''
def save_black_pixels(image):
    '''
    create a new transparent image of the same size as the original
    '''
    transparent_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    
    '''
    check the rgb value of each pixel in the monochromatic image,
    if value is pure black (or 0, 0, 0) then copy that pixel's location
    to the transparent image
    '''
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            r, g, b, _ = image.get_at((x, y))
            if r == 0 and g == 0 and b == 0:
                transparent_image.set_at((x, y), (0, 0, 0, 255))
    
    '''
    saves the new transparent image
    '''
    pygame.image.save(transparent_image, "Lineart.png")

'''
get image name from user input
'''
image_path = input("Enter the name of the image (ex: 'image.jpg'/'image.png'): ")

try:
    '''
    open orignal image
    '''
    original_image = pygame.image.load(image_path)

    '''
    check if the image was properly opened
    '''
    if original_image is None:
        raise ValueError("Unable to load image. Make sure the file name is correct.")
except pygame.error as e:
    print("Error loading image:", e)
    pygame.quit()
    sys.exit()
except Exception as e:
    print("An error occurred:", e)
    pygame.quit()
    sys.exit()

'''
convert original image to monochrome
'''
monochrome_image = monochrome(original_image)

'''
boost last picked color
'''
last_picked_color = (0, 0, 0)

'''
Main loop to update image
'''
while True:
    '''
    checking for button presses and resizing
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            '''
            call resize_display method if window width or height has changed
            '''
            resize_display(event.w, event.h)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            '''
            check to see if user has clicked on screen
            then save the color and print it in the terminal
            '''
            if event.button == 1:
                '''
                verify that mouse position is correct for window width and height 
                '''
                adjusted_pos = (event.pos[0] - (screen_width - monochrome_image.get_width()) // 2, 
                                event.pos[1] - (screen_height - monochrome_image.get_height()) // 2)
                color_picked = pick_color(monochrome_image, adjusted_pos)
                last_picked_color = color_picked
                print("Color picked:", color_picked)
        elif event.type == pygame.KEYDOWN:
            '''
            check to see if the 'b' key has been pressed and call the boost
            if the 'b' key wasn't pressed, check to see if the 's' key was pressed
            if the 's' key was pressed call the save function
            '''
            if event.key == pygame.K_b:
                monochrome_image = boost_image(monochrome_image, last_picked_color)
            elif event.key == pygame.K_s:
                save_black_pixels(monochrome_image)

    '''
    make the background of the image viewer white
    after the original image has been imported
    '''
    screen.fill((255, 255, 255))

    '''
    calculate center of image viewer window to center imported image
    '''
    image_x = (screen_width - monochrome_image.get_width()) // 2
    image_y = (screen_height - monochrome_image.get_height()) // 2

    '''
    display converted version of image
    '''
    screen.blit(monochrome_image, (image_x, image_y))

    '''
    update display after each loop
    '''
    pygame.display.update()
