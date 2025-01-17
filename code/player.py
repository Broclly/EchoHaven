from settings import * 
from enemies import MovingEnemy, TNTEnemy

class HealthBar():
    def __init__(self, x, y, w, h, health):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = health
        self.max_hp = 150  # Maximum health is set to a constant value of 150

    def draw(self, surface):
        # Calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, collisions_group, screen, all_sprites, enemy_group):
        super().__init__(groups)
        self.image = pygame.image.load(join('sprites', 'player', 'walk_left', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.hitbox = self.rect.inflate(-100, -100)

        self.health = 150
        self.move_speed = 600
        self.move_distance = 0
        self.score = 0
        self.target_pos = pygame.Vector2(position)
        self.facing = pygame.Vector2()
        self.screen = screen
        self.collisions_group = collisions_group
        self.all_sprites = all_sprites
        self.enemy_group = enemy_group

        # Animation
        self.walkleft_frames = [
            join('sprites', 'player', 'walk_left', '0.png'),
            join('sprites', 'player', 'walk_left', '1.png'),
            join('sprites', 'player', 'walk_left', '2.png'),
            join('sprites', 'player', 'walk_left', '3.png')
        ]

        self.walkright_frames = [
            join('sprites', 'player', 'walk_right', '0.png'),
            join('sprites', 'player', 'walk_right', '1.png'),
            join('sprites', 'player', 'walk_right', '2.png'),
            join('sprites', 'player', 'walk_right', '3.png')
        ]

        self.attackleft_frames = [
            join('sprites', 'player', 'attack_left', '0.png'),
            join('sprites', 'player', 'attack_left', '1.png'),
            join('sprites', 'player', 'attack_left', '2.png'),
            join('sprites', 'player', 'attack_left', '3.png')
        ]

        self.attackright_frames = [
            join('sprites', 'player', 'attack_right', '0.png'),
            join('sprites', 'player', 'attack_right', '1.png'),
            join('sprites', 'player', 'attack_right', '2.png'),
            join('sprites', 'player', 'attack_right', '3.png')
        ]

        self.frame = 0
        self.frame_update = pygame.time.get_ticks()
        self.animation_speed = 100
        self.current_direction = self.walkleft_frames

        # Movement indicator
        self.move_indicator = pygame.image.load(join('sprites', 'UI', 'move_indicator.png')).convert_alpha()
        self.move_indicator = pygame.transform.scale(self.move_indicator, (45, 45))
        self.indicator_rect = self.move_indicator.get_rect()

        # Attacks 
        self.attacking = False
        self.AtkFrame = 0
        self.AtkFrame_update = pygame.time.get_ticks()
        self.Atk_animation_speed = 100
        self.atk_direction = self.attackleft_frames

        self.fireballs = pygame.sprite.Group()
        self.FBcooldown = 500
        self.last_fireball_time = 0

        # Health bar
        self.health_bar = HealthBar(50, 50, 180, 35, self.health) 

        #Game over screen
        self.game_over_image = pygame.image.load(join('sprites', 'UI', 'Game_over (1).png')).convert_alpha()
        self.game_over_rect = self.game_over_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        #Score font
        self.font = pygame.font.Font(pygame.font.match_font('orbitro'), 36)

        # Player Audio 
        self.level_up = pygame.mixer.Sound(join('audio', 'levelup_sound.mp3'))
        self.level_up_played = False
        self.level_up.set_volume(0.1)

        self.sword_attack_sound = pygame.mixer.Sound(join('audio', 'sword_attack.wav'))
        self.sword_attack_sound.set_volume(0.2)

        self.fireball_sound = pygame.mixer.Sound(join('audio', 'Fireball_sound.mp3'))
        self.fireball_sound.set_volume(0.2)


    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            screen_pos = pygame.Vector2(event.pos)
            camera_offset = self.all_sprites.camera_offset
            self.target_pos = screen_pos - camera_offset
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_fireball_time > self.FBcooldown:
                screen_pos = pygame.Vector2(event.pos)
                camera_offset = self.all_sprites.camera_offset 
                self.FBtarget_pos = screen_pos - camera_offset
                if self.score >= 1000:
                    self.shoot_fireball(self.FBtarget_pos)
                    self.fireball_sound.play()
                    self.last_fireball_time = current_time

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.attacking = True
            self.sword_attack_sound.play()

    def update_pos(self, dt):
        if self.attacking:
            self.attack(dt)
        
        if self.hitbox.center !=  self.target_pos:
            move_direction = self.target_pos - pygame.Vector2(self.hitbox.center)
            self.move_distance = move_direction.length()
            
            if self.move_distance != 0:
                if self.move_distance < 5:
                    self.hitbox.center = self.target_pos
                else:
                    move_direction = move_direction.normalize()
                    self.hitbox.center += move_direction * self.move_speed * dt

                    #Checks collisions
                    # new_pos = self.hitbox.center + move_direction * self.move_speed * dt

                    # collide_rect = self.hitbox.copy()
                    # collide_rect.center = new_pos
                    # collisions = pygame.sprite.spritecollide(self, self.collisions_group, False)
                    
                    # if collisions:
                    #     print(f"Collision detected at: {new_pos}")
                    #     for collision in collisions:
                    #         print(f"Colliding with: {collision}")
                        
                    # else:
                    #     self.hitbox.center = new_pos

                self.rect.center = self.hitbox.center
                self.animations(dt)
            
            self.fireballs.update(dt)

    def attack(self, dt):
        ticks_passed = pygame.time.get_ticks()
        if ticks_passed - self.AtkFrame_update > self.Atk_animation_speed:
            self.AtkFrame_update = ticks_passed

            if self.current_direction == self.walkleft_frames:
                self.atk_direction = self.attackleft_frames
            else:
                self.atk_direction = self.attackright_frames

            self.AtkFrame = (self.AtkFrame + 1) % len(self.atk_direction)
            self.image = pygame.image.load(self.atk_direction[self.AtkFrame]).convert_alpha()
            
            if self.AtkFrame == len(self.attackleft_frames) - 1:
                self.attacking = False

            for enemy in self.enemy_group:
                if self.hitbox.colliderect(enemy.hitbox):
                    if isinstance(enemy, (MovingEnemy, TNTEnemy)):
                        enemy.kill()
                        self.health += 2
                        self.score += 100

    def shoot_fireball(self, dt):
        fireball = Fireball(self.rect.center, self.fireballs, self.enemy_group, self.FBtarget_pos, self)
        self.all_sprites.add(fireball)
        self.fireballs.add(fireball)

    def animations(self,dt):
        if not self.attacking:
            if self.target_pos[0] > self.hitbox.center[0]:
                self.current_direction = self.walkright_frames 
            else:
                self.current_direction = self.walkleft_frames
        
        ticks_passed = pygame.time.get_ticks()
        if ticks_passed - self.frame_update > self.animation_speed:
            self.frame_update = ticks_passed
            self.frame = (self.frame + 1) % len(self.current_direction)
            self.image = pygame.image.load(self.current_direction[self.frame]).convert_alpha()

    def moveindicator(self):
        camera_offset = self.all_sprites.camera_offset
        self.indicator_rect.center = self.target_pos + camera_offset
        self.screen.blit(self.move_indicator, self.indicator_rect)

    def update(self, dt):
        if self.health <= 0:
            self.screen.blit(self.game_over_image, self.game_over_rect)
            pygame.display.flip()
            pygame.time.wait(15000)  # Wait for 15 seconds before quitting
            pygame.quit()
            sys.exit()

        #Update health bar
        self.health_bar.hp = self.health
        self.health_bar.draw(self.screen)

        #score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        self.screen.blit(score_text, score_rect)

class Fireball(pygame.sprite.Sprite):
    def __init__(self, pos, groups, enemy_group, target_pos, player):
        super().__init__(groups)
        self.image = pygame.image.load(join('sprites', 'player', 'fireball', 'fireball_sprite.png')).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(0, 0)
        
        self.speed = 550
        self.lifetime = 2000
        self.spawn_timer = pygame.time.get_ticks()
        self.enemy_group = enemy_group
        self.player = player

        facing = pygame.Vector2(target_pos) - pygame.Vector2(pos)
        self.velocity = facing.normalize() * self.speed

    def update(self, dt):
        self.hitbox.center += self.velocity * dt
        self.rect.center = self.hitbox.center

        for enemy in self.enemy_group:
            if self.hitbox.colliderect(enemy.hitbox):
                if isinstance(enemy, (MovingEnemy, TNTEnemy)):
                    enemy.kill()
                    self.player.health += 1
                    self.player.score += 50
                

        if pygame.time.get_ticks() - self.spawn_timer > self.lifetime:
            self.kill()