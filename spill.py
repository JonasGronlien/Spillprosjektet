import pygame 
import random

pygame.init()

#1 oppsett
BREDDE = 800
HOYDE = int(BREDDE * 0.8) 

skjerm = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("skytespill")

#setter FPS
clock = pygame.time.Clock()
FPS = 60

#spill variabler
GRAVITY = 0.75
TILE_SIZE = 40 

#definerer spiller handlinger variabler 
moving_left = False 
moving_right = False
shoot = False

# laster bilder 
#kuler
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

#pickup boxes 
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
item_boxes = {
    'health'    : health_box_img,
    'ammo'      : ammo_box_img
}


#definerer farger  
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#font 
font = pygame.font.SysFont("Futura", 30)

def draw_text(text, font, text_col, x, y):
     img = font.render(text, True, text_col)
     skjerm.blit(img, (x, y))

def draw_bg():
    skjerm.fill(BG)
    pygame.draw.line(skjerm, RED, (0, 400), (BREDDE, 400))



class soldat(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        self.char_type = char_type 
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.ammo = ammo 
        self.start_ammo  = ammo 
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        img = pygame.image.load(f'img/{self.char_type}/idle/0.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width()* scale), int( img.get_height()* scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.scale = scale 
        #ai spesefike variabler 
        self.move_counter  = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False 
        self.idling_counter = 0

    
    def update(self):
        #opptaterer cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1   


    def move(self, moving_left, moving_right):
            #tilbakestiller bevegelse variabler
            dx = 0
            dy = 0

            #gir bevegelses variabler når spiller beveger høyre og venstre
            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                dx = +self.speed
                self.flip = False
                self.direction = 1
            
            #jump
            if self.jump == True and self.in_air == False:
                self.vel_y = -11
                self.jump = False
                self.in_air = True

            
            #gravitet
            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y

            # kollisjon med bakken 
            if self.rect.bottom + dy > 400  :
                dy = 400 - self.rect.bottom
                self.in_air = False


            #opptater rect posisjon 
            self.rect.x += dx
            self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = kule(self.rect.centerx + (0.75 * self.rect.size[0]* self.direction), self.rect.centery, self.direction)
            kule_group.add(bullet)
            #reduserer ammo
            self.ammo -= 1 
    
    def ai(self):
        if self.alive and spiller.alive:
            if not self.idling and random.randint(1, 200) == 1:
                self.idling = True
                self.idling_counter = 50
            #sjekker når ai er nærme spiler 
            if self.vision.colliderect(spiller.rect):
                 #slutt å løpe 
                 self.idling = True 
                 #skyt 
                 self.shoot()
            if not self.idling:
                ai_moving_right = self.direction == 1
                ai_moving_left = not ai_moving_right
                self.move(ai_moving_left, ai_moving_right)
                self.move_counter += 1
                #fiende ser spiller 
                self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                if self.move_counter > TILE_SIZE:
                    self.direction *= -1
                    self.move_counter = 0   
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False
                    self.idling_counter = 0

                          
    def check_alive(self):
        global poeng
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            if self.alive == True:
                poeng += 1 
            self.alive = False 
            self.bytt_bilde()
    
    def bytt_bilde(self):
        img = pygame.image.load('img/player/Death/7.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width()* self.scale), int( img.get_height()* self.scale)))


    def draw(self):
        skjerm.blit(pygame.transform.flip(self.image, self. flip, False), self.rect)    


class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


	def update(self):
		#check if the player has picked up the box
		if pygame.sprite.collide_rect(self, spiller):
			#check what kind of box it was
			if self.item_type == 'health':
				spiller.health += 25
				if spiller.health > spiller.max_health:
					spiller.health = spiller.max_health
			elif self.item_type == 'ammo':
				spiller.ammo += 15
			#delete the item box
			self.kill()
               

class HealthBar():
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health

	def draw(self, health):
          #opptaterer med ny health 
          self.health = health 
          #regner health ratio 
          ratio = self.health / self.max_health
          pygame.draw.rect(skjerm, BLACK, (self.x - 2, self.y - 2, 154, 24) )
          pygame.draw.rect(skjerm, RED, (self.x, self.y, 150, 20) )
          pygame.draw.rect(skjerm, GREEN, (self.x, self.y, 150 * ratio, 20)  )

          
     
class kule(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10 
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self):
        #flytt kula
        self.rect.x += (self.direction * self.speed)
        #sjekker om kule har gått ut av rekkevidde
        if self.rect.right < 0 or self.rect.left > BREDDE - 100:
            self.kill()
        #sjekker kollisjon med fiende
        if pygame.sprite.spritecollide(spiller, kule_group, False):
            if spiller.alive:
                self.kill()
                spiller.health -= 5 
        for fiende in fiende_group:
            if pygame.sprite.spritecollide(fiende, kule_group, False):
                if fiende.alive:
                    fiende.health -= 25
                    self.kill()

#sprite gruppe
kule_group = pygame.sprite.Group()  
fiende_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

#lager item boxes
item_box = ItemBox('health', 100, 360)
item_box_group.add(item_box)
item_box = ItemBox('ammo', 400, 360)
item_box_group.add(item_box)


spiller = soldat('player',200, 200, 1.65, 5, 20)
health_bar = HealthBar(10, 10, spiller.health, spiller.health)


fiende = soldat('enemy',400, 200, 1.65, 2, 20)
fiende2 = soldat('enemy',300, 200, 1.65, 2, 20)
fiende_group.add(fiende)
fiende_group.add(fiende2)


poeng = 0

run = True 
while run: 
    #håndter input
    
    clock.tick(FPS)

    draw_bg()
    #vis spiller health
    health_bar.draw(spiller.health)
    #hvis ammo
    draw_text('AMMO: ', font, WHITE, 10, 35)
    for x in range(spiller.ammo):
         skjerm.blit(bullet_img, (90 + (x * 10), 40))

    spiller.update()
    spiller.draw()

    for fiende in fiende_group:
        fiende.ai()
        fiende.check_alive()
        fiende.draw()
    
    fiende_group.update 

    poeng_sum = font.render("POENG : " + str(poeng), True, WHITE)
    skjerm.blit(poeng_sum, (10, 60))

    kule_group.update()
    kule_group.draw(skjerm)
    item_box_group.update()
    item_box_group.draw(skjerm)

    #opptaterer spiller action  
    if spiller.alive:
        #shoot bullets 
        if shoot:
            spiller.shoot()
        spiller.move(moving_left, moving_right)
        

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #tastatur trykk
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and spiller.alive:
                spiller.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        #tastatur slipp 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False  
            if event.key == pygame.K_SPACE:
                shoot = False

    spiller.draw()

    pygame.display.flip()

pygame : quit
