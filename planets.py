"""
Fra TechWithTim
https://www.youtube.com/watch?v=WTLPmUHTPqo
Reference: https://fiftyexamples.readthedocs.io/en/latest/gravity.html
"""
import pygame
import math
pygame.init()

WIDTH,HEIGHT = 1600,1200
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Planet simulator")

WHITE=(255,255,255)
YELLOW = (255,255,0)
BLUE = (100,149,237)
RED = (188,39,50)
DARK_GREY = (81,79,80)
ORANGE = (255,100,100)
LIGHT_BLUE = (100,100,255)
DARK_BLUE = (0,0,100)
DARK_RED =(150,50,50)
FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 15/AU # 1 AU = 100 Pixels
#    TIMESTEP = 3600*24 # 1 Day
    TIMESTEP = 30600*24 # 1 Day
    
    def __init__(self,x,y,radius,color,mass, name = None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        
        self.x_vel = 0
        self.y_vel = 0

    def draw(self,win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + WIDTH / 2

        if len(self.orbit) > 2:
            updated_points=[]
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x,y))

            pygame.draw.lines(win,self.color,False, updated_points, 2)

        pygame.draw.circle(win,self.color,(x,y),self.radius)

        if not self.sun:
            name_text = FONT.render(f"{self.name}",1,WHITE)
                                    
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000000000, 0)}Mkm", 1, WHITE)

            win.blit(name_text, (x - name_text.get_width()/2, y - name_text.get_height()-10/2))
                     
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()+10/2))

    def attraction(self,other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass/distance**2
        theta = math.atan2(distance_y,distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        return force_x,force_y

    def update_position(self,planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self==planet:
                continue

            fx,fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx/self.mass*self.TIMESTEP
        self.y_vel += total_fy/self.mass*self.TIMESTEP
        
        self.x += self.x_vel*self.TIMESTEP
        self.y += self.y_vel*self.TIMESTEP
        self.orbit.append((self.x,self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0,0,10,YELLOW,1.98892 * 10**30,"Sun")
    sun.sun = True

    earth = Planet(-1 * Planet.AU,0,16,BLUE,5.9742 * 10**24,"Earth")
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.254 * Planet.AU, 0, 12, RED, 6.39 * 10**23, "Mars")
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387*Planet.AU,0,8,DARK_GREY,3.3 *10**23, "Mercur")
    mercury.y_vel = -47.4 * 1000  

    venus = Planet(0.723 * Planet.AU, 0,14,WHITE,4.8685 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(778.5/149.6*Planet.AU,0,55,ORANGE,1898 * 10**24, "Jupiter")
    jupiter.y_vel = -13.1 * 1000

    saturn = Planet(1432/149.6*Planet.AU,0,50,LIGHT_BLUE,568 * 10**24, "Saturn")
    saturn.y_vel = -9.7 * 1000

    uranus = Planet(2867/149.6*Planet.AU,0,27,DARK_RED,86.8 * 10**24,"Uranus")
    uranus.y_vel = -6.8 * 1000

    neptune = Planet(4515/149.6*Planet.AU,0,25,DARK_BLUE,102 * 10**24,"Neptun")
    neptune.y_vel = -5.4 * 1000

    pluto = Planet(5906/149.6*Planet.AU,0,18,DARK_GREY,0.0130 * 10**24, "Pluto")
    pluto.y_vel = -4.7 * 1000



    
    planets = [sun,earth, mars, mercury,venus,jupiter,saturn,uranus,neptune,pluto]

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.K_z:
                planet.SCALE=planet.SCALE-1
                
            
                
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
            
        pygame.display.update()
        
    pygame.quit()

main()
