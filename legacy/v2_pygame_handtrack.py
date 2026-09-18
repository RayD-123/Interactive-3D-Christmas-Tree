'''
import cv2
import mediapipe as mp
import pygame
import random
import math

# --- Configuration ---
WIDTH, HEIGHT = 800, 600
PARTICLE_COUNT = 1200
TREE_COLOR = (50, 255, 100)  # Greenish
STAR_COLOR = (255, 255, 0)  # Yellow
bg_color = (10, 10, 20)  # Dark night background

# --- Initialize MediaPipe for Hand Tracking ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
    max_num_hands=1
)

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Light Particle Christmas Tree")
clock = pygame.time.Clock()


class Particle:
    def __init__(self, x, y, is_star=False):
        self.x = random.randint(0, WIDTH)  # Start at random position
        self.y = random.randint(0, HEIGHT)
        self.target_x = x
        self.target_y = y
        self.vx = 0
        self.vy = 0
        self.is_star = is_star

        # Randomize colors slightly for a "light" effect
        if self.is_star:
            self.color = STAR_COLOR
            self.size = 6
        else:
            # Varying shades of green and some ornaments (red/blue)
            if random.random() > 0.95:
                self.color = (255, 50, 50)  # Red ornament
            elif random.random() > 0.95:
                self.color = (50, 100, 255)  # Blue ornament
            else:
                g = random.randint(150, 255)
                self.color = (50, g, 50)
            self.size = 2

    def update(self, hand_pos):
        # 1. Force towards the tree target (Home position)
        dx_home = self.target_x - self.x
        dy_home = self.target_y - self.y
        dist_home = math.hypot(dx_home, dy_home)

        # Spring force towards home
        force_home = 0.05
        ax = dx_home * force_home
        ay = dy_home * force_home

        # 2. Force towards/away from Hand (Interaction)
        if hand_pos:
            hx, hy = hand_pos
            dx_hand = hx - self.x
            dy_hand = hy - self.y
            dist_hand = math.hypot(dx_hand, dy_hand)

            # If hand is close, particles react
            interaction_radius = 150
            if dist_hand < interaction_radius:
                # Swirl effect: Add a perpendicular force for rotation
                angle = math.atan2(dy_hand, dx_hand)
                rotation_force = 1.5

                # Attraction or Repulsion (Mix for swirl)
                # Currently set to mild attraction + strong rotation
                ax += math.cos(angle + math.pi / 2) * rotation_force
                ay += math.sin(angle + math.pi / 2) * rotation_force

                # Add a little jitter when near hand
                ax += random.uniform(-0.5, 0.5)
                ay += random.uniform(-0.5, 0.5)

        # Apply friction/damping so they don't oscillate forever
        friction = 0.85
        self.vx = (self.vx + ax) * friction
        self.vy = (self.vy + ay) * friction

        # Update position
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


def generate_tree_targets():
    """Generates coordinates for a spiral cone tree."""
    targets = []

    # Tree Body (Spiral)
    for i in range(PARTICLE_COUNT):
        # Normalized height (0 at top, 1 at bottom)
        h = i / PARTICLE_COUNT

        # Cone width expands as we go down
        radius = 150 * h

        # Spiral angle
        angle = 20 * h * 2 * math.pi

        tx = WIDTH // 2 + radius * math.cos(angle)
        ty = 100 + h * 400

        targets.append((tx, ty, False))

    # Add a Star at the top
    targets.append((WIDTH // 2, 90, True))

    return targets


# --- Setup Particles ---
target_positions = generate_tree_targets()
particles = [Particle(tx, ty, is_star) for tx, ty, is_star in target_positions]

# --- Main Loop ---
cap = cv2.VideoCapture(0)

running = True
while running:
    # 1. Handle Event Queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Computer Vision (Hand Tracking)
    success, frame = cap.read()
    hand_pos = None

    if success:
        # Flip frame horizontally for mirror effect and convert to RGB
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            # Get the tip of the index finger of the first hand
            landmark = results.multi_hand_landmarks[0].landmark[8]  # 8 is Index Finger Tip

            # Map normalized coordinates (0-1) to screen size
            hand_x = int(landmark.x * WIDTH)
            hand_y = int(landmark.y * HEIGHT)
            hand_pos = (hand_x, hand_y)

    # 3. Update & Draw
    screen.fill(bg_color)

    # Draw a faint glow for the hand
    if hand_pos:
        pygame.draw.circle(screen, (30, 30, 50), hand_pos, 40)

    for p in particles:
        p.update(hand_pos)
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

# Cleanup
cap.release()
pygame.quit()
'''
#黑色背景 圣诞树3.10版本 无过多装饰 手势只能指哪里打哪里，类似融化特效

