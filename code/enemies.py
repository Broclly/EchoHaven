from settings import *
import random
import pygame
from os.path import join

class MovingEnemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.player = player 
        
        self.frames_barrel = [
            join('sprites', 'enemies', 'barrel', '0.png'),
            join('sprites', 'enemies', 'barrel', '1.png'),
            join('sprites', 'enemies', 'barrel', '2.png'),
            join('sprites', 'enemies', 'barrel', '3.png'),
            join('sprites', 'enemies', 'barrel', '4.png')
        ]

        self.frames_torch = [
            join('sprites', 'enemies', 'torch', '0.png'),
            join('sprites', 'enemies', 'torch', '1.png'),
            join('sprites', 'enemies', 'torch', '2.png'),
            join('sprites', 'enemies', 'torch', '3.png'),
            join('sprites', 'enemies', 'torch', '4.png')
        ]
       
        self.enemy_variant = random.choice([self.frames_barrel, self.frames_torch])
        self.frames = self.enemy_variant

        self.frame = 0
        self.frame_update = pygame.time.get_ticks()
        self.animation_speed = 100
        self.speed = 85

        self.image = pygame.image.load(self.frames[self.frame]).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-75, -75)
        
        self.damage_cooldown = 2000
        self.last_damage = 0

    def animate(self):
        ticks_passed = pygame.time.get_ticks()
        if ticks_passed - self.frame_update > self.animation_speed:
            self.frame_update = ticks_passed
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = pygame.image.load(self.frames[self.frame]).convert_alpha()

    def move(self, dt):
        direction = pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize()
            self.hitbox.center += direction * self.speed * dt
            self.rect.center = self.hitbox.center

    def collisions(self):
        current_time = pygame.time.get_ticks()
        if pygame.sprite.collide_rect(self, self.player):
            if current_time - self.last_damage > self.damage_cooldown:
                self.player.health -= 5
                self.last_damage = current_time
            

    def update(self, dt):
        self.animate()
        self.move(dt)
        self.collisions()     

class TNTEnemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.player = player
        self.all_sprites, self.enemies_group = groups

        self.frames_tnt = [
            join('sprites', 'enemies', 'tnt', '0.png'),
            join('sprites', 'enemies', 'tnt', '1.png'),
            join('sprites', 'enemies', 'tnt', '2.png'),
            join('sprites', 'enemies', 'tnt', '3.png'),
            join('sprites', 'enemies', 'tnt', '4.png'),
            join('sprites', 'enemies', 'tnt', '5.png'),
            join('sprites', 'enemies', 'tnt', '6.png')
        ]
        
        self.image = pygame.image.load(join('sprites', 'enemies', 'tnt', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-75, -75)
        
        self.frame = 0
        self.frame_update = pygame.time.get_ticks()
        self.animation_speed = 100
        self.speed = 100

        self.tnt_throw_cooldown = 3000
        self.last_tnt_throw = 0

    def throw_tnt(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_tnt_throw > self.tnt_throw_cooldown:
            tnt = TNT(self.rect.center, self.player.rect.center, self.all_sprites, self.player)
            self.all_sprites.add(tnt)
            self.last_tnt_throw = current_time

    def animate(self):
        ticks_passed = pygame.time.get_ticks()
        if ticks_passed - self.frame_update > self.animation_speed:
            self.frame_update = ticks_passed
            self.frame = (self.frame + 1) % len(self.frames_tnt)
            self.image = pygame.image.load(self.frames_tnt[self.frame]).convert_alpha()

    def update(self, dt):
        self.animate()
        self.throw_tnt()


class TNT(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos, groups, player):
        super().__init__(groups)
        self.image = pygame.image.load(join('sprites', 'enemies', 'dynamite', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-75, -75)

        self.speed = 300
        self.player = player
        direction = pygame.Vector2(target_pos) - pygame.Vector2(pos)
        self.velocity = direction.normalize() * self.speed

    def update(self, dt):
        self.hitbox.center += self.velocity * dt
        self.rect.center = self.hitbox.center
        self.check_collisions()

    def check_collisions(self):
        if self.hitbox.colliderect(self.player.hitbox):
            self.player.health -= 4
            self.kill()
            