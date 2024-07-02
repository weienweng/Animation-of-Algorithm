import pygame
import sys
import random

pygame.init()

WHITE, BLACK, GRAY, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0), (200, 200, 200), (255, 0, 0), (0, 255, 0), (0, 0, 255)

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sorting Algorithms Visualization")

BLOCK_WIDTH, BLOCK_HEIGHT, SPACING = 60, 60, 5

data = [random.randint(1, 99) for _ in range(15)]

class Block:
    def __init__(self, x, y, value):
        self.x, self.y, self.value = x, y, value
        self.color = GRAY
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, BLOCK_WIDTH, BLOCK_HEIGHT))
        pygame.draw.rect(surface, BLACK, (self.x, self.y, BLOCK_WIDTH, BLOCK_HEIGHT), 2)
        text = self.font.render(str(self.value), True, BLACK)
        text_rect = text.get_rect(center=(self.x + BLOCK_WIDTH // 2, self.y + BLOCK_HEIGHT // 2))
        surface.blit(text, text_rect)

    def move_to(self, new_x, new_y, steps=10):
        start_x, start_y = self.x, self.y
        for i in range(steps):
            self.x = start_x + (new_x - start_x) * i // steps
            self.y = start_y + (new_y - start_y) * i // steps
            draw_blocks()
            pygame.time.wait(5)
        self.x, self.y = new_x, new_y

blocks = [Block(i * (BLOCK_WIDTH + SPACING) + SPACING, HEIGHT // 2 - BLOCK_HEIGHT // 2, val) for i, val in enumerate(data)]

def draw_blocks():
    screen.fill(WHITE)
    for block in blocks:
        block.draw(screen)
    pygame.display.flip()

def exchange_sort():
    n = len(blocks)
    for i in range(n):
        for j in range(i+1, n):
            blocks[i].color, blocks[j].color = RED, GREEN
            draw_blocks()
            display_sort_title("Exchange Sort")
            pygame.time.wait(200)
            if blocks[i].value > blocks[j].value:
                blocks[i].color, blocks[j].color = GREEN, RED
                draw_blocks()
                display_sort_title("Exchange Sort")
                pygame.time.wait(100)
                x1, y1 = blocks[i].x, blocks[i].y
                x2, y2 = blocks[j].x, blocks[j].y
                blocks[i].move_to(x2, y1)
                blocks[j].move_to(x1, y2)
                blocks[i], blocks[j] = blocks[j], blocks[i]
            blocks[i].color = blocks[j].color = GRAY
    for block in blocks:
        block.color = BLUE
    draw_blocks()
    display_sort_title("Exchange Sort - Complete")

def bubble_sort():
    n = len(blocks)
    for i in range(n):
        for j in range(0, n-i-1):
            blocks[j].color, blocks[j+1].color = RED, GREEN
            draw_blocks()
            display_sort_title("Bubble Sort")
            pygame.time.wait(200)
            if blocks[j].value > blocks[j+1].value:
                blocks[j].color, blocks[j+1].color = GREEN, RED
                draw_blocks()
                display_sort_title("Bubble Sort")
                pygame.time.wait(100)
                x1, y1 = blocks[j].x, blocks[j].y
                x2, y2 = blocks[j+1].x, blocks[j+1].y
                blocks[j].move_to(x2, y1)
                blocks[j+1].move_to(x1, y2)
                blocks[j], blocks[j+1] = blocks[j+1], blocks[j]
            blocks[j].color = blocks[j+1].color = GRAY
    for block in blocks:
        block.color = BLUE
    draw_blocks()
    display_sort_title("Bubble Sort - Complete")

def selection_sort():
    n = len(blocks)
    for i in range(n):
        min_idx = i
        blocks[i].color = RED
        for j in range(i+1, n):
            blocks[j].color = GREEN
            draw_blocks()
            display_sort_title("Selection Sort")
            pygame.time.wait(200)
            if blocks[j].value < blocks[min_idx].value:
                blocks[min_idx].color = GRAY
                min_idx = j
                blocks[min_idx].color = RED
            else:
                blocks[j].color = GRAY
        if min_idx != i:
            blocks[i].color, blocks[min_idx].color = GREEN, RED
            draw_blocks()
            display_sort_title("Selection Sort")
            pygame.time.wait(100)
            x1, y1 = blocks[i].x, blocks[i].y
            x2, y2 = blocks[min_idx].x, blocks[min_idx].y
            blocks[i].move_to(x2, y1)
            blocks[min_idx].move_to(x1, y2)
            blocks[i], blocks[min_idx] = blocks[min_idx], blocks[i]
        blocks[i].color = BLUE
    draw_blocks()
    display_sort_title("Selection Sort - Complete")

def resize_blocks():
    global BLOCK_WIDTH, BLOCK_HEIGHT, SPACING
    BLOCK_WIDTH = min(60, (WIDTH - SPACING * (len(blocks) + 1)) // len(blocks))
    BLOCK_HEIGHT = min(60, HEIGHT // 3)
    SPACING = 5
    for i, block in enumerate(blocks):
        block.x = i * (BLOCK_WIDTH + SPACING) + SPACING
        block.y = HEIGHT // 2 - BLOCK_HEIGHT // 2

def shuffle_blocks():
    global blocks
    random.shuffle(blocks)
    for i, block in enumerate(blocks):
        block.x = i * (BLOCK_WIDTH + SPACING) + SPACING
        block.y = HEIGHT // 2 - BLOCK_HEIGHT // 2
        block.color = GRAY
    draw_blocks()

def display_sort_title(title):
    title_font = pygame.font.Font(None, 48)
    title_surface = title_font.render(title, True, BLACK)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title_surface, title_rect)
    pygame.display.flip()

running = True
sorting = False
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
exchange_text = font.render("Press 'E' for Exchange Sort", True, BLACK)
bubble_text = font.render("Press 'B' for Bubble Sort", True, BLACK)
selection_text = font.render("Press 'S' for Selection Sort", True, BLACK)
reset_text = font.render("Press 'R' to Reset", True, BLACK)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            resize_blocks()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and not sorting:
                shuffle_blocks()
                sorting = True
                exchange_sort()
                sorting = False
            elif event.key == pygame.K_b and not sorting:
                shuffle_blocks()
                sorting = True
                bubble_sort()
                sorting = False
            elif event.key == pygame.K_s and not sorting:
                shuffle_blocks()
                sorting = True
                selection_sort()
                sorting = False
            elif event.key == pygame.K_r:
                sorting = False
                data = [random.randint(1, 99) for _ in range(15)]
                blocks = [Block(i * (BLOCK_WIDTH + SPACING) + SPACING, HEIGHT // 2 - BLOCK_HEIGHT // 2, val) for i, val in enumerate(data)]
                resize_blocks()

    screen.fill(WHITE)
    for block in blocks:
        block.draw(screen)
    screen.blit(exchange_text, (10, 10))
    screen.blit(bubble_text, (10, 50))
    screen.blit(selection_text, (10, 90))
    screen.blit(reset_text, (10, 130))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
