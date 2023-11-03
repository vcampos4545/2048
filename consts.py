WINDOW_WIDTH = 400
WINDOW_HEIGHT = 1.5 * WINDOW_WIDTH

SIDE_MARGIN = WINDOW_WIDTH // 10
GAME_WIDTH = WINDOW_WIDTH - 2*SIDE_MARGIN #Account for side margins on BOTH sides
TOP_MARGIN = WINDOW_HEIGHT // 3
GAME_WINDOW = (SIDE_MARGIN, TOP_MARGIN, GAME_WIDTH, GAME_WIDTH)

BLOCK_WIDTH = GAME_WIDTH // 4
BLOCK_MARGIN = GAME_WIDTH // 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_COLOR_1 = (119, 110, 101)
TEXT_COLOR_2 = (255, 255, 255)

BG_CREAM = (251,248,239)
BG_GREY = (187,173,160)
EMPTY_GREY = (204,192,179)
BLOCK_COLORS = {
    "2" : (238,228,218),
    "4" : (237,224,200),
    "8" : (242,177,121),
    "16" : (245,149,99),
    "32" : (246,124,95),
    "64" : (246,94,59),
    "128" : (237,207,114),
    "256" : (237,204,97),
    "512" : (237,200,80),
    "1024" : (237,197,63),
    "2048" : (237,194,46)
}