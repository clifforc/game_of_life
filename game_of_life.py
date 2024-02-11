from time import sleep
import pygame
import numpy as np
from scipy.signal import convolve2d

# Set pygame window name
pygame.display.set_caption('Game of life')

# Define color constants
COLOR_BACKGROUND = (0, 0, 0)
COLOR_GRID = (40, 40, 40)
COLOR_ALIVE_CELLS = (255, 255, 255)

# Define screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
ACTIVE_WIDTH = 600

# Define cells size
CELLS_SIZE = 5

# Text margin
TEXT_MARGIN = SCREEN_WIDTH - (SCREEN_WIDTH - ACTIVE_WIDTH - 5)


def update(screen, cells, size, show_progress=False):
    updated_cells = cells_life_logic(cells)
    for row, col in np.ndindex(cells.shape):
        color = COLOR_BACKGROUND if cells[row, col] == 0 else COLOR_ALIVE_CELLS
        if show_progress:
            if updated_cells[row, col] == 0 and cells[row, col] == 1:
                color = COLOR_BACKGROUND
            elif updated_cells[row, col] == 1 and cells[row, col] == 0:
                color = COLOR_ALIVE_CELLS
        pygame.draw.rect(screen, color, (col * size, row * size,
                                         size - 1, size - 1))
    return updated_cells


def cells_life_logic(cells):
    mask_arr = np.array([[1, 1, 1],
                         [1, 0, 1],
                         [1, 1, 1]])
    alive = convolve2d(cells, mask_arr, mode='same', boundary='wrap')
    updated_cells = np.zeros_like(cells)
    updated_cells[(cells == 1) & ((alive < 2) | (alive > 3))] = 0
    updated_cells[(cells == 1) & ((alive == 2) | (alive == 3))] = 1
    updated_cells[(cells == 0) & (alive == 3)] = 1
    return updated_cells


def rules(screen):
    default_font = pygame.font.Font(None, 21)
    rules_text = ['HOTKEYS',
                  'Press "Spacebar" to pause',
                  'Press "c" to reset field',
                  'Press "q" to quit game']
    text_offset = 30
    for rule in rules_text:
        text = default_font.render(rule, True, COLOR_ALIVE_CELLS)
        screen.blit(text, (TEXT_MARGIN, text_offset))
        text_offset += 40


def stats(screen, cells, max_alive):
    default_font = pygame.font.Font(None, 21)
    count_alive = np.count_nonzero(cells)
    if max_alive < count_alive:
        max_alive = count_alive
    stats_text = ['GAME STATS',
                  f'Alive cells: {count_alive}',
                  f'Max alive cells: {max_alive}']
    text_offset = 220
    for stat in stats_text:
        text = default_font.render(stat, True, COLOR_ALIVE_CELLS)
        screen.blit(text, (TEXT_MARGIN, text_offset))
        text_offset += 40
    return max_alive


def handle_keys(event, running, screen, cells, size):
    if event.type == pygame.QUIT:
        pygame.quit()
        return running, False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            running = not running
            update_screen(screen, cells, size)
        if event.key == pygame.K_c:
            running = False
            cells.fill(0)
            update_screen(screen, cells, size)
        if event.key == pygame.K_q:
            pygame.quit()
            return running, False
    return running, True


def update_screen(screen, cells, size):
    update(screen, cells, size)
    pygame.display.update()


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    cells = np.zeros((SCREEN_HEIGHT // CELLS_SIZE, ACTIVE_WIDTH // CELLS_SIZE))
    screen.fill(COLOR_GRID)
    rules(screen)
    max_alive = 0
    stats(screen, cells, max_alive)
    update(screen, cells, CELLS_SIZE)
    pygame.display.flip()
    pygame.display.update()
    running = False

    while True:
        for event in pygame.event.get():
            running, flag = handle_keys(event, running, screen,
                                        cells, CELLS_SIZE)
            if not flag:
                return
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // CELLS_SIZE, pos[0] // CELLS_SIZE] = 1
                update_screen(screen, cells, CELLS_SIZE)
        screen.fill(COLOR_GRID)
        rules(screen)
        max_alive = stats(screen, cells, max_alive)
        if running:
            cells = update(screen, cells, CELLS_SIZE, show_progress=True)
            pygame.display.update()
            sleep(0.02)
        sleep(0.001)


if __name__ == "__main__":
    main()
