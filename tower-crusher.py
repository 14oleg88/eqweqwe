#Створи власний Шутер!

from pygame import *
import random
import pygame_menu
import pygame_menu.themes

init()
font.init()
mixer.init()
mixer.music.load("Voicy_CLASH ROYALE BATTLE MUSIC.mp3")
mixer.music.set_volume(0.1)
mixer.music.play(loops=-1)

fire_sound = mixer.Sound('mini-pekka-hit.mp3')
fire_sound.set_volume(0.4)
FONT = 'PressStart2P-Regular.ttf'




#створи вікно гри
FPS = 60
scr_info = display.Info()
WIDTH, HEIGHT = scr_info.current_w, scr_info.current_h
window = display.set_mode((WIDTH, HEIGHT), flags=FULLSCREEN)
display.set_caption("Catch up")

clock = time.Clock()

bg = image.load('map.png')
bg = transform.scale(bg, (WIDTH, HEIGHT))
player_img = image.load('Mini_PEKKA_2.webp')
enemy_img = image.load("Goblin_Cage_1.webp")
fire_img = image.load("ddwzo4p-0108faf6-2508-479e-b29c-1bdc4f199d29.png")
fire_sound = mixer.Sound('mini-pekka-hit.mp3')
fire_sound.set_volume(0.5)

all_sprites = sprite.Group()
all_labels = sprite.Group()

class Label(sprite.Sprite):
    def __init__(self, text, x,y, fontSize = 40, fontname=FONT, color =(255,255,255)):
        super().__init__()
        self.color = color
        self.font = font.Font(fontname, fontSize)
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_labels.add(self)

    def set_text(self, new_text, color =(255,255,255)):
        self.image = self.font.render(new_text, True, color)


class BaseSprite(sprite.Sprite):
    def __init__(self, image, x,y,width, height):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x,y,width, height)
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)
    def draw(self,window):
        window.blit(self.image, self.rect)

class Player(BaseSprite):
    def __init__(self, image,x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image, True, False)
        self.speed_x = 10
        self.speed_y = 0
        self.max_speed = 20
        self.hp = 100
        self.score = 0
        self.coins_counter= 0
        self.damage_timer = time.get_ticks()
        self.rect.centerx = x
        self.bullets = sprite.Group()
        self.fire_timer = time.get_ticks()

    def fire(self):
        bullet = Bullet(self.rect, fire_img, 3, 205)
        self.bullets.add(bullet)
        fire_sound.play()


    def update(self):
        old_pos = self.rect.x, self.rect.y
        keys = key.get_pressed()
        if keys[K_SPACE]:
            now = time.get_ticks()
            if now-self.fire_timer > 400:
                self.fire()
                self.fire_timer = now
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed_x
            self.image = self.left_image
        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed_x
            self.image = self.right_image
        if keys[K_w] and self.rect.top > 0:
            if self.speed_y < self.max_speed:
                self.speed_y += 0.1
            if self.rect.y > HEIGHT/2:
                self.rect.y -= self.speed_x
            self.rect.y -= self.speed_x
        if keys[K_s] and self.rect.bottom < HEIGHT and self.speed_y>0:
            self.speed_y -= 0.05
            if self.rect.bottom < HEIGHT:
                self.rect.y += self.speed_x


        if not keys[K_w] and self.speed_y > 2:
                self.speed_y -= 0.1

        coll_list = sprite.spritecollide(self, enemy_group , False, sprite.collide_mask)
        if len(coll_list)>0:
            now = time.get_ticks()
            if now-self.damage_timer > 500:
                self.damage_timer = time.get_ticks() #обнуляємо таймер дамагу
                self.hp -= 10 #віднімаємо HP
                hp_label.set_text(f"hp: {self.hp}")


