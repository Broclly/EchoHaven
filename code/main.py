from settings import * 
from player import Player, HealthBar
from sprites import Ground, CollisionBoxes, MapObjects, Fire
from camera import AllSprites
from pytmx.util_pygame import load_pygame
from enemies import MovingEnemy, TNTEnemy, TNT
import random

BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)  

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("RK Studios")

TITLE_FONT = pygame.font.Font(pygame.font.match_font('orbitro'), 64)

#Frame rate control
clock = pygame.time.Clock()

def typewriter_effect(surface, text, font, color, center, duration):
    alpha = 0
    displayed_text = ""
    char_index = 0
    typewriter_speed = duration * 60 // len(text)  #Calculate speed based on duration and text length

    while char_index < len(text):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        surface.fill(BACKGROUND_COLOR)
        
        if alpha < 255:
            alpha += 255 // (duration * 60)
        
        displayed_text += text[char_index]
        char_index += 1
        
        text_surface = font.render(displayed_text, True, color)
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(center=center)
        
        surface.blit(text_surface, text_rect)
        pygame.display.flip()
        
        clock.tick(typewriter_speed)
    
    #Wait for 2 seconds after the effect is done
    time.sleep(2)

def fade_to_image(surface, image, duration):
    alpha = 0
    fade_speed = 255 // (duration * 60)
    while alpha < 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        surface.fill(BACKGROUND_COLOR)
        image.set_alpha(alpha)
        surface.blit(image, (0, 0))
        pygame.display.flip()
        
        alpha += fade_speed
        clock.tick(60)

def title_screen():
    typewriter_effect(
        surface=screen,
        text="RK Studios",
        font=TITLE_FONT,
        color=TEXT_COLOR,  #Set the color to red
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
        duration=3,  #typewriter effect duration in seconds
    )

title_screen()

#Main game setup
pygame.display.set_caption("Echohaven")

def load_image(file_path):
    print(f"Loading image from: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file or directory: '{file_path}'")
    return pygame.image.load(file_path).convert_alpha()

#Define the relative file paths for the images
cursor_path = os.path.join("sprites", "UI", "mouse_pointer.png")
loading_image_path = os.path.join("sprites", "UI", "title_screen.png")
next_image_path = os.path.join("sprites", "UI", "keybind_screen.png")
button_image_path = os.path.join("sprites", "UI", "ContinueButtonNP.png")
button_pressed_image_path = os.path.join("sprites", "UI", "ContinueButtonP.png")

#Load the cursor image
custom_cursor = load_image(cursor_path)

#Load the loading screen image
loading_image = load_image(loading_image_path)

#Load the next image
next_image = load_image(next_image_path)

#Load the button images
button_image = load_image(button_image_path)
button_pressed_image = load_image(button_pressed_image_path)

#Resize the images to fit the screen (1280x720)
loading_image = pygame.transform.scale(loading_image, (1280, 720))
next_image = pygame.transform.scale(next_image, (1280, 720))

#Button position
button_rect = button_image.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 70))

#Fade to the next image after the title screen
fade_to_image(screen, next_image, 2)  #2 seconds fade duration

#Main game loop begins
running = True
loading = False
show_next_image = True
button_pressed = False
start_fade = False
alpha = 255  #Set the opacity of the effect
fade_speed = 2  #Define how fast the fade effect should happen

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            #Start the fade effect when Enter is pressed
            if loading:
                start_fade = True
                alpha = 255  #Reset alpha for fade effect
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                button_pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            if button_pressed:
                button_pressed = False
                loading = True
                show_next_image = False

    #Clear the screen by filling it with black
    screen.fill((0, 0, 0))

    if show_next_image:
        #Display the next image on the screen
        screen.blit(next_image, (0, 0))

        #Display the button
        if button_pressed:
            screen.blit(button_pressed_image, button_rect)
        else:
            screen.blit(button_image, button_rect)

        #Always display the custom cursor during the next image screen
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(custom_cursor, (mouse_x, mouse_y))

        #Hide the system cursor since the custom cursor is being used
        pygame.mouse.set_visible(False)

    elif loading:
        #Display the loading image on the screen
        screen.blit(loading_image, (0, 0))

        #Always display the custom cursor during the loading screen
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(custom_cursor, (mouse_x, mouse_y))

        #Hide the system cursor since the custom cursor is being used
        pygame.mouse.set_visible(False)

        #Once Enter is pressed, start the fade effect to the black screen
        if start_fade and alpha > 0:
            alpha -= fade_speed
            fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(255 - alpha)
            screen.blit(fade_surface, (0, 0))
        elif start_fade and alpha <= 0:
            #Clear the screen to black after fade is complete
            screen.fill((0, 0, 0))
            running = False  #Exit the loop to start the main game

    pygame.display.flip()

    clock.tick(60)









