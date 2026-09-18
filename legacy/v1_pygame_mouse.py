

#鼠标代替
import pygame
import random
import math

# --- Configuration ---
WIDTH, HEIGHT = 800, 600
PARTICLE_COUNT = 1200
TREE_COLOR = (50, 255, 100)
STAR_COLOR = (255, 255, 0)
bg_color = (10, 10, 20)

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Light Particle Christmas Tree (Mouse Version)")
clock = pygame.time.Clock()


class Particle:
    def __init__(self, x, y, is_star=False):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.target_x = x
        self.target_y = y
        self.vx = 0
        self.vy = 0
        self.is_star = is_star

        if self.is_star:
            self.color = STAR_COLOR
            self.size = 6
        else:
            if random.random() > 0.95:
                self.color = (255, 50, 50)  # Red
            elif random.random() > 0.95:
                self.color = (50, 100, 255)  # Blue
            else:
                g = random.randint(150, 255)
                self.color = (50, g, 50)
            self.size = 2

    def update(self, hand_pos):
        # 1. Force towards Home
        dx_home = self.target_x - self.x
        dy_home = self.target_y - self.y

        force_home = 0.05
        ax = dx_home * force_home
        ay = dy_home * force_home

        # 2. Force from Mouse
        if hand_pos:
            hx, hy = hand_pos
            dx_hand = hx - self.x
            dy_hand = hy - self.y
            dist_hand = math.hypot(dx_hand, dy_hand)

            interaction_radius = 150
            if dist_hand < interaction_radius:
                angle = math.atan2(dy_hand, dx_hand)
                rotation_force = 1.5

                # Swirl effect
                ax += math.cos(angle + math.pi / 2) * rotation_force
                ay += math.sin(angle + math.pi / 2) * rotation_force

                ax += random.uniform(-0.5, 0.5)
                ay += random.uniform(-0.5, 0.5)

        friction = 0.85
        self.vx = (self.vx + ax) * friction
        self.vy = (self.vy + ay) * friction

        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


def generate_tree_targets():
    targets = []
    for i in range(PARTICLE_COUNT):
        h = i / PARTICLE_COUNT
        radius = 150 * h
        angle = 20 * h * 2 * math.pi
        tx = WIDTH // 2 + radius * math.cos(angle)
        ty = 100 + h * 400
        targets.append((tx, ty, False))
    targets.append((WIDTH // 2, 90, True))
    return targets


# --- Setup ---
target_positions = generate_tree_targets()
particles = [Particle(tx, ty, is_star) for tx, ty, is_star in target_positions]

# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get Mouse Position instead of Camera
    mouse_pos = pygame.mouse.get_pos()

    screen.fill(bg_color)

    # Draw faint glow at mouse
    pygame.draw.circle(screen, (30, 30, 50), mouse_pos, 40)

    for p in particles:
        p.update(mouse_pos)
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()