import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rain Dodge")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
PLAYER_VEL = 5

STAR_WIDTH, STAR_HEIGHT = 10, 20
STAR_VEL = 7

FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, stars, elapsed_time):
    WIN.blit(BG, (0, 0))

    # Timer
    time_text = FONT.render(f"Time Survived: {int(elapsed_time)}s", 1, (255, 255, 255))
    WIN.blit(time_text, (10, 10))

    # Player
    pygame.draw.rect(WIN, (255, 0, 0), player)

    # Stars
    for star in stars:
        pygame.draw.rect(WIN, (255, 255, 0), star)

    pygame.display.update()


def main():
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()

    elapsed_time = 0
    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Add stars
        if star_count >= star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        # Quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        # Move stars + collision
        for star in stars[:]:
            star.y += STAR_VEL

            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                hit = True
                run = False
                break

        if hit:
            lost_text = FONT.render(f"You survived for {int(elapsed_time)} seconds!", 1, (255, 255, 255))
            WIN.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2 - lost_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, stars, elapsed_time)

    pygame.quit()


if __name__ == "__main__":
    main()