'''
import cv2
import mediapipe as mp
import pygame
import random
import math

# --- 1. Configuration & Colors (配置与颜色) ---
WIDTH, HEIGHT = 1000, 700  # 稍微大一点的窗口
PARTICLE_COUNT = 1500  # 增加粒子数量

# Color Palette (配色板 - 金属感与节日气氛)
BG_COLOR = (245, 240, 225)  # 米黄色背景 Warm Beige
GOLD = (232, 195, 85)  # 金色
SILVER = (210, 210, 215)  # 银色
RED = (220, 40, 60)  # 圣诞红
GREEN = (50, 160, 80)  # 圣诞绿
BLUE = (60, 100, 230)  # 宝蓝
WARM_WHITE = (255, 250, 220)  # 暖白光

COLOR_PALETTE = [GOLD, SILVER, RED, GREEN, BLUE, WARM_WHITE]

# --- 2. Initialize MediaPipe & Pygame (初始化) ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
    max_num_hands=1
)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("豪华金属质感互动圣诞树")
clock = pygame.time.Clock()

# 启用透明度支持
s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


# --- 3. Helper Functions (辅助函数) ---

def draw_star(surface, color, x, y, size):
    """绘制一个五角星"""
    points = []
    # 计算五角星的10个顶点
    for i in range(10):
        angle = i * 36 * math.pi / 180 - math.pi / 2
        # 外点和内点交替
        radius = size if i % 2 == 0 else size * 0.4
        px = x + radius * math.cos(angle)
        py = y + radius * math.sin(angle)
        points.append((px, py))

    # 绘制主体
    pygame.draw.polygon(surface, color, points)
    # 绘制高光边缘让它更有金属感
    pygame.draw.polygon(surface, (255, 255, 200), points, 2)


# --- 4. Classes (类定义) ---

class GiftBox:
    """树下的礼物盒"""

    def __init__(self):
        self.w = random.randint(40, 80)
        self.h = random.randint(30, 60)
        # 放置在地面附近
        self.x = random.randint(WIDTH // 2 - 300, WIDTH // 2 + 300)
        self.y = HEIGHT - self.h - random.randint(5, 30)

        base_color = random.choice([RED, GREEN, BLUE, GOLD])
        # 让颜色稍微暗一点作为底色
        self.color = [max(0, c - 30) for c in base_color]
        self.ribbon_color = GOLD if base_color != GOLD else RED

    def draw(self, surface):
        # 盒子主体
        box_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(surface, self.color, box_rect)

        # 绘制金属感高光边框
        pygame.draw.rect(surface, [min(255, c + 60) for c in self.color], box_rect, 3)

        # 丝带十字
        ribbon_width = 8
        # 竖向丝带
        pygame.draw.rect(surface, self.ribbon_color,
                         (self.x + self.w // 2 - ribbon_width // 2, self.y, ribbon_width, self.h))
        # 横向丝带
        pygame.draw.rect(surface, self.ribbon_color,
                         (self.x, self.y + self.h // 2 - ribbon_width // 2, self.w, ribbon_width))


class Particle:
    def __init__(self, x, y):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        # 加入一点随机抖动，让树看起来更自然蓬松
        jitter = 15
        self.target_x = x + random.uniform(-jitter, jitter)
        self.target_y = y + random.uniform(-jitter, jitter)
        self.vx = 0
        self.vy = 0

        # 大小不一：增加随机范围
        self.base_size = random.randint(3, 9)
        self.current_size = self.base_size

        # 颜色与金属质感
        self.base_color = random.choice(COLOR_PALETTE)
        # 高光颜色：比底色更亮，接近白色
        self.highlight_color = (
            min(255, self.base_color[0] + 100),
            min(255, self.base_color[1] + 100),
            min(255, self.base_color[2] + 100)
        )

        # 随机闪烁参数
        self.blink_speed = random.uniform(0.02, 0.05)
        self.blink_phase = random.uniform(0, math.pi * 2)

    def update(self, hand_pos):
        # 1. 回家去（目标位置）的力
        dx_home = self.target_x - self.x
        dy_home = self.target_y - self.y

        force_home = 0.06
        ax = dx_home * force_home
        ay = dy_home * force_home

        # 2. 手的交互力
        if hand_pos:
            hx, hy = hand_pos
            dx_hand = hx - self.x
            dy_hand = hy - self.y
            dist_hand = math.hypot(dx_hand, dy_hand)

            interaction_radius = 180
            if dist_hand < interaction_radius:
                angle = math.atan2(dy_hand, dx_hand)
                # 旋转力增强
                rotation_force = 2.0
                ax += math.cos(angle + math.pi / 2) * rotation_force
                ay += math.sin(angle + math.pi / 2) * rotation_force
                # 靠近手时稍微变大
                self.current_size = min(self.base_size * 1.5, 12)
            else:
                self.current_size = self.base_size
        else:
            self.current_size = self.base_size

        # 摩擦力
        friction = 0.88
        self.vx = (self.vx + ax) * friction
        self.vy = (self.vy + ay) * friction

        self.x += self.vx
        self.y += self.vy

        # 更新闪烁动画
        self.blink_phase += self.blink_speed

    def draw(self, surface):
        # 计算闪烁亮度系数
        blink_factor = (math.sin(self.blink_phase) + 1) / 2 * 0.3 + 0.7
        current_color = [int(c * blink_factor) for c in self.base_color]

        ix, iy = int(self.x), int(self.y)
        isize = int(self.current_size)

        # 1. 绘制主体底色圆
        pygame.draw.circle(surface, current_color, (ix, iy), isize)

        # 2. 绘制金属高光（在左上角画一个更亮、更小的圆）
        highlight_size = max(1, int(isize * 0.4))
        highlight_offset = int(isize * 0.3)
        pygame.draw.circle(surface, self.highlight_color,
                           (ix - highlight_offset, iy - highlight_offset),
                           highlight_size)


# --- 5. Setup Generation (生成设定) ---

def generate_tree_targets():
    """生成螺旋树的目标点"""
    targets = []
    tree_height = 500
    tree_top_y = 120

    for i in range(PARTICLE_COUNT):
        h_norm = i / PARTICLE_COUNT  # 0(顶) 到 1(底)

        # 半径随高度增加
        radius = 220 * h_norm

        # 螺旋角度
        angle = 18 * h_norm * 2 * math.pi

        tx = WIDTH // 2 + radius * math.cos(angle)
        ty = tree_top_y + h_norm * tree_height

        targets.append((tx, ty))

    # 树顶星的位置
    star_pos = (WIDTH // 2, tree_top_y - 20)

    return targets, star_pos


target_positions, star_target = generate_tree_targets()
particles = [Particle(tx, ty) for tx, ty in target_positions]

# 生成礼物盒
gifts = [GiftBox() for _ in range(8)]

# --- 6. Main Loop (主循环) ---
cap = cv2.VideoCapture(0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- CV Hand Tracking ---
    success, frame = cap.read()
    hand_pos = None
    if success:
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            landmark = results.multi_hand_landmarks[0].landmark[8]  # 食指指尖
            hand_x = int(landmark.x * WIDTH)
            hand_y = int(landmark.y * HEIGHT)
            hand_pos = (hand_x, hand_y)

    # --- Draw & Update ---
    screen.fill(BG_COLOR)  # 填充米黄色背景

    # 1. 画地面的礼物盒 (最底层)
    for gift in gifts:
        gift.draw(screen)

    # 2. 画粒子和丝带
    # 为了画丝带，我们需要在粒子更新位置之后进行
    particle_coords = []
    for p in particles:
        p.update(hand_pos)
        p.draw(screen)
        particle_coords.append((p.x, p.y))

    # 3. 绘制模拟丝带 (连接螺旋线上的部分点)
    # 每隔一定数量的点连接一下，形成缠绕感
    ribbon_step = 15
    for i in range(0, len(particle_coords) - ribbon_step, ribbon_step):
        p1 = particle_coords[i]
        p2 = particle_coords[i + ribbon_step]
        # 只连接距离不太远的点
        if math.hypot(p1[0] - p2[0], p1[1] - p2[1]) < 100:
            # 画一条半透明的金色粗线
            # 使用临时 surface 画透明线
            temp_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(temp_surf, (*GOLD, 80), p1, p2, 6)
            screen.blit(temp_surf, (0, 0))

    # 4. 画树顶五角星 (最高层)
    draw_star(screen, GOLD, star_target[0], star_target[1], 25)

    # 5. 画手的交互光晕 (改为暖色光以适应背景)
    if hand_pos:
        # 使用带alpha通道的圆圈
        s.fill((0, 0, 0, 0))  # 清空透明层
        pygame.draw.circle(s, (255, 220, 150, 100), hand_pos, 50)  # 半透明暖光
        screen.blit(s, (0, 0))

    pygame.display.flip()
    clock.tick(60)

cap.release()
pygame.quit()
'''
#装饰版本，我觉得礼盒和星星都是贴纸类似的，增加了放大缩小效果，但是还是不满意，摄像头灵敏度不高