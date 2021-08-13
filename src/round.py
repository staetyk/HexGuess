import platforms


def main(self):
    img = "../images/clear_pixel.png"
    for x in range(1000):
        up = platforms.Platform(img)
        up.rect.x = x
        up.rect.y = 0
        up.player = self.player
        self.platform_list.add(up)
    for x in range(1000):
        down = platforms.Platform(img)
        down.rect.x = x
        down.rect.y = 650
        down.player = self.player
        self.platform_list.add(down)
    for x in range(650):
        left = platforms.Platform(img)
        left.rect.y = x
        left.rect.x = 0
        left.player = self.player
        self.platform_list.add(left)
    for x in range(650):
        right = platforms.Platform(img)
        right.rect.y = x
        right.rect.x = 1000
        right.player = self.player
        self.platform_list.add(right)