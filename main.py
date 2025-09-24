import pygame
from random import randint, choice
from typing import TypeAlias
import cairosvg
import io

''' 
globals
'''

# convention for two_tuple :
# index 0 - x axis, index 1 - y axis
# throughout
two_tuple : TypeAlias = tuple[int, int]

LOGO_MOVEMENT_SPEED : int = 5
RATIO_LOGO_TO_SCREEN : float = 0.08
FPS : int = 30
COLORS : list[str] = [ 
    "maroon",
    "yellow",
    "aquamarine",
    "gray",
    "deepskyblue",
    "red",
    "hotpink",
    "lightgreen",
    "purple",
    "white",
    "orange",
]

IMAGE_PATH : str = "./dvd-logo.svg"
SCREEN : pygame.display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
SCREEN_DIM : two_tuple = SCREEN.get_size()
ORIG_IMAGE_DIM : two_tuple = pygame.image.load(IMAGE_PATH).get_size()
IMAGE_SCALING : float = RATIO_LOGO_TO_SCREEN * SCREEN_DIM[0] * SCREEN_DIM[1] / \
                        (ORIG_IMAGE_DIM[0] * ORIG_IMAGE_DIM[1])
SCALED_IMAGE_DIM : two_tuple = tuple(IMAGE_SCALING * elt for elt in ORIG_IMAGE_DIM)
IMAGE_BOUNDS : tuple[two_tuple, two_tuple] = (
                (SCALED_IMAGE_DIM[0] // 2, SCREEN_DIM[0] - SCALED_IMAGE_DIM[0] // 2), 
                (SCALED_IMAGE_DIM[1] // 2, SCREEN_DIM[1] - SCALED_IMAGE_DIM[1] // 2), 
                )   
EXCLUDE_FROM_SPAWN_PERCENTAGE : float = 0.1

'''
Logo:
class contining logo info (position, current color, etc.)
'''

class Logo:
    # init()
    def __init__(self):
        self.color_index : int = self.initialize_color_index()
        self.x_direction: int = self.initialize_direction()
        self.y_direction: int = self.initialize_direction()
        self.surface = self.load_svg_as_surface()
        self.rect = self.surface.get_rect()
        self.initialize_pos()

    # return random choice between -1 and 1
    def initialize_direction(self) -> int:
        return choice([-1,1])

    # increment index in COLORS list
    def update_color_index(self) -> None:
        self.color_index = (self.color_index + 1) % len(COLORS)

    # set (x,y) position of self.rect to random position within image bounds
    def initialize_pos(self) -> None:
        x_range : int = IMAGE_BOUNDS[0][1] - IMAGE_BOUNDS[0][0]
        y_range : int = IMAGE_BOUNDS[1][1] - IMAGE_BOUNDS[1][0]

        x_low : int = int(IMAGE_BOUNDS[0][0] + EXCLUDE_FROM_SPAWN_PERCENTAGE * x_range)
        x_high : int = int(IMAGE_BOUNDS[0][1] - EXCLUDE_FROM_SPAWN_PERCENTAGE * x_range)
        y_low : int = int(IMAGE_BOUNDS[0][0] + EXCLUDE_FROM_SPAWN_PERCENTAGE * y_range)
        y_high : int = int(IMAGE_BOUNDS[1][1] - EXCLUDE_FROM_SPAWN_PERCENTAGE * y_range)

        self.rect.centerx = randint(x_low, x_high)
        self.rect.centery = randint(y_low, y_high)

    # return random index between 0 and the length of the specified COLORS list
    def initialize_color_index(self) -> int:
        return randint(0, len(COLORS) - 1)

    # update x position - return true if new position would go out of bounds for x-axis
    # else false
    def update_x_pos(self) -> bool:
        retval : bool = False
        new_pos : int = self.rect.centerx + self.x_direction * LOGO_MOVEMENT_SPEED
        if new_pos >= IMAGE_BOUNDS[0][0] and new_pos <= IMAGE_BOUNDS[0][1]:
            self.rect.centerx = new_pos
        else: 
            self.x_direction *= -1
            retval = True
        return retval

    # update y position - return true if new position would go out of bounds for y-axis
    # else false
    def update_y_pos(self) -> bool:
        retval : bool = False
        new_pos : int = self.rect.centery + self.y_direction * LOGO_MOVEMENT_SPEED
        if new_pos >= IMAGE_BOUNDS[1][0] and new_pos <= IMAGE_BOUNDS[1][1]:
            self.rect.centery = new_pos
        else: 
            self.y_direction *= -1
            retval = True
        return retval

    # call update_x_pos(), update_y_pos(). if either hits an edge call reload_suface()
    def update_pos(self) -> None:
        x_hits_edge : bool = self.update_x_pos()
        y_hits_edge : bool = self.update_y_pos()
        if x_hits_edge or y_hits_edge:
            self.reload_surface()

    # reload class's surface after edge / corner hit
    def reload_surface(self) -> None:
        self.update_color_index()
        new_surface = self.load_svg_as_surface()  
        new_rect = new_surface.get_rect()
        new_rect.centerx = self.rect.centerx
        new_rect.centery = self.rect.centery
        self.surface = new_surface
        self.rect = new_rect

    # function to load and convert SVG to Pygame surface, filling svg with current color
    def load_svg_as_surface(self):
        with open (IMAGE_PATH, "r") as file:
            svg_data = file.read()
        svg_data = svg_data.replace('fill="white"', f'fill="{COLORS[self.color_index]}"') 
        png_bytes = cairosvg.svg2png(bytestring=svg_data.encode("utf-8"), scale=IMAGE_SCALING)
        image_io = io.BytesIO(png_bytes)
        return pygame.image.load(image_io).convert_alpha()
    
# main()
def main():
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    logo = Logo()
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            # press any key to quit
            if event.type == pygame.KEYDOWN \
                    or event.type == pygame.QUIT:
                running = False
        SCREEN.fill("black") # black background
        SCREEN.blit(logo.surface, logo.rect)
        logo.update_pos()
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()
