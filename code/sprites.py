from settings import * 

class Ground(pygame.sprite.Sprite):
    def __init__(self, pos, texture, groups):
        super().__init__(groups)
        self.image = texture
        self.rect = self.image.get_rect(topleft = pos)
        self.ground = True

class CollisionBoxes(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        # self.image.fill('red')
        self.rect = pygame.Rect(pos, size)

class MapObjects(pygame.sprite.Sprite):
    def __init__(self, pos, texture, groups):

        if texture is None:
            print(f"Warning: Missing texture for object at position {pos}")

        super().__init__(groups)
        self.image = texture
        self.rect = self.image.get_rect(topleft = pos)

class Fire(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.frames = [
            join('sprites', 'fire', '0.png'),
            join('sprites', 'fire', '1.png'),
            join('sprites', 'fire', '2.png'),
            join('sprites', 'fire', '3.png'),
            join('sprites', 'fire', '4.png'),
            join('sprites', 'fire', '5.png'),
            join('sprites', 'fire', '6.png')
        ]

        self.frame = 0
        self.frame_update = pygame.time.get_ticks()
        self.animation_speed = 100
        self.image = pygame.image.load(self.frames[self.frame]).convert_alpha()
        self.rect = self.image.get_rect(midbottom =(pos[0], pos[1] + 30 ))

    def animate(self, dt):

        ticks_passed = pygame.time.get_ticks()
        if ticks_passed - self.frame_update > self.animation_speed:
            self.frame_update = ticks_passed
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = pygame.image.load(self.frames[self.frame]).convert_alpha()
    
    def update(self, dt):
        self.animate(dt)

# class Enemies(pygame.sprite.Sprite):
#     def __init__(self, pos, groups):


