import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Ranger")

BG = pygame.transform.scale(pygame.image.load("space-bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 70

PLAYER_VEL = 5
STAR_VEL = 3

BULLET_VEL = 7 

FONT = pygame.font.SysFont("comicsans", 30)

SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load("spaceship.jpg"), (PLAYER_WIDTH, PLAYER_HEIGHT))


class Star:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Game:
    def __init__(self):
        self.player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.player_img = SPACESHIP_IMAGE
        self.clock = pygame.time.Clock()

        self.start_time = time.time()
        self.elapsed_time = 0

        self.star_add_increment = 2000
        self.star_count = 0

        self.stars = []
        self.hit = False

        self.star_width = 10
        self.star_height = 20

    def draw(self):
        WIN.blit(BG, (0, 0))
        time_text = FONT.render(f'Time: {round(self.elapsed_time)}s', 1, 'red')
        WIN.blit(time_text, (10, 10))
        WIN.blit(self.player_img, (self.player.x, self.player.y))
        for star in self.stars:
            pygame.draw.rect(WIN, star.color, star.rect)
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update_player_position(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player.x - PLAYER_VEL >= 0: #left
            self.player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and self.player.x + PLAYER_VEL + self.player.width <= WIDTH: #right
            self.player.x += PLAYER_VEL
        if keys[pygame.K_UP] and self.player.y - PLAYER_VEL >= 0: #up
            self.player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and self.player.y + PLAYER_VEL + self.player.height <= HEIGHT: #down
            self.player.y += PLAYER_VEL

    def update_stars(self):
        self.star_count += self.clock.tick(80)
        self.elapsed_time = time.time() - self.start_time
        if self.star_count > self.star_add_increment:
            for _ in range(4):
                star_x = random.randint(0, WIDTH - self.star_width)
                star = Star(star_x, -self.star_height, self.star_width, self.star_height)
                self.stars.append(star)
            self.star_add_increment = max(200, self.star_add_increment - 50)
            self.star_count = 0

    def check_collisions(self):
        for star in self.stars[:]:
            star.rect.y += STAR_VEL
            if star.rect.y > HEIGHT:
                self.stars.remove(star)
            elif star.rect.y + star.rect.height >= self.player.y and star.rect.colliderect(self.player):
                self.stars.remove(star)
                self.hit = True
                break

    def run(self):
        run = True
        while run:
            run = self.handle_events()
            self.update_player_position()
            self.update_stars()
            self.check_collisions()
            if self.hit:
                lost_text = FONT.render('You Lost!', 1, 'blue')
                last_text = FONT.render(f'Time: {round(self.elapsed_time)}s', 1, 'red')
                WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
                WIN.blit(last_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2 + 30))
                pygame.display.update()
                pygame.time.delay(4000)
                break
            self.draw()
            self.clock.tick(200)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
