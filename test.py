class PadSprite(pygame.sprite.Sprite):
    normal = pygame.image.load('pad_normal.png')
    hit = pygame.image.load('pad_hit.png')
    def __init__(self, position):
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position
    def update(self, hit_list):
        if self in hit_list: self.image = self.hit
        else: self.image = self.normal
pads = [
    PadSprite((200, 200)),
    PadSprite((800, 200)),
    PadSprite((200, 600)),
    PadSprite((800, 600)),
]
pad_group = pygame.sprite.RenderPlain(*pads)