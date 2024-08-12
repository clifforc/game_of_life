from time import sleep

import pygame
import numpy as np
from scipy.signal import convolve2d

import constants as c

# Set pygame window name
pygame.display.set_caption('Game of life')


def update(screen, cells, size, show_progress=False):
    updated_cells = cells_life_logic(cells)
    for row, col in np.ndindex(cells.shape):
        color = c.COLOR_BACKGROUND if cells[row, col] == 0 \
            else c.COLOR_ALIVE_CELLS
        if show_progress:
            if updated_cells[row, col] == 0 and cells[row, col] == 1:
                color = c.COLOR_BACKGROUND
            elif updated_cells[row, col] == 1 and cells[row, col] == 0:
                color = c.COLOR_ALIVE_CELLS
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


def display_rules(screen):
    default_font = pygame.font.Font(None, 21)
    rules_text = ['HOTKEYS',
                  'Press "Spacebar" to pause',
                  'Press "c" to reset field',
                  'Press "q" to quit game',]
    text_offset = 30
    for rule in rules_text:
        text = default_font.render(rule, True, c.COLOR_TEXT)
        screen.blit(text, (c.TEXT_MARGIN, text_offset))
        text_offset += 40


def display_stats(screen, count_alive, max_alive):
    default_font = pygame.font.Font(None, 21)
    stats_text = ['GAME STATS',
                  f'Alive cells: {count_alive}',
                  f'Max alive cells: {max_alive}']
    text_offset = 220
    for stat in stats_text:
        text = default_font.render(stat, True, c.COLOR_TEXT)
        screen.blit(text, (c.TEXT_MARGIN, text_offset))
        text_offset += 40


def calculate_and_display_stats(screen, cells, max_alive):
    count_alive = np.count_nonzero(cells)
    if max_alive < count_alive:
        max_alive = count_alive
    display_stats(screen, count_alive, max_alive)
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


def game_init():
    pygame.init()
    screen = pygame.display.set_mode(c.SCREEN_SIZE)
    cells = np.zeros(
        (c.SCREEN_HEIGHT // c.CELLS_SIZE, c.ACTIVE_WIDTH // c.CELLS_SIZE)
    )
    screen.fill(c.COLOR_GRID)
    display_rules(screen)
    max_alive = 0
    calculate_and_display_stats(screen, cells, max_alive)
    update(screen, cells, c.CELLS_SIZE)
    pygame.display.flip()
    pygame.display.update()
    running = False
    game_loop(running, screen, cells, max_alive)


def set_cells_via_mouse(cells, screen):
    pos = pygame.mouse.get_pos()
    if (pos[0] // c.CELLS_SIZE) < c.ACTIVE_WIDTH // c.CELLS_SIZE:
        cells[pos[1] // c.CELLS_SIZE, pos[0] // c.CELLS_SIZE] = 1
    update_screen(screen, cells, c.CELLS_SIZE)


def game_loop(running, screen, cells, max_alive):
    while True:
        for event in pygame.event.get():
            running, flag = handle_keys(
                event, running, screen, cells, c.CELLS_SIZE
            )
            if not flag:
                return
            if pygame.mouse.get_pressed()[0]:
                set_cells_via_mouse(cells, screen)
        screen.fill(c.COLOR_GRID)
        display_rules(screen)
        max_alive = calculate_and_display_stats(screen, cells, max_alive)
        if running:
            cells = update(screen, cells, c.CELLS_SIZE, show_progress=True)
            pygame.display.update()
            sleep(0.02)
        sleep(0.001)
