import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airship Landing Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)

class Airship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 50
        self.vx = 0
        self.vy = 0
        self.width = 60
        self.height = 40
        self.fuel = 1000
        self.gravity = 0.05
        self.thrust_power = 0.15
        self.side_thrust = 0.05
        self.is_thrusting = False
        self.crashed = False
        self.landed = False

    def update(self):
        if self.crashed or self.landed:
            return

        self.is_thrusting = False
        keys = pygame.key.get_pressed()
        
        if self.fuel > 0:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.vy -= self.thrust_power
                self.fuel -= 2
                self.is_thrusting = True
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.vx -= self.side_thrust
                self.fuel -= 1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.vx += self.side_thrust
                self.fuel -= 1

        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        # Draw Airship balloon
        rect = pygame.Rect(int(self.x - self.width//2), int(self.y - self.height//2), self.width, self.height)
        pygame.draw.ellipse(surface, GRAY, rect)
        
        # Draw basket
        basket_width = 20
        basket_height = 15
        basket_rect = pygame.Rect(int(self.x - basket_width//2), int(self.y + self.height//2), basket_width, basket_height)
        pygame.draw.rect(surface, BROWN, basket_rect)

        # Draw ropes connecting balloon to basket
        pygame.draw.line(surface, WHITE, (int(self.x - self.width//3), int(self.y)), (int(self.x - basket_width//2), int(self.y + self.height//2)))
        pygame.draw.line(surface, WHITE, (int(self.x + self.width//3), int(self.y)), (int(self.x + basket_width//2), int(self.y + self.height//2)))

        # Draw flame
        if self.is_thrusting:
            flame_points = [
                (self.x - 5, self.y + self.height//2 + basket_height + 2),
                (self.x + 5, self.y + self.height//2 + basket_height + 2),
                (self.x, self.y + self.height//2 + basket_height + 20 + random.randint(-5, 5))
            ]
            pygame.draw.polygon(surface, YELLOW, flame_points)
            
    def get_bottom_pos(self):
        # Returns the (x, y) coordinates of the bottom center of the airship's basket
        return (self.x, self.y + self.height//2 + 15)

class Terrain:
    def __init__(self):
        # Randomly generate terrain while ensuring there's a flat landing pad
        self.points = [
            (0, random.randint(300, 500)),
            (100, random.randint(300, 500)),
            (250, random.randint(300, 500)),
            (350, 480), # Landing pad start
            (450, 480), # Landing pad end
            (550, random.randint(300, 500)),
            (700, random.randint(300, 500)),
            (800, random.randint(300, 500))
        ]
        self.pad_start = 3
        self.pad_end = 4

    def draw(self, surface):
        # Draw terrain surface
        pygame.draw.lines(surface, WHITE, False, self.points, 2)
        
        # Draw terrain fill (polygons underneath the line)
        fill_points = [(0, HEIGHT)] + self.points + [(WIDTH, HEIGHT)]
        pygame.draw.polygon(surface, (40, 40, 40), fill_points)

        # Highlight landing pad
        pad_p1 = self.points[self.pad_start]
        pad_p2 = self.points[self.pad_end]
        pygame.draw.line(surface, GREEN, pad_p1, pad_p2, 5)

    def check_collision(self, airship):
        ship_bottom_x, ship_bottom_y = airship.get_bottom_pos()

        # Out of bounds check
        if ship_bottom_x < 0 or ship_bottom_x > WIDTH or ship_bottom_y < 0 or ship_bottom_y > HEIGHT:
            return "crash"

        # Check intersection with terrain lines
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            
            if p1[0] <= ship_bottom_x <= p2[0]:
                # Interpolate y on the line segment directly under the ship
                t = (ship_bottom_x - p1[0]) / (p2[0] - p1[0])
                terrain_y = p1[1] + t * (p2[1] - p1[1])
                
                # If the ship reaches or passes the terrain ground level
                if ship_bottom_y >= terrain_y - 2:
                    # Check if on the landing pad
                    if i == self.pad_start:
                        # Check landing conditions (speed requirements)
                        if abs(airship.vy) < 2.0 and abs(airship.vx) < 1.0:
                            return "land"
                        else:
                            return "crash"
                    else:
                        return "crash"
        return "none"

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def main():
    airship = Airship()
    terrain = Terrain()
    
    running = True
    game_over = False
    message = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    # Reset game
                    airship = Airship()
                    terrain = Terrain()
                    game_over = False
                    message = ""

        if not game_over:
            airship.update()
            status = terrain.check_collision(airship)
            
            if status == "crash":
                airship.crashed = True
                game_over = True
                message = "CRASHED! Press 'R' to restart."
            elif status == "land":
                airship.landed = True
                game_over = True
                message = "SUCCESSFUL LANDING! Press 'R' to restart."

        # Drawing
        screen.fill(BLACK)
        terrain.draw(screen)
        airship.draw(screen)
        
        # HUD / UI
        draw_text(f"Fuel: {max(0, airship.fuel)}", WHITE, 10, 10)
        draw_text(f"V. Speed: {abs(airship.vy):.1f} (Target < 2.0)", GREEN if abs(airship.vy) < 2.0 else RED, 10, 40)
        draw_text(f"H. Speed: {abs(airship.vx):.1f} (Target < 1.0)", GREEN if abs(airship.vx) < 1.0 else RED, 10, 70)

        if game_over:
            color = GREEN if airship.landed else RED
            text_rect = font.render(message, True, color).get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(font.render(message, True, color), text_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()