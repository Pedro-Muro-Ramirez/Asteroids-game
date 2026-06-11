import asyncio
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def new_game():
    """Create fresh sprite groups and starting objects for a new round."""
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, drawable, updatable)

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    AsteroidField()

    return updatable, drawable, asteroids, shots, player

async def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 96)
    hint_font = pygame.font.Font(None, 40)

    updatable, drawable, asteroids, shots, player = new_game()
    dt = 0.0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                updatable, drawable, asteroids, shots, player = new_game()
                game_over = False

        screen.fill("black")

        if not game_over:
            log_state()
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    game_over = True
                    break

            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        asteroid.split()
                        shot.kill()

        for draw in drawable:
            draw.draw(screen)

        if game_over:
            title = title_font.render("GAME OVER", True, "white")
            hint = hint_font.render("Press R to restart", True, "white")
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30)))
            screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40)))

        pygame.display.flip()
        dt = clock.tick(60) / 1000
        await asyncio.sleep(0)  # yield to the browser event loop (required by pygbag)

if __name__ == "__main__":
    asyncio.run(main())
