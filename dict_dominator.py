import pygame
import random

pygame.font.init()
pygame.mixer.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
FPS = 60
BACKGROUND_COLOR = (0, 55, 0)
SPACESHIP_WIDTH= 50
SPACESHIP_HEIGHT = 50
RED_ENEMY = pygame.transform.scale(pygame.image.load('ass_sets/red_enemy.png'), (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))
RED_ENEMY2 = pygame.transform.scale(pygame.image.load('ass_sets/red_enemy2.png'), (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))
ENEMY_BULLET = pygame.transform.scale(pygame.image.load('ass_sets/enemy_bullet.png'), (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))
        


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
    def collision(self, obj):
        return collide(obj, self)
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None     
class Ship:
    COOLDOWN = 5
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0
        self.score = 0
        self.health = health
        
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
            elif laser.collision(obj):
                obj.health -= 10
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
class Enemy(Ship):
    COLOR_MAP = {"red": (RED_ENEMY, ENEMY_BULLET), "red2": (RED_ENEMY2, ENEMY_BULLET)}
    
    def __init__(self,x,y, color):
        super().__init__(x,y)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.vel = random.randint(3,6)
    def move(self):
            self.y += self.vel
            
        
class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = pygame.transform.scale(pygame.image.load('ass_sets/spaceship.png'),
                                               (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
        self.mask_img = pygame.mask.from_surface(self.ship_img)
        self.laser_img = pygame.transform.scale(pygame.image.load('ass_sets/bullet.png'), (30, 45))
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WINDOW_HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= 10
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        self.score += 100
    def healthbar(self,window):
        pygame.draw.rect(window, (255, 0, 0),
                        (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect (window, (0, 255, 0),(
            self.x, self.y + self.ship_img.get_height()+10, self.ship_img.get_width() * (self.health/self.max_health),10))

def init_game():
    print("game")
    clock = pygame.time.Clock()
    player = Player(50, 50)
    player_vel = 10
    laser_vel = 10
    lost = False
    level = 0
    enemies = []
    wave_length  = 5
    lives = 5
    lost_countdown = 0
    main_font = pygame.font.SysFont("arial", 50)
    run = True
    while run:
        clock.tick(FPS)
        background = pygame.transform.scale(pygame.image.load('ass_sets/background_image.jpeg'),
                                            (WINDOW_WIDTH, WINDOW_HEIGHT))
        WINDOW.blit(background, (0,0))
        live_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        score_label = main_font.render(f"Score :{player.score}", 1, (255,255,255))
        WINDOW.blit(live_label, (10, 10))
        WINDOW.blit(level_label, (WINDOW_WIDTH - level_label.get_width() - 10, 10))
        WINDOW.blit(score_label, (10, 70))
        pygame.draw.circle(WINDOW, (27,5,89), (player.x +25, player.y+25), 100)
        player.draw(WINDOW)
        if lost:
            lost_label = main_font.render(f"You lost! Score: {player.score}", 1, (255,255, 255))
            WINDOW.blit(lost_label, (WINDOW_WIDTH // 2 - lost_label.get_width()// 2, 350))
        if len(enemies) == 0:
            print(enemies)
            level += 1
            wave_length +=5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WINDOW_WIDTH - 100), random.randrange(-500, -100), random.choice(["red", "red2"]))
                enemies.append(enemy)
        for enemy in enemies:
            enemy.draw(WINDOW)

                
        pygame.display.update()
        # if lives <=0 or player.health <= 0:
        #     lost = True
        #     lost_countdown +=1 
        #     if lost:
        #         if lost_countdown > FPS * 3:
        #             run = False
        #         else:
        #             continue
        
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
        for enemy in enemies[:]:
            if random.randrange(0,4 * 60 - level) == 1:
                enemy.shoot()
            enemy.move()
            enemy.move_lasers(laser_vel, player)
            if collide(enemy, player):
                enemies.remove(enemy)
                player.health -=10
            elif enemy.y + enemy.get_height()> WINDOW_HEIGHT:
                lives -= 1
                enemies.remove(enemy)
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
    