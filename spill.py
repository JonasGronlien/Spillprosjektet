import pygame 

pygame.init()


BREDDE = 800
HOYDE = int(BREDDE * 0.8) 

skjerm = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("skytespill")


class soldat(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/player/idle/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width()* scale), int( img.get_height()* scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def draw(self):
        skjerm.blit(self.image, self.rect)
    


spiller = soldat(700, 200, 3)
spiller2 = soldat(400, 200, 3)
        

run = True 
while run: 

    spiller.draw()
    spiller2.draw()

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.flip()

pygame : quit
