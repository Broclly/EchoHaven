from settings import * 

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.camera_offset = pygame.Vector2()

    def update_offset(self, target_pos):
        self.camera_offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.camera_offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)


    def draw(self, target_pos):
        self.update_offset(target_pos)

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]

        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
                self.screen.blit(sprite.image, sprite.rect.topleft + self.camera_offset)


        # Draw each sprite with the calculated offset as well as ordering the sprites porpperly so that they apprear correctly. 
        # For example, this ensures that when the player walks behind(above) a tree they are drawn behind it and when they walk in front(below) they are drawn in front of it
        # Ground sprites are excepted from the sorting as they are always the bottom layer
        # Camera code from Clear Code on Youtube