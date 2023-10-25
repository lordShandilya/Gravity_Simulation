import pygame
import math

pygame.init()

width,height = 800,600
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Gravitational Slingshot Effect")

PLANET_MASS = 100
SHIP_MASS = 5
G = 5
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100

BG = pygame.transform.scale(pygame.image.load("gravitational_simulation/background.jpg"),(width,height))
PLANET = pygame.transform.scale(pygame.image.load("gravitational_simulation/jupiter.png"),(PLANET_SIZE*2,PLANET_SIZE*2))

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

class Planet:
    def __init__(self,x,y,mass):
        self.x = x
        self.y = y 
        self.mass = mass
    
    def draw(self):
        win.blit(PLANET,(self.x - PLANET_SIZE, self.y - PLANET_SIZE))

class Spacecraft:
    def __init__(self,x,y,vel_x,vel_y,mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
    
    def move(self, planet = None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        accl_x = -((G*planet.mass)/(distance**2))*((self.x - planet.x)/distance)
        accl_y = -((G*planet.mass)/(distance**2))*((self.y - planet.y)/distance)
        self.vel_x += accl_x
        self.vel_y += accl_y 
        self.x += self.vel_x
        self.y += self.vel_y
    
    def draw(self):
        pygame.draw.circle(win,RED,(int(self.x),int(self.y)),OBJ_SIZE)


def create_ship(location,mouse):
    t_x,t_y = location
    m_x,m_y = mouse
    vel_x = (m_x - t_x)/VEL_SCALE
    vel_y =  (m_y - t_y)/VEL_SCALE
    obj = Spacecraft(t_x,t_y,vel_x,vel_y,mass=SHIP_MASS)
    return obj

def main():
    running = True
    clock = pygame.time.Clock()

    planet = Planet(width//2,height//2,PLANET_MASS)
    object =[]
    temp_obj_pos = None

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos,mouse_pos)
                    object.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos
        
        win.blit(BG, (0,0))

        if temp_obj_pos:
            pygame.draw.line(win,WHITE,temp_obj_pos,mouse_pos,2)
            pygame.draw.circle(win,RED,temp_obj_pos,OBJ_SIZE)

        for obj in object[:]:
            obj.draw()
            obj.move(planet)
            off_screen = obj.x <0 or obj.x > width or obj.y < 0 or obj.y > height
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_SIZE
            if off_screen or collided:
                object.remove(obj)
            
        planet.draw()

        

        pygame.display.update()
    pygame.quit()
    
if __name__ == "__main__":
    main()
