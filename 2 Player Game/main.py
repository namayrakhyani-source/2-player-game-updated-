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
clock = pygame.time.Clock()

'''
bullet Class()
'''
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((12,6))
        self.image.fill("red")
        self.rect = self.image.get_rect(center = (x,y))
        self.direction = direction

    def update(self):
        self.rect.x += bullet_speed * self.direction
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill() 


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


    def shoot(self):
        if len(self.bullets) >= max_bullets:
            return
        if self.side == 'left':
            bullet = Bullet(self.rect.right, self.rect.centery, 1)
        else:
            bullet = Bullet(self.rect.left, self.rect.centery, -1)
        self.bullets.add(bullet)


    def update(self):
        self.bullets.update()


    def movement(self, keys):
        if keys[self.controls['left']]:
            self.rect.x = self.rect.x - player_speed
        if keys[self.controls['right']]:
             self.rect.x = self.rect.x + player_speed
        if keys[self.controls['up']]:
             self.rect.y = self.rect.y - player_speed
        if keys[self.controls['down']]:
             self.rect.y = self.rect.y + player_speed

        #Setting boundaries
        #Setting top and bottom boundaries for both players
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(HEIGHT, self.rect.bottom)
        if self.side == 'left':
            self.rect.left = max(0, self.rect.left)
            self.rect.right = min(divider.left, self.rect.right)
        else:
            self.rect.left = max(divider.right, self.rect.left)
            self.rect.right = min(WIDTH, self.rect.right)

player_1 = Player(100, 200, 'assets/soldier_left.png', 
                  {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s}, "left")

player_2 = Player(1100, 200, 'assets/soldier_right.png',
                  {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}, "right" )

players = pygame.sprite.Group()
players.add(player_1, player_2)


def check_collision():
    for bullet in player_1.bullets:
        if bullet.rect.colliderect(player_2.rect):
            player_2.health -= 10
            bullet.kill()

    for bullet in player_2.bullets:
        if bullet.rect.colliderect(player_1.rect):
            player_1.health -= 10
            bullet.kill()


def display():
    screen.fill('blue')
    screen.blit(bg_image, (0,0))

    #Applying font on text using render function. This function does not display the text
    player_1_text = health_font.render(f'Player 1: {player_1.health}', True, 'green')
    #Displaying text on screen
    screen.blit(player_1_text, (30,30))

    player_2_text = health_font.render(f'Player 2: {player_2.health}', True, 'green')
    screen.blit(player_2_text, (950, 30))

    #displaying both the players on the screen
    players.draw(screen)

    #displaying divider on the screen
    pygame.draw.rect(screen, 'black', divider)

    #displaying bullets
    player_1.bullets.draw(screen)
    player_2.bullets.draw(screen)
    
    pygame.display.update()

def main():
    is_running = True
    while is_running:
        clock.tick(fps)
        display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
                is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    player_1.shoot()
                if event.key == pygame.K_RSHIFT:
                    player_2.shoot()

        #calling update function of the player class
        players.update()
        check_collision()

        #Condition for game end
        if player_1.health <= 0:
            print('PLAYER 2 WINS!')
            break
        if player_2.health <= 0:
            print('PLAYER 1 WINS!')
            break

        #Getting all the keys pressed
        keys = pygame.key.get_pressed()

        #Calling move function for the players
        player_1.movement(keys)
        player_2.movement(keys)
