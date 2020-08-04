'''
              Bullseye
A* Path Finding Visualizer Using Pygame
'''
import pygame, os
from queue import PriorityQueue

#window
W_Width = 750
WIN = pygame.display.set_mode((W_Width, W_Width))
pygame.display.set_caption("Bullseye")

TOTAL_ROWS = 30
C_WIDTH = W_Width//TOTAL_ROWS
PATH_FOUND = 0
CLOCK = pygame.time.Clock()
Arial = os.path.join("font", "arial.ttf")

#font
pygame.font.init()

#colours
BARRIER = (12, 53, 71)
PATH = (255, 254, 106)
START = (255, 255, 181)
FADE_ICON = (161, 132,177)
ICON = (68, 8, 99)
END = (255, 255, 182)
CLOSED = (64, 206, 255)
OPEN = (64, 206, 227)
SEMI_OPEN = (64, 227, 183)
UNVISITED = (255, 255, 255)
LINE = (175, 216, 248)

class Cube :
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width + 1
        self.y = col * width + 1
        self.width = width - 1
        self.total_rows = total_rows
        self.neighbors = []
        self.size = 0
        self.name = "unvisited"

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.name == "closed"

    def is_open(self):
        return self.name == "open"

    def is_barrier(self):
        return self.name == "barrier"

    def is_start(self):
        return self.name == "start"

    def is_end(self):
        return self.name == "end"

    def reset(self):
        self.name = "unvisited"

    def make_closed(self):
        self.name = "closed"

    def make_open(self):
        self.name = "open"

    def make_barrier(self):
        self.name = "barrier"

    def make_start(self):
        self.name = "start"

    def make_end(self):
        self.name = "end"

    def make_path(self):
        self.name = "path"

    def draw(self, win):
        global PATH_FOUND

        #draw each cube
        if self.name == "unvisited" :
            pygame.draw.rect(win, UNVISITED, (self.x, self.y, self.width, self.width))
        if self.name == "start" :
            if PATH_FOUND >= 0.5:
                self.size += 1
                if self.size <= C_WIDTH:
                    pygame.draw.rect(win, START, (
                    self.x + C_WIDTH // 2 - self.size // 2, self.y + C_WIDTH // 2 - self.size // 2, self.size,
                    self.size))
                    FONT = pygame.font.Font(Arial, round(self.size * 1.2), bold=True)
                    icon = FONT.render("►", 1, FADE_ICON)
                    center = icon.get_rect(center=(self.x+self.width//2, self.y+self.width//2))
                    WIN.blit(icon, center)
                else :
                    pygame.draw.rect(win, START, (self.x, self.y, C_WIDTH, C_WIDTH))
                    FONT = pygame.font.Font(Arial, round(C_WIDTH * 1.2), bold=True)
                    icon = FONT.render("►", 1, FADE_ICON)
                    center = icon.get_rect(center=(self.x + self.width // 2, self.y + self.width // 2))
                    WIN.blit(icon, center)
            else:
                FONT = pygame.font.Font(Arial, round(C_WIDTH * 1.2), bold=True)
                icon = FONT.render("►", 1, ICON)
                center = icon.get_rect(center=(self.x + self.width // 2, self.y + self.width // 2))
                WIN.blit(icon, center)
        if self.name == "end" :
            SYMBOL = "ʘ"
            if PATH_FOUND == 1:
                self.size += 1
                for neighbor in self.neighbors:
                    if neighbor.name == "path" and neighbor.y > self.y:
                        SYMBOL = "▲"
                    elif neighbor.name == "path" and neighbor.y < self.y:
                        SYMBOL = "▼"
                    elif neighbor.name == "path" and neighbor.x < self.x:
                        SYMBOL = "►"
                    elif neighbor.name == "path" and neighbor.x > self.x:
                        SYMBOL = "◄"
                if self.size <= C_WIDTH:
                    pygame.draw.rect(win, PATH, (
                        self.x + C_WIDTH // 2 - self.size // 2, self.y + C_WIDTH // 2 - self.size // 2, self.size,
                        self.size))
                    FONT = pygame.font.Font(Arial, round(self.size * 1.2), bold=True)
                    icon = FONT.render(SYMBOL, 1, ICON)
                    center = icon.get_rect(center=(self.x + self.width // 2, self.y + self.width // 2))
                    WIN.blit(icon, center)
                else:
                    pygame.draw.rect(win, PATH, (self.x, self.y, C_WIDTH, C_WIDTH))
                    FONT = pygame.font.Font(Arial, round(C_WIDTH * 1.2), bold=True)
                    icon = FONT.render(SYMBOL, 1, ICON)
                    center = icon.get_rect(center=(self.x + self.width // 2, self.y + self.width // 2))
                    WIN.blit(icon, center)
            else :
                FONT = pygame.font.Font(Arial, round(C_WIDTH * 1.2), bold=True)
                icon = FONT.render(SYMBOL, 1, ICON)
                center = icon.get_rect(center=(self.x + self.width // 2, self.y + self.width // 2))
                WIN.blit(icon, center)
        if self.name == "barrier" :
            self.size += 1
            if self.size<= C_WIDTH :
                pygame.draw.rect(win, BARRIER, (self.x + C_WIDTH // 2 - self.size // 2 , self.y + C_WIDTH // 2 - self.size // 2, self.size, self.size))
            else :
                pygame.draw.rect(win, BARRIER, (self.x, self.y, C_WIDTH, C_WIDTH))
        if self.name == "path" :
            self.size += 1
            if self.size <= C_WIDTH:
                pygame.draw.rect(win, PATH, (self.x, self.y, C_WIDTH, C_WIDTH))
            else:
                pygame.draw.rect(win, PATH, (self.x, self.y, C_WIDTH, C_WIDTH))
        if self.name == "closed":
            self.size += 1
            if self.size <= C_WIDTH :
                pygame.draw.rect(win, CLOSED, (
                    self.x + C_WIDTH // 2 - self.size // 2, self.y + C_WIDTH // 2 - self.size // 2, self.size,
                    self.size))
            else:
                pygame.draw.rect(win, CLOSED, (self.x, self.y, C_WIDTH - 1, C_WIDTH - 1))
        if self.name == "open" :
            self.size += 1
            rect_color = CLOSED

            if self.size <= C_WIDTH:
                if self.size >= C_WIDTH / 2:
                    rect_color = SEMI_OPEN
                pygame.draw.rect(win, rect_color, (
                    self.x + C_WIDTH // 2 - self.size // 2, self.y + C_WIDTH // 2 - self.size // 2, self.size,
                    self.size))
            else:
                rect_color = OPEN
                pygame.draw.rect(win, rect_color, (self.x, self.y, C_WIDTH - 1, C_WIDTH - 1))

    def update_neigbors(self, grid):
        self.neighbors = []

        if (self.row > 0 and not grid[self.row - 1][self.col].is_barrier()) : #Upper neighbor
            self.neighbors.append(grid[self.row - 1][self.col])

        if (self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier()) : #Bottom neighbor
            self.neighbors.append(grid[self.row + 1][self.col])

        if (self.col > 0 and not grid[self.row][self.col - 1].is_barrier()) : #Left neighbor
            self.neighbors.append(grid[self.row][self.col - 1])

        if (self.col < self.total_rows -1 and not grid[self.row][self.col + 1].is_barrier()) : #Right neighbor
            self.neighbors.append(grid[self.row][self.col + 1])

def h_score(start, end) : #heuristic function to find absolute distance between start and end cube
    x1, y1 = start
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)

def draw_path(came_from , current, draw) :
    global PATH_FOUND
    PATH_FOUND = 0.5
    path_list = []
    #backtrack current cube
    while current in came_from :
        current = came_from[current]
        path_list.insert(0, current)
    for cube in path_list[1:] :
        CLOCK.tick(20)
        cube.make_path()
        draw()
    PATH_FOUND = 1

def algorithm(draw, grid, start, end) :
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_track = {start}
    came_from = {}
    g_score = {cube : float('inf') for row in grid for cube in row } #distance between start and current cube
    g_score[start] = 0
    f_score = {cube : float('inf') for row in grid for cube in row } #addition of g_score and h_score
    f_score[start] = h_score(start.get_pos(), end.get_pos())

    while not open_set.empty():

        # quit pygame if clicked on [X]
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                quit()

        current = open_set.get()[2]  #get current cube
        open_set_track.remove(current)

        if current == end :  #if end cube found then exit
            draw_path(came_from, end, draw) #draw found path
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbors :
            tenative_g_score = g_score[current] + 1

            if tenative_g_score < g_score[neighbour] :
                came_from[neighbour] = current
                g_score[neighbour] = tenative_g_score
                f_score[neighbour] = tenative_g_score + h_score(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set_track :
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_track.add(neighbour)
                    if neighbour.name != "end":
                        neighbour.make_closed()

        CLOCK.tick(30)
        draw()

        if current != start :
            current.make_open()
    return False

def make_grid(total_rows, w_width) :
    grid = []

    #make grid of cubes
    for i in range(total_rows) :
        grid.append([])
        for j in range(total_rows):
            cube = Cube(i, j, C_WIDTH, total_rows)
            grid[i].append(cube)

    return grid

def draw_grid_lines(win, total_rows, w_width):

    #draw horizontal grid lines
    for i in range(total_rows):
        pygame.draw.line(win, LINE, (0, i * C_WIDTH), (w_width, i * C_WIDTH))

    #draw vertical grid lines
    for j in range(total_rows):
        pygame.draw.line(win, LINE, (j * C_WIDTH, 0), (j * C_WIDTH, w_width))

def draw(win, grid, total_rows, w_width):
    win.fill(UNVISITED)

    draw_grid_lines(win, total_rows, w_width)
    #draw/update each cube in the grid
    for row in grid :
        for cube in row :
            cube.draw(win)

    pygame.display.update()

def get_cube_pos(pos, w_width, total_rows):
    x, y = pos #get current mouse position on screen
    row = x // C_WIDTH
    col = y // C_WIDTH
    return row, col

def main(win, w_width, total_rows) :
    running = True
    start = None
    end = None
    grid = make_grid(total_rows, w_width)
    global PATH_FOUND

    while running :
        draw(win, grid, total_rows, w_width)

        # quit pygame if clicked on [X]
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
                break

            if pygame.mouse.get_pressed()[0] : #Left_click
                pos = pygame.mouse.get_pos()
                row , col = get_cube_pos(pos, w_width, total_rows)
                cube = grid[row][col]
                if not start and cube!=end:
                    cube.make_start()
                    start = cube
                elif not end and cube!=start:
                    cube.make_end()
                    end = cube
                elif start != cube and end != cube :
                    cube.make_barrier()

            elif pygame.mouse.get_pressed()[2] : #Right_click
                pos = pygame.mouse.get_pos()
                row , col = get_cube_pos(pos, w_width, total_rows)
                cube = grid[row][col]
                cube.size = 0
                PATH_FOUND = 0
                if cube.is_start() :
                    start = None
                    cube.reset()
                elif cube.is_end():
                    end = None
                    cube.reset()
                elif cube.is_barrier() :
                    cube.reset()

            #check if space is clicked
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE and start and end : #visualize on key press

                    #update neighbors
                    for row in grid :
                        for cube in row :
                            cube.update_neigbors(grid)
                            if cube.name == "open" or cube.name == "closed" or cube.name == "path" :
                                cube.reset()
                                cube.size = 0
                                PATH_FOUND = 0

                    #run the algorithm
                    algorithm(lambda : draw(win, grid, total_rows, w_width), grid, start, end)

                if event.key == pygame.K_c : #reset screen on key press
                    start = None
                    end = None
                    grid = make_grid(total_rows, w_width)
                    PATH_FOUND = 0
    pygame.quit()
    quit()

main(WIN, W_Width, TOTAL_ROWS)