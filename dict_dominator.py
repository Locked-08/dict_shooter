import pygame
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
FPS = 60
BACKGROUND_COLOR = (0, 55, 0)
SPACESHIP_WIDTH= 50
SPACESHIP_HEIGHT = 50


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self,vel):
        self.y += vel
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)
class Ship:
    COOLDOWN = 5
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WINDOW_HEIGHT):
                self.lasers.remove(laser)
    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1
    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x + 22, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1
class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_img = pygame.transform.scale(pygame.image.load('ass_sets/spaceship.png'),
                                               (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
        self.mask_img = pygame.mask.from_surface(self.ship_img)
        self.laser_img = pygame.transform.scale(pygame.image.load('ass_sets/bullet.png'), (30, 45))
        self.mask = pygame.mask.from_surface(self.ship_img)

    def draw(self, window):
        super().draw(window)

def init_game():
    print("game")
    clock = pygame.time.Clock()
    player = Player(50, 50)
    player_vel = 5
    laser_vel = 2
    enemies = []
    run = True
    while run:
        clock.tick(FPS)
        background = pygame.transform.scale(pygame.image.load('ass_sets/background_image.jpeg'),
                                            (WINDOW_WIDTH, WINDOW_HEIGHT))
        WINDOW.blit(background, (0,0))
        player.draw(WINDOW)
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < WINDOW_HEIGHT:
            player.y += player_vel
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() +15  < WINDOW_WIDTH:
            player.x += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        player.move_lasers(-laser_vel, enemies)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

def render_window():
    pygame.init()
    pygame.display.set_caption("Game Design Tutorial 2")
    clock = pygame.time.Clock()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        WINDOW.fill(BACKGROUND_COLOR)
        surface = pygame.display.get_surface()
        main_menu_title_pos=(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 100)
        main_menu_begin_pos = (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 20)
        main_menu_font = pygame.font.SysFont('Arial', 35)
        main_menu_title = main_menu_font.render("Game design Tutorial 2", 1, "white")
        main_menu_begin = main_menu_font.render("Click anywhere to begin", 1, "white")
        surface.blit(main_menu_title, main_menu_title_pos)
        surface.blit(main_menu_begin, main_menu_begin_pos)
        pygame.display.update()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                init_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                init_game()                       
def main():
    render_window()
    
if __name__ == "__main__":
    main()
    