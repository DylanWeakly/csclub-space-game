import pygame
import random
from mazeSetup import mazes

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
TILE_SIZE = 50

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Outlaw's Reckoning - Help the Cowboy save his horse!")

# Load Assets
cowboy_img = pygame.image.load("assets/cowboy.png")  # Replace with actual image file
cowboy_img = pygame.transform.scale(cowboy_img, (50, 50))
partner_img = pygame.image.load("assets/horse.png")  # Replace with actual image file
partner_img = pygame.transform.scale(partner_img, (75, 75))

# Load the background image
background_img = pygame.image.load("assets/mojave.png")  # Replace with actual background image file
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Scale it to fit the screen

level = 5
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
                pygame.draw.rect(screen, "black", (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Game Loop
clock = pygame.time.Clock()
cowboy = Cowboy()
all_sprites = pygame.sprite.Group(cowboy)
partner_rect = partner_img.get_rect(midbottom=(WIDTH - TILE_SIZE * 2, HEIGHT - TILE_SIZE * 2))

# Define fonts for the level label and congratulations message
font = pygame.font.Font(None, 50)
congrats_font = pygame.font.Font(None, 100)

running = True
while running:
    clock.tick(60)
    screen.fill("white")  # Clear the screen
    screen.blit(background_img, (0, 0))  # Draw the background image
    
    # Render level text at the top-center with a more visible color (e.g., bright yellow)
    level_text = font.render(f"Level {level + 1} of 6", True, (255, 255, 0))  # Bright yellow color
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 10))  # Position it at the top-center
    
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
            # Displaying the congratulations message
            congrats_text = congrats_font.render("Congratulations, you beat the game!", True, (0, 255, 0))  # Green color
            screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, HEIGHT // 2 - congrats_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds before closing
            running = False
        else:
            maze = mazes[level]
            start_x, start_y = get_start_position()
            cowboy.rect.topleft = (start_x, start_y)
    
    pygame.display.flip()

pygame.quit()