class Game:
    def __init__(self):

        # game setup 
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Echohaven")
        self.clock = pygame.time.Clock()
        self.running = True

        #mouse
        pygame.mouse.set_visible(True)
        cursor_path = os.path.join("sprites", "UI", "mouse_pointer.png")
        custom_cursor = load_image(cursor_path)
        pygame.mouse.set_cursor((8, 8), custom_cursor)

        #audio
        pygame.mixer.init()
        self.main_theme = os.path.join("audio", "Main_theme.mp3")
        pygame.mixer.music.load(self.main_theme)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        
        # Sprite groups
        self.all_sprites = AllSprites()
        self.collisions_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        

        # Entities
        self.spawn_points = []
        self.fire_entities = []

        # Enemy cooldown
        self.spawn_cooldown = 16000
        self.last_spawn = 0


        # Load
        self.load_map()


    def load_map(self):
        game_map = load_pygame(join('map', 'maps', 'game_map2.tmx'))


        # Tile Layers
        for x,y, image in game_map.get_layer_by_name('ground_0').tiles():
            Ground((x*TILE_SIZE, y*TILE_SIZE), image, self.all_sprites)

        for x,y, image in game_map.get_layer_by_name('ground_1').tiles():
            Ground((x*TILE_SIZE, y*TILE_SIZE), image, self.all_sprites)

        for x,y, image in game_map.get_layer_by_name('ground_2').tiles():
            Ground((x*TILE_SIZE, y*TILE_SIZE), image, self.all_sprites)

        for x,y, image in game_map.get_layer_by_name('ground_3').tiles():
            Ground((x*TILE_SIZE, y*TILE_SIZE), image, self.all_sprites)

         # Objects 
        for obj in game_map.get_layer_by_name('objects'):
            texture = game_map.get_tile_image_by_gid(obj.gid)
            if texture:
                MapObjects((obj.x, obj.y), texture, self.all_sprites)

        # Villagers
        for villager in game_map.get_layer_by_name('villagers'):
            texture = game_map.get_tile_image_by_gid(villager.gid)
            if texture:
                MapObjects((villager.x, villager.y), texture, self.all_sprites)
        
        # Collisions
        for box in game_map.get_layer_by_name('collisions'):
            CollisionBoxes((box.x, box.y), (box.width, box.height), (self.all_sprites, self.collisions_group))
        
        # Spawn points
        for spawn_point in game_map.get_layer_by_name('spawns'):
            if spawn_point.name == 'player':
                self.player = Player((spawn_point.x, spawn_point.y), self.all_sprites, self.collisions_group, self.screen, self.all_sprites, self.enemy_group)
                
            elif spawn_point.name == 'fire':
                self.fire_entities.append((spawn_point.x, spawn_point.y))

                for entity in self.fire_entities:
                    Fire(entity, self.all_sprites)

            elif spawn_point.name == 'enemy':
                self.spawn_points.append((spawn_point.x, spawn_point.y))


    def spawn_enemies(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn > self.spawn_cooldown:
                for spawn in self.spawn_points:
                    random_enemy = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

                    if random_enemy == 1 or random_enemy == 2 or random_enemy == 3:
                        MovingEnemy((spawn[0], spawn[1]), [self.all_sprites, self.enemy_group], self.player)
                    
                    if random_enemy == 5 and self.player.score >= 2500:
                        MovingEnemy((spawn[0], spawn[1]), [self.all_sprites, self.enemy_group], self.player)

                    if random_enemy == 6 and self.player.score >= 5000:
                        MovingEnemy((spawn[0], spawn[1]), [self.all_sprites, self.enemy_group], self.player)

                    if random_enemy == 7 and self.player.score >= 7500:
                        TNTEnemy((spawn[0], spawn[1]), [self.all_sprites, self.enemy_group], self.player, )
                    
                    if random_enemy == 4:
                        TNTEnemy((spawn[0], spawn[1]), [self.all_sprites, self.enemy_group], self.player, )

                self.last_spawn = current_time


    def run(self): 
        while self.running:

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.player.events(event)

            # Delta time
            dt = self.clock.tick(60) / 1000.0 # delta time ensures that the game runs at a consistant speed regardless of the frame rate
            
            # Update
            self.all_sprites.update(dt)
            self.player.update_pos(dt)
            self.all_sprites.update_offset(self.player.rect.center)
            if self.player.score > 1000 and self.player.level_up_played == False:
                self.player.level_up.play()
                self.player.level_up_played = True

            self.spawn_enemies()

            # Draw
            self.screen.fill((71, 171, 169)) # Colour of the map water 
            self.all_sprites.draw(self.player.rect.center)
            self.player.moveindicator()
            
            #Draw health bar last to ensure its on top of everything
            self.player.health_bar.draw(self.screen)
            self.player.update(dt)

            pygame.display.flip()

            # #Check if player is dead
            # if self.player.health <= 0:
            #     self.running = False

        
        
        pygame.quit()



if __name__ == '__main__': # will only run if this file is the main file
    game = Game()
    game.run()