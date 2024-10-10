import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.g = float('inf')  # Cost from start to this node
        self.h = float('inf')  # Heuristic cost from this node to end
        self.f = float('inf')  # Total cost
        self.neighbors = []
        self.parent = None
        self.wall = False
        self.visited = False

    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.wall

    def make_wall(self):
        self.wall = True

    def make_open(self):
        self.wall = False

    def make_closed(self):
        self.visited = True

    def update_neighbors(self, grid):
        self.neighbors = []
        # Check the four possible directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for direction in directions:
            new_row, new_col = self.row + direction[0], self.col + direction[1]
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                if not grid[new_row][new_col].is_wall():
                    self.neighbors.append(grid[new_row][new_col])

    def heuristic(self, end):
        return abs(self.row - end.row) + abs(self.col - end.col)

def reconstruct_path(current):
    path = []
    while current:
        path.append(current)
        current = current.parent
    return path[::-1]  # Return reversed path

def a_star_algorithm(draw, grid, start, end):
    open_set = [start]
    start.g = 0
    start.h = start.heuristic(end)
    start.f = start.h

    while open_set:
        open_set.sort(key=lambda node: node.f)
        current = open_set.pop(0)

        if current == end:
            return reconstruct_path(current)

        for neighbor in current.neighbors:
            if neighbor.visited:
                continue
            temp_g = current.g + 1  # Assuming each move has a cost of 1

            if temp_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = temp_g
                neighbor.h = neighbor.heuristic(end)
                neighbor.f = neighbor.g + neighbor.h

                if neighbor not in open_set:
                    open_set.append(neighbor)

        current.make_closed()
        draw()

    return []

def make_grid():
    return [[Node(row, col) for col in range(COLS)] for row in range(ROWS)]

def draw_grid(win, grid):
    for row in grid:
        for node in row:
            color = WHITE
            if node.is_wall():
                color = BLACK
            if node.visited:
                color = GREY
            pygame.draw.rect(win, color, (node.col * GRID_SIZE, node.row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(win, BLUE, (node.col * GRID_SIZE, node.row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def draw(win, grid, path=[]):
    win.fill(BLUE)
    draw_grid(win, grid)

    for node in path:
        pygame.draw.rect(win, GREEN, (node.col * GRID_SIZE, node.row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Pathfinding Algorithm")
    clock = pygame.time.Clock()
    grid = make_grid()

    start = None
    end = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:  # Left click to set start and end
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // GRID_SIZE, pos[0] // GRID_SIZE
                if not start:
                    start = grid[row][col]
                elif not end:
                    end = grid[row][col]
                else:
                    grid[row][col].make_wall()

            if pygame.mouse.get_pressed()[2]:  # Right click to reset walls
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // GRID_SIZE, pos[0] // GRID_SIZE
                grid[row][col].make_open()
                if grid[row][col] == start:
                    start = None
                elif grid[row][col] == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    path = a_star_algorithm(lambda: draw(win, grid, path), grid, start, end)
                    draw(win, grid, path)

                if event.key == pygame.K_r:  # Press 'R' to reset the grid
                    grid = make_grid()
                    start = None
                    end = None

        draw(win, grid)

if __name__ == "__main__":
    main()
