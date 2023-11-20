import pygame 

pygame.init()


BREDDE = 800
HOYDE = int(BREDDE * 0.8) 

skjerm = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("skytespill")

#setter FPS
clock = pygame.time.Clock()
FPS = 60


#definerer spiller handlinger variabler 
moving_left = False 
moving_right = False

#definerer farger  
BG = (144, 201, 120)

def draw_bg():
    skjerm.fill(BG)




class soldat(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        self. char_type = char_type 
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.flip = False
        img = pygame.image.load(f'img/{self.char_type}/idle/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width()* scale), int( img.get_height()* scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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



        #opptater rect posisjon 
        self.rect.x += dx
        self.rect.y += dy


    def draw(self):
        skjerm.blit(pygame.transform.flip(self.image, self. flip, False), self.rect)
    


spiller = soldat('player',200, 200, 3, 5)
fiende = soldat('enemy',400, 200, 3, 5)

run = True 
while run: 
    
    clock.tick(FPS)

    draw_bg()

    spiller.draw()
    fiende.draw()

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
            if event.key == pygame.K_ESCAPE:
                run = False

        #tastatur slipp 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False  


    pygame.display.flip()

pygame : quit
