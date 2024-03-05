import pygame as pg
import pygame.time
from functools import cache
import pyautogui as py


@cache
def get_points(x0, y0, radius):
    x = radius
    y = 0
    err = 0

    l1, l2, l3, l4, l5, l6, l7, l8 = [], [], [], [], [], [], [], []

    while x >= y:
        l1.append((x0 - x, y0 - y))
        l2.insert(0, (x0 - y, y0 - x))
        l3.append((x0 + y, y0 - x))
        l4.insert(0, (x0 + x, y0 - y))
        l5.append((x0 + x, y0 + y))
        l6.insert(0, (x0 + y, y0 + x))
        l7.append((x0 - y, y0 + x))
        l8.insert(0, (x0 - x, y0 + y))

        y += 1
        err += 1 + 2 * y
        if 2 * (err - x) + 1 > 0:
            x -= 1
            err += 1 - 2 * x

    return set((*l1, *l2, *l3, *l4, *l5, *l6, *l7, *l8))


@cache
def get_colors(h):
    colors = [0, 0, 0, 0]

    if h > 765:
        h %= 765

    index = int(h // 255)

    colors[index] = (h-1) % 255
    colors[index-1] = 255 - (h-1) % 255

    if index == 1:
        colors = (colors[1], colors[2], colors[0])
    else:
        colors = colors[1::]

    return colors[0], colors[1], colors[2]


class Circle:
    def __init__(self, screen, x, y, max_point, smooth):
        self.x, self.y = x, y
        self.max_point = max_point
        self.now = 0
        self.smooth = smooth
        self.screen = screen

    def update(self):
        self.now += self.smooth

        circle = get_points(self.x, self.y, self.now)

        h = 100
        for points in circle:
            h += 4
            pg.draw.rect(self.screen, get_colors(int(h)), (*points, 1, 1))


class App:
    def __init__(self):
        pg.init()
        self.size = py.size()
        self.sc = pg.display.set_mode(self.size)
        self.black = 0, 0, 0
        self.clock = pygame.time.Clock()
        self.circles = []
        self.alpha_surface = pg.Surface(self.size)
        self.alpha_surface.set_alpha(20)

    def run(self):
        a = 1
        while True:
            self.clock.tick(144)
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
                    exit()
                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    pos = pg.mouse.get_pos()
                    self.circles.append(Circle(self.sc, *pos, max_point=350, smooth=6)) #randint(200, 800), smooth=randint(10, 30)))
            self.sc.blit(self.alpha_surface, (0, 0))

            a += 1

            if a % 14 == 0:
                pos = pg.mouse.get_pos()
                self.circles.append(Circle(self.sc, *pos, max_point=90, smooth=2)) #randint(10, 110), smooth=randint(2, 5))) #90, 2

            [circle.update() if circle.now < circle.max_point else self.circles.remove(circle)
             for circle in self.circles]

            pygame.display.set_caption(str(self.clock.get_fps()))

            pg.display.update()


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
