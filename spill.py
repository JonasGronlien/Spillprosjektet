import pygame 

pygame.init()


BREDDE = 800
HOYDE = int(BREDDE * 0.8) 

skjerm = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("skytespill")



x = 200
y = 200



run = True 
while run: 

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run : False


pygame : quit
