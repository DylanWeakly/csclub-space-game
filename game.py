import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
PLAYER_SPEED = 5
TILE_SIZE = 50

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Outlaw's Reckoning")

# Load Assets
cowboy_img = pygame.image.load("assets/cowboy.png")  # Replace with actual image file
cowboy_img = pygame.transform.scale(cowboy_img, (50, 50))
partner_img = pygame.image.load("assets/partner.png")  # Replace with actual image file
partner_img = pygame.transform.scale(partner_img, (50, 50))

# List of Different Mazes for Multiple Levels
mazes = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    # Additional 9 different mazes can be added here as needed
]

level = 0
maze = mazes[level]

# Find starting position for Cowboy
def get_start_position():
    for row_idx, row in enumerate(maze):
        for col_idx, tile in enumerate(row):
            if tile == 0:
                return col_idx * TILE_SIZE, row_idx * TILE_SIZE
    return 0, 0

start_x, start_y = get_start_position()

# Cowboy Class
class Cowboy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cowboy_img
        self.rect = self.image.get_rect(topleft=(start_x, start_y))
        self.speed = PLAYER_SPEED
    
    def move(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed
        
        # Check if moving out of screen boundaries
        if self.rect.left + dx < 0:  # Prevent moving left out of screen
            dx = 0
        if self.rect.right + dx > WIDTH:  # Prevent moving right out of screen
            dx = 0
        if self.rect.top + dy < 0:  # Prevent moving up out of screen
            dy = 0
        if self.rect.bottom + dy > HEIGHT:  # Prevent moving down out of screen
            dy = 0
        
        new_rect = self.rect.move(dx, dy)
        if not self.collides_with_walls(new_rect):
            self.rect = new_rect
    
    def collides_with_walls(self, rect):
        for row_idx, row in enumerate(maze):
            for col_idx, tile in enumerate(row):
                if tile == 1:
                    wall_rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if rect.colliderect(wall_rect):
                        return True
        return False
    
    def update(self, keys):
        self.move(keys)

# Function to Draw Maze
def draw_maze():
    for row_idx, row in enumerate(maze):
        for col_idx, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, BLACK, (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Game Loop
clock = pygame.time.Clock()
cowboy = Cowboy()
all_sprites = pygame.sprite.Group(cowboy)
partner_rect = partner_img.get_rect(midbottom=(WIDTH - TILE_SIZE * 2, HEIGHT - TILE_SIZE * 2))

running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)
    
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_maze()
    cowboy.update(keys)
    all_sprites.draw(screen)
    screen.blit(partner_img, partner_rect)
    
    if cowboy.rect.colliderect(partner_rect):
        print(f"You completed level {level + 1}!")
        level += 1
        if level >= len(mazes):
            print("Game Completed!")
            running = False
        else:
            maze = mazes[level]
            start_x, start_y = get_start_position()
            cowboy.rect.topleft = (start_x, start_y)
    
    pygame.display.flip()

pygame.quit()
