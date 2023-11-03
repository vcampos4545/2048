import pygame
pygame.init()
import numpy as np
from consts import *

class Game:
    def __init__(self, initial_grid=None):
        self.w = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('2048')

        self.score = 0
        self.best = 0 #TODO: Get best score from saved text file
        self.moves = 0

        if not initial_grid:
            self.new_game()
        else:
            self.grid = initial_grid

    
    def new_game(self):
        """
        [new_game] resets the game state to a new game
        """
        self.grid = np.zeros((4, 4))
        for _ in range(2):
            self.spawn_block()
        

    def slide(self, arr, dir):
        """
        [slide] slides and combines the numbers in [arr] in the direction
        [dir] with the following rules:
        1. if dir is 1, then slide and combine numbers to the left
        2. if dir is -1, slide and combine numbers to the right
        3. numbers can be combined only if they are slid into a block with the same
        value (i.e. 2 -> 2 becomes 4, 4->4 becomes 8, 2->4 does not combine)
        4. Numbers can only be combined once in a slide (4->4->8 is 4->8 not 16)
        5. Numbers are slide such that no gaps exist in the row and all numbers have been slide
        or combined

        Returns:
            np.array: the slid and combined array
        """
        if dir == -1:
            temp = np.flip(np.copy(arr))
        else:
            temp = np.copy(arr)
        #For each element (after the 0th)
        combined = [False]*len(temp) #tracks which positions have been combined
        for i in range(1, len(temp)):
            
            if temp[i] == 0: continue
            
            #Finds next spot with next nonzero or 0th index
            idx = i-1
            while idx > 0 and temp[idx] == 0:
                idx -= 1
            
            if temp[idx] != 0 and temp[idx] != temp[i]:
                idx += 1
            
            if idx == i: continue

            if temp[idx] == temp[i] and not combined[idx]:
                #then combine
                temp[idx] = temp[idx] * 2
                temp[i] = 0
                combined[idx] = True
                self.score += temp[idx] * 2
            elif temp[idx] == 0:
                #Slide number
                temp[idx] = temp[i]
                temp[i] = 0

        return np.flip(temp) if dir == -1 else temp


    def shift_grid(self, dir1, dir):
        """
        [shift_grid] shifts self.grid in direction [dir]
        """
        if dir1 == "UP" or dir1 == "DOWN":
            for i in range(self.grid.shape[0]):
                self.grid[i,:] = self.slide(self.grid[i,:], dir)
        elif dir1 == "RIGHT" or dir1 == "LEFT":
            for j in range(self.grid.shape[1]):
                self.grid[:,j] = self.slide(self.grid[:,j], dir)

    def spawn_block(self):
        """
        [spawn_block] spawns a randomly chosen number in an open block
        spot.  

        Returns:
            int: -1: no possible spawn locations, 0: successful
        """

        #Generate random block value
        val = np.random.choice([2, 4])

        #get list of possible spawn locations
        coords = []
        for i in range(4):
            for j in range(4):
                if self.grid[i, j] == 0:
                    coords.append(f'{i} {j}')
        
        #Check no spawn locations
        if len(coords) == 0:
            return -1
        
        #Randomly choose spawn location
        i, j = np.random.choice(coords).split(" ")
        #Update grid
        self.grid[int(i), int(j)] = val

        return 0

    def draw_text(self, text, text_color, font_size, center_x, center_y):
        """
        [draw_text] is a helper function that will draw [text] to the 
        pygame screen with given parameters
        """
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text = font.render(text, True, text_color)
        textRect = text.get_rect()
        textRect.center = (center_x, center_y)
        self.w.blit(text, textRect)

    def draw_header(self):
        """
        [draw_header] draws the header of the game to the pygame window. 
        This includes the current and best scores, text information, and
        the new game button
        """
        #Draw 2048
        self.draw_text("2048", TEXT_COLOR_1, 50, 100, 50)

        #Draw score block
        pygame.draw.rect(self.w, BG_GREY, (200, 20, 75, 50))
        self.draw_text("Score", TEXT_COLOR_2, 12, 237, 30)
        self.draw_text(str(int(self.score)), TEXT_COLOR_2, 25, 237, 53)

        #Drw best block
        pygame.draw.rect(self.w, BG_GREY, (290, 20, 75, 50))
        self.draw_text("Best", TEXT_COLOR_2, 12, 327, 30)
        self.draw_text(str(int(self.score)), TEXT_COLOR_2, 25, 327, 53)

        #TODO: Draw New Game button
    
    def draw_grid(self):
        """
        [draw_grid] draws the game grid to the pygame window
        """
        #Draw grid background
        pygame.draw.rect(self.w, BG_GREY, GAME_WINDOW)
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                n = self.grid[i, j]
                x = GAME_WINDOW[0] + j * BLOCK_WIDTH
                y = GAME_WINDOW[1] + i * BLOCK_WIDTH

                
                #Draw block background
                block_color = EMPTY_GREY if n == 0 else BLOCK_COLORS[str(int(n))]
                pygame.draw.rect(self.w, block_color, (x + BLOCK_MARGIN, 
                                                    y + BLOCK_MARGIN, 
                                                    BLOCK_WIDTH-2*BLOCK_MARGIN, 
                                                    BLOCK_WIDTH-2*BLOCK_MARGIN))
                
                if n != 0:
                    #Draw number in block
                    text_color = TEXT_COLOR_1 if n < 8 else TEXT_COLOR_2
                    text = self.font.render(str(int(self.grid[i, j])), True, text_color)
                    textRect = text.get_rect()
                    textRect.center = (x + BLOCK_WIDTH // 2, y + BLOCK_WIDTH // 2)
                    self.w.blit(text, textRect)

    def run(self):
        """
        Main game loop
        """

        while True:
            ##############################################################
            #                    Update game state
            ##############################################################
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif e.type == pygame.KEYDOWN:
                    grid_before = self.grid
                    
                    if e.key == pygame.K_LEFT:
                        self.shift_grid("LEFT", dir=1)
                    elif e.key == pygame.K_RIGHT:
                        self.shift_grid("RIGHT", dir=-1)
                    elif e.key == pygame.K_DOWN:
                        self.shift_grid("DOWN", dir=-1)
                    elif e.key == pygame.K_UP:
                        self.shift_grid("UP", dir=1)
                    self.moves += 1

                    grid_after = self.grid

                    #TODO: Fix
                    # if not np.all(grid_after == grid_before):
                    self.spawn_block()

            ##############################################################
            #                     Draw to pygame gui
            ##############################################################
            
            #Fill background
            self.w.fill(BG_CREAM)

            #Draw Game information
            self.draw_header()
            
            #Draw game grid
            self.draw_grid()

            #Update screen
            pygame.display.update()