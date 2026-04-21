from random import randint, choice

class MazeGenerator:

    def __init__(self, width: int, height: int, start: tuple[int, int],
                 end: tuple[int, int], output_file: str, maze_type: bool,
                 num_42_cells: list[tuple[int, int]]) -> None:

        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.output_file = output_file
        self.maze_type = maze_type
        self.walls_config = self.init_walls()
        self.num_42_cells = num_42_cells

    def init_walls(self):

        grid = dict()
        for i in range(self.height):
            for j in range(self.width):
                grid[(j, i)] = [1, 1, 1, 1]
        return (grid)

    def get_possible_moves1(self, curr_coordinate: tuple[int, int],
                            taken_cells: list[tuple[int, int]]) -> list[int]:

        x, y = curr_coordinate
        moves_dict = {0: (x, y - 1), 1: (x + 1, y), 2: (x, y + 1), 3: (x - 1, y)}
        possible_moves = []
        for move in moves_dict.values():
            x, y = move
            if (x >= 0 and x < self.width and y >= 0 and y < self.height
                    and move not in taken_cells):
                possible_moves.append(move)
        possible_moves_dict = {num: move for num, move in moves_dict.items() if
                               move in possible_moves}
        return (possible_moves_dict)

    def create_maze(self) -> None:

        curr_cell = self.start
        taken_cells = self.num_42_cells.copy()
        taken_cells.append(curr_cell)
        total_cells = self.height * self.width
        while len(taken_cells) != total_cells:
            possible_moves_dict = self.get_possible_moves1(curr_cell, taken_cells)
            while not possible_moves_dict:
                curr_index = taken_cells.index(curr_cell)
                curr_cell = taken_cells[curr_index - 1]
                possible_moves_dict = self.get_possible_moves1(curr_cell, taken_cells)
            move_index = choice(list(possible_moves_dict.keys()))
            self.walls_config[curr_cell][move_index] = 0
            curr_cell = possible_moves_dict[move_index]
            self.walls_config[curr_cell][(move_index + 2) % 4] = 0
            taken_cells.append(curr_cell)

    def get_possible_moves2(self, curr_cell: tuple[int, int],
                            taken_cells: list[tuple[int, int]]) -> list[tuple[int, int]]:

        up, right, down, left = self.walls_config[curr_cell]
        x, y = curr_cell
        cell_up = (x, y - 1)
        cell_right = (x + 1, y)
        cell_down = (x, y + 1)
        cell_left = (x - 1, y)
        possible_moves = []
        if not up and cell_up not in taken_cells:
            possible_moves.append(cell_up)
        if not right and cell_right not in taken_cells:
            possible_moves.append(cell_right)
        if not down and cell_down not in taken_cells:
            possible_moves.append(cell_down)
        if not left and cell_left not in taken_cells:
            possible_moves.append(cell_left)
        return (possible_moves)

    def solve_maze(self, start_cell: tuple[int, int], end_cell: tuple[int, int]) -> None:

        curr_cell = start_cell
        best_path = [curr_cell]
        cell_paths = dict()
        while curr_cell != end_cell:
            possible_moves = self.get_possible_moves2(curr_cell, best_path)
            if not possible_moves:
                best_path.pop()
                curr_cell = best_path[-1]
                possible_moves = cell_paths[curr_cell]
                while not possible_moves:
                    best_path.pop()
                    curr_cell = best_path[-1]
                    possible_moves = cell_paths[curr_cell]
            next_cell = possible_moves[-1]
            possible_moves.pop()
            cell_paths[curr_cell] = possible_moves
            best_path.append(next_cell)
            curr_cell = next_cell
        return (best_path)

    def write_output(self) -> None:

        file = open(self.output_file, 'w')
        for cell, walls in self.walls_config.items():
            x, y = cell
            up, right, down, left = walls
            number = up + right * 2 + down * 4 + left * 8
            if number < 10:
                file.write(str(number))
            else:
                leftover = number - 10
                file.write(chr(ord('A') + leftover))
            if x == self.width - 1:
                file.write("\n")
        file.close()