class Enemy(BaseSprite):
    def __init__(self, image, width, height):
        x = random.randint(0, WIDTH-width)
        y = random.randint(400, HEIGHT) * -1
        super().__init__(image, x, y, width, height)
        self.speed_x = 10
        self.speed_y = 2
        self.max_speed = 20
        self.hp = 100
        self.rect.centerx = x

    def update(self):
        self.rect.y += self.speed_y + player.speed_y
        if self.rect.y > HEIGHT:
            self.kill()

class Bullet(BaseSprite):
    def __init__(self, player_rect, image, width, height):
        super().__init__(image, player_rect.x, player_rect.y, width, height)
        self.speed_y = 290
        self.rect.bottom = player_rect.top
        self.rect.centerx = player_rect.centerx

    def update(self):
        self.rect.y -= self.speed_y
        if self.rect.y < 0:
            self.kill()




player = Player(player_img, WIDTH/2, HEIGHT-200, 110, 100)
finish = False



run = True
bg1_y = 0
bg2_y = -HEIGHT
enemy_group = sprite.Group()
spawn_timer = time.get_ticks()
max_spawn_time = 2000

result = Label("", 300, 300, fontSize=70)
restart = Label("Press R to restart", 300, 450, fontSize=40)
all_labels.remove(restart)
hp_label = Label(f"HP: {player.hp}", 10, 10)
score_label = Label(f"Score: {player.score}", 10, 30)

def start_the_game():
    if finish:
        player.hp = 100
        player.score = 0

    menu.disable()

def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    menu.disable()

myimage = pygame_menu.baseimage.BaseImage(
    image_path="background.jpg",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,

)

def start_the_game():
    menu.disable()

def restart_game():
    global finish
    if finish:
        player.hp = 100
        player.score = 0
        hp_label = Label(f"HP: {player.hp}", 10, 10)
        score_label = Label(f"Score: {player.score}", 10, 30)
        finish = False
        for enemy in enemy_group:
            enemy.kill()
        player.rect.x = WIDTH/2
        player.rect.y = HEIGHT-200
        finish_menu.disable()

mytheme = pygame_menu.Theme(background_color=(0, 0, 0, 0), # transparent background
                title_background_color=(4, 47, 126),
                title_font_shadow=True,
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
                widget_padding=25,
                widget_font=pygame_menu.font.FONT_8BIT
                )

mytheme.background_color = myimage

menu = pygame_menu.Menu('Welcome', WIDTH, HEIGHT,
                       theme=mytheme)

menu.add.button('Play', start_the_game)
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Quit', pygame_menu.events.EXIT)

finish_menu = pygame_menu.Menu('Welcome', WIDTH, HEIGHT,
                       theme=mytheme)

finish_menu.add.button('Restart', restart_game)
finish_menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
finish_menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(window)



while run:
    for e in event.get():
        if e.type == QUIT:
            run=False
        if e.type ==KEYDOWN:
            if e.key == K_ESCAPE:
                run=False

    if not finish:
        all_sprites.update()
        now = time.get_ticks()
        if now - spawn_timer > random.randint(400, max_spawn_time):
            spawn_timer = now
            enemy_count = random.randint(1,3)
            for i in range(enemy_count):
                enemy_group.add(Enemy(enemy_img, 120, 80))

        if player.hp<=0:
            finish = True
            finish_menu.enable()
            finish_menu.mainloop(window)

        collide_list = sprite.groupcollide(enemy_group, player.bullets, True, True)
        for enemy in collide_list:
            player.score+=10
            score_label.set_text(f"Score: {player.score}")

        bg1_y += player.speed_y
        bg2_y += player.speed_y
        if bg1_y > HEIGHT:
            bg1_y = -HEIGHT
        if bg2_y > HEIGHT:
            bg2_y = -HEIGHT
    window.blit(bg, ((0,bg1_y)))
    window.blit(bg, ((0,bg2_y)))
    all_sprites.draw(window)
    all_labels.draw(window)

    display.update()
    clock.tick(FPS)
