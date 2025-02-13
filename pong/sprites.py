from settings import *
from random import choice, uniform


class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)



         # image
        self.image = pygame.Surface(SIZE["paddle"])
        self.image.fill(COLORS["paddle"])

        self.rect = self.image.get_frect(center = POS['player'])
         #rect and movement
        self.old_rect = self.rect.copy()
        self.direction = 0 ## initializing at zero


    def move(self, dt):
        self.rect.centery += self.direction * self.speed * dt 
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)




class Player(Paddle):
    def __init__(self, groups):
        super().__init__(groups)


        self.speed = SPEED['player']


    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN])- int(keys[pygame.K_UP])





class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites):
        super().__init__(groups)

        self.paddle_sprites = paddle_sprites

        self.image = pygame.Surface(SIZE["ball"], pygame.SRCALPHA)
        #self.image.fill(COLORS["ball"])
        pygame.draw.circle(self.image,COLORS["ball"], (SIZE['ball'][0]/2,SIZE['ball'][1]/2),SIZE['ball'][0]/2)

        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.Vector2(choice([1,-1]), uniform(0.7, 0.8)*choice([-1, 1]))

        ## Adding the old_rect for position in past frames
        self.old_rect = self.rect.copy()


    def move(self, dt):
        self.rect.center += self.direction * SPEED['ball'] * dt
        ## making the call to the collision function of ball with paddle
        self.collision("horizontal")

    def wall_collision(self):
        # y dirrection
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1

        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1
 

            

        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction.x *= -1


    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect): ## if the paddle collides with the ball
                if direction == "horizontal":
                    if self.rect.right >= sprite.rect.left and self.direction.x ==  1: ## 1st condition from the board
                        self.rect.right = sprite.rect.left
                       
                    if self.rect.left <= sprite.rect.right and self.direction.x == -1:
                        self.rect.left = sprite.rect.right

                    self.direction.x *= -1 ## this had to be outside of the if statement. That was the glitch


    def update(self, dt):
        self.old_rect = self.rect.copy() ## updating the old_rect
        self.move(dt)
        self.wall_collision()




## The Paddle class had errors because it was tabbed too far to the right and it is Paddle not paddle

class Opponent(Paddle):
    def __init__(self, groups, ball):
        super().__init__(groups)


        self.speed = SPEED['opponent']
        self.rect.center = POS['opponent']
        self.ball = ball



    def get_direction(self):
        ### self.direction was spelled wrong. that is why paddle didn't move
        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1
        