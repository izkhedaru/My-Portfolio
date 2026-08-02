import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Basics")
clock = pygame.time.Clock()

# Constants
MOVE_SPEED = 5
JUMP_STRENGTH = 14
GROUND_Y_LEVEL = 250
SNAIL_SPEED = 4

# Game State
game_active = True
game_won = False
score = 0
player_gravity = 0

try:
    test_font = pygame.font.Font("font/LuckiestGuy-Regular.ttf", 50)
except pygame.error:
    test_font = pygame.font.Font(None, 50)
    
sky_surface = pygame.image.load("player/Sky.png").convert_alpha()
ground_surface = pygame.image.load("player/ground.png").convert_alpha()

snail_surf = pygame.image.load("snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(bottomright=(600, GROUND_Y_LEVEL))

player_surf = pygame.image.load("player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, GROUND_Y_LEVEL))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
                game_won = False
                snail_rect.left = 800
                player_rect.midbottom = (80, GROUND_Y_LEVEL)
                player_gravity = 0
                score = 0

        if game_active:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_w) and player_rect.bottom >= GROUND_Y_LEVEL:
                    player_gravity = -JUMP_STRENGTH
                    score += 1
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if player_rect.bottom >= GROUND_Y_LEVEL:
                    player_gravity = -JUMP_STRENGTH
                    score += 1

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, GROUND_Y_LEVEL))

        # Check win condition
        if score >= 10:
            game_active = False
            game_won = True

        # Score UI
        score_surf = test_font.render(f"Score: {score}", True, "#11abec")
        score_rect = score_surf.get_rect(center=(400, 60))
        pygame.draw.rect(screen, "Cyan", score_rect.inflate(20, 10))
        screen.blit(score_surf, score_rect)

        # Snail
        snail_rect.x -= SNAIL_SPEED
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)

        # Player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: player_rect.x -= MOVE_SPEED
        elif keys[pygame.K_d]: player_rect.x += MOVE_SPEED

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= GROUND_Y_LEVEL:
            player_rect.bottom = GROUND_Y_LEVEL
            player_gravity = 0
        screen.blit(player_surf, player_rect)

        # Collision
        if snail_rect.colliderect(player_rect):
            game_active = False

    else:
        screen.fill("Cyan")
        msg = "You Win!" if game_won else "Game Over"
        status_surf = test_font.render(msg, False, (100, 100, 100))
        status_rect = status_surf.get_rect(center=(400, 150))
        restart_surf = test_font.render("Press Enter/Return to Restart", False, (100, 100, 100))
        restart_rect = restart_surf.get_rect(center=(400, 300))
        
        screen.blit(status_surf, status_rect)
        screen.blit(restart_surf, restart_rect)

    pygame.display.update()
    clock.tick(60)