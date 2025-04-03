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
BULLET_SPEED = 10
TILE_SIZE = 50

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Outlaw's Reckoning")

# Load Assets
cowboy_img = pygame.image.load("assets/cowboy.png")  # Replace with actual image file
cowboy_img = pygame.transform.scale(cowboy_img, (50, 50))
partner_img = pygame.image.load("assets/partner.png")  # Replace with actual image file
partner_img = pygame.transform.scale(partner_img, (50, 50))

# Maze Layout (1 = Wall, 0 = Path)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        self.rect.x += BULLET_SPEED
        if self.rect.x > WIDTH:
            self.kill()

# Cowboy Class
class Cowboy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cowboy_img
        self.rect = self.image.get_rect(midbottom=(50, HEIGHT - 100))
        self.speed = PLAYER_SPEED
        self.bullets = pygame.sprite.Group()
    
    def move(self, keys):
        new_x, new_y = self.rect.x, self.rect.y
        if keys[pygame.K_LEFT]:
            new_x -= self.speed
        if keys[pygame.K_RIGHT]:
            new_x += self.speed
        if keys[pygame.K_UP]:
            new_y -= self.speed
        if keys[pygame.K_DOWN]:
            new_y += self.speed
        
        # Collision detection with maze
        if not self.collides_with_walls(new_x, new_y):
            self.rect.x, self.rect.y = new_x, new_y
    
    def collides_with_walls(self, x, y):
        for row_idx, row in enumerate(maze):
            for col_idx, tile in enumerate(row):
                if tile == 1:
                    wall_rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if wall_rect.colliderect(pygame.Rect(x, y, 50, 50)):
                        return True
        return False
    
    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery)
        self.bullets.add(bullet)
    
    def update(self, keys):
        self.move(keys)
        self.bullets.update()

# Draw Maze Function
def draw_maze():
    for row_idx, row in enumerate(maze):
        for col_idx, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, BLACK, (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Game Loop
clock = pygame.time.Clock()
cowboy = Cowboy()
all_sprites = pygame.sprite.Group(cowboy)
partner_rect = partner_img.get_rect(midbottom=(WIDTH - 100, HEIGHT - 100))

running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)
    draw_maze()
    
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            cowboy.shoot()
    
    cowboy.update(keys)
    all_sprites.draw(screen)
    cowboy.bullets.draw(screen)
    screen.blit(partner_img, partner_rect)
    
    # Check if Cowboy reaches partner
    if cowboy.rect.colliderect(partner_rect):
        print("You saved your partner!")
        running = False
    
    pygame.display.flip()

pygame.quit()
