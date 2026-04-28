import random


class MazeGenerator:
    """Generates and manages a configurable maze, including structure,
    special '42' cells, and optional imperfect paths."""
    def __init__(self, width: int, height: int, start: tuple[int, int],
                 end: tuple[int, int], output_file: str, maze_type: bool,
                 num_42_cells: list[tuple[int, int]]) -> None:
        """Initialize the maze generator with dimensions, endpoints,
        output file, type, and optional '42' cell positions."""
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.output_file = output_file
        self.maze_type = maze_type
        self.walls_config = self.init_walls()
        self.num_42_cells = num_42_cells
        self.algorithm_pos = [self.start]
        self.moves_sequence = [self.start]
        self.walls_to_burn: dict[tuple[int, int], tuple[int, int]] = {}

    def init_walls(self):
        """Initialize the maze grid with all walls present for each cell."""
        grid = dict()
        for i in range(self.height):
            for j in range(self.width):
                grid[(j, i)] = [1, 1, 1, 1]
        return (grid)

    def get_possible_moves1(self,
                            curr_coordinate: tuple[int, int],
                            taken_cells: list[tuple[int, int]]) -> dict[
                                int, tuple[int, int]]:
        """Return valid neighboring moves excluding visited cells,
        out-of-bounds positions, and '42' cells."""
        x, y = curr_coordinate
        moves_dict = {
            0: (x, y - 1),
            1: (x + 1, y),
            2: (x, y + 1),
            3: (x - 1, y)}
        possible_moves = []
        for move in moves_dict.values():
            x, y = move
            if (x >= 0 and x < self.width and y >= 0 and y < self.height
                    and move not in taken_cells
                    and move not in self.num_42_cells):
                possible_moves.append(move)
        possible_moves_dict = {num: move for num, move in moves_dict.items() if
                               move in possible_moves}
        return (possible_moves_dict)

    def create_maze(self) -> None:
        """Generate the maze using backtracking, carving paths while avoiding
        '42' cells and optionally creating imperfections."""
        curr_cell = self.start
        total_num_cells = len(self.num_42_cells)
        total_cells = self.height * self.width
        while len(self.moves_sequence) + total_num_cells != total_cells:
            possible_moves_dict = self.get_possible_moves1(
                curr_cell,
                self.moves_sequence)
            while not possible_moves_dict:
                curr_index = self.moves_sequence.index(curr_cell)
                curr_cell = self.moves_sequence[curr_index - 1]
                possible_moves_dict = self.get_possible_moves1(
                    curr_cell,
                    self.moves_sequence)
            move_index = random.choice(list(possible_moves_dict.keys()))
            self.walls_config[curr_cell][move_index] = 0
            curr_cell = possible_moves_dict[move_index]
            self.walls_config[curr_cell][(move_index + 2) % 4] = 0
            self.moves_sequence.append(curr_cell)
        if not self.maze_type:
            self.remove_walls()

    def select_cell(self,
                    curr_cell: tuple[int, int]) -> tuple[int, int] | None:
        """Randomly select a valid neighboring cell separated by a wall,
        remove the wall, and return the new cell or None if unavailable."""
        curr_x, curr_y = curr_cell
        close_cells = [
            (curr_x, curr_y - 1),
            (curr_x + 1, curr_y),
            (curr_x, curr_y + 1),
            (curr_x - 1, curr_y)]
        valid_cells = [
            cell for cell, num
            in zip(close_cells, self.walls_config[curr_cell])
            if num and cell not in self.num_42_cells]
        if not valid_cells:
            return (None)
        next_cell = random.choice(valid_cells)
        index = close_cells.index(next_cell)
        self.walls_config[curr_cell][index] = 0
        self.walls_config[next_cell][(index + 2) % 4] = 0
        return (next_cell)

    def remove_walls(self) -> None:
        """Randomly remove additional walls to create an imperfect maze with
        multiple solutions while avoiding '42' cells."""
        available_cells = [
            (i, j) for i in range(1, self.width - 1)
            for j in range(1, self.height - 1) if (i, j)
            not in self.num_42_cells]
        while available_cells:
            curr_cell = random.choice(available_cells)
            next_cell = self.select_cell(curr_cell)
            while not next_cell:
                available_cells.remove(curr_cell)
                if not available_cells:
                    return
                curr_cell = random.choice(available_cells)
                next_cell = self.select_cell(curr_cell)
            self.walls_to_burn[curr_cell] = next_cell
            curr_x, curr_y = curr_cell
            close_cells = [
                (curr_x + i, curr_y + j)
                for i in [-2, -1, 0, 1, 2]
                for j in [-2, -1, 0, 1, 2]]
            available_cells = [
                cell for cell in available_cells
                if cell not in close_cells]

    def get_possible_moves2(self, curr_cell: tuple[int, int],
                            taken_cells: list[tuple[int, int]]) -> list[
                                tuple[int, int]]:
        """Return accessible neighboring cells through open walls that have
        not yet been visited."""
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

    def solve_maze(self,
                   start_cell: tuple[int, int],
                   end_cell: tuple[int, int]) -> list[tuple[int, int]]:
        """Find a path from start to end using backtracking through open walls
        and return the solution path."""
        curr_cell = start_cell
        best_path = [curr_cell]
        cell_paths: dict[tuple[int, int], list[tuple[int, int]]] = {}
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
        best_path.pop()
        best_path.pop(0)
        return (best_path)

    def write_output(self) -> None:
        """Write the maze structure, start/end points, and solution path
        directions to the output file."""
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
        x_start, y_start = self.start
        x_end, y_end = self.end
        file.write(f"\n{x_start},{y_start}\n")
        file.write(f"{x_end},{y_end}\n")
        solution = self.solve_maze(self.start, self.end)
        curr_cell = self.start
        for next_cell in solution[1:]:
            x_curr, y_curr = curr_cell
            x_next, y_next = next_cell
            if x_next > x_curr:
                file.write("E")
            elif x_next < x_curr:
                file.write("W")
            elif y_next > y_curr:
                file.write("S")
            elif y_next < y_curr:
                file.write("N")
            curr_cell = next_cell
        file.write("\n")
        file.close()
