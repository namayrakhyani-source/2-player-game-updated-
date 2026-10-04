import pygame

pygame.init()

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('2 Player Games')

bg_image = pygame.image.load('assets/bg_image.png')

#creating the divider
divider = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

player_speed = 5
bullet_speed = 10
max_bullets = 3

health_font = pygame.font.SysFont('consolas, couriernew, monospace', 30)
winner_font = pygame.font.SysFont('Times New Roman', 60)

fps = 60

'''
player Class()
'''
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, controls, side):
        #super lets us use and function from parent class, __init__ is the function from parent class
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (100,150))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.controls = controls
        self.side = side
        self.health = 100
        self.bullets = pygame.sprite.Group()

    def movement(self, keys):
        if keys[self.conrols['left']]:
            self.rect.x = self.rect.x - player_speed
        if keys[self.conrols['right']]:
             self.rect.x = self.rect.x + player_speed
        if keys[self.conrols['up']]:
             self.rect.y = self.rect.y - player_speed
        if keys[self.conrols['down']]:
             self.rect.y = self.rect.y + player_speed

player_1 = Player(100, 200, 'assets/soldier_left.png', 
                  {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s}, "left")

player_2 = Player(1100, 200, 'assets/soldier_right.png',
                  {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}, "right" )

players = pygame.sprite.Group()
players.add(player_1, player_2)


def display():
    screen.fill('blue')
    screen.blit(bg_image, (0,0))

    #displaying both the players on the screen
    players.draw(screen)

    #displaying divider on the screen
    pygame.draw.rect(screen, 'black', divider)
    
    pygame.display.update()

def main():
    while True:
        display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
    

    pygame.quit()

main()