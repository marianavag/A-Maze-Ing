from random import randint, random
from mazegen.mlx.mlx import Mlx
from mazegen.maze_generator import MazeGenerator


class Image:

    def __init__(self, maze: MazeGenerator, title: str, texts: list[str], cell_size: int,
                 width: int, height: int, color_dict: dict[str, list[int]],
                 pixel_dict: dict[str, list[int]]) -> None:

        # Setting up the basic settings 
        self.maze = maze
        self.start = self.maze.start
        self.end = self.maze.end
        self.curr_cell = self.maze.start
        self.title = title
        self.texts = texts
        self.cell_size = cell_size
        self.wall_width = 3
        self.maze_width = cell_size - self.wall_width * 2
        self.width = cell_size * width
        self.height = cell_size * height + 20 * len(texts)
        self.color_dict = color_dict
        self.pixel_dict = pixel_dict
        # Setting the animation generator and time attributes 
        self.building_maze = True
        self.deleting_walls = False
        self.algorithm_gen = self.algorithm_sequence()
        self.last_time = None
        self.delay = 0.5
        self.burst_delay = 0.03
        # Jump start the mlx and saving important attributes
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(self.mlx_ptr, self.width,
                                               self.height, self.title)
        self.img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, self.width,
                                              cell_size * height)
        buf, bpp, size_line, fmt = self.mlx.mlx_get_data_addr(self.img_ptr)
        self.buf = buf
        self.size_line = size_line

    def change_colors(self) -> None:

        for element in self.color_dict.keys():
            for i in range(3):
                b = randint(0, 255)
                g = randint(0, 255)
                r = randint(0, 255)
            self.color_dict[element] = [b, g, r]

    def color_element(self, element: str, color: list[int] = None) -> None:

        if not color:
            b, g, r = self.color_dict[element]
        else:
            b, g, r = color
        for index in self.pixel_dict[element]:
            self.buf[index + 0] = b
            self.buf[index + 1] = g
            self.buf[index + 2] = r
            self.buf[index + 3] = 255
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)

    def insert_text(self) -> None:

        y_pos = self.height - 20 * len(self.texts)
        for text in self.texts:
            self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr, 0, y_pos, 0xFFFFFF, text)
            y_pos += 20

    def color_rect(self, element: str, start_pixel: tuple[int, int], rect_height: int,
                   rect_width: int, paint: bool = True) -> None:

        b, g, r = self.color_dict[element]
        for _ in range(rect_height):
            for _ in range(rect_width):
                self.pixel_dict[element].append(start_pixel)
                self.buf[start_pixel] = b
                self.buf[start_pixel + 1] = g
                self.buf[start_pixel + 2] = r
                self.buf[start_pixel + 3] = 255
                start_pixel += 4
            start_pixel -= 4 * rect_width
            start_pixel += self.size_line
        if paint:
            self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)

    def color_cell(self, element: str, curr_cell: tuple[int, int], paint: bool = True) -> None:

        x_curr, y_curr = curr_cell
        start = (y_curr * self.size_line + x_curr * 4) * self.cell_size
        start += (self.size_line + 4) * self.wall_width
        self.color_rect(element, start, self.maze_width, self.maze_width, paint)

    def draw_grid(self) -> None:

        # Coloring the horizontal lines
        self.color_rect("maze_num_wall", 0, self.wall_width, self.width, False)
        start = (self.cell_size - self.wall_width) * self.size_line
        for i in range(1, self.maze.height):
            self.color_rect("maze_num_wall", start, 2 * self.wall_width, self.width, False)
            start += self.cell_size * self.size_line
        self.color_rect("maze_num_wall", start, self.wall_width, self.width, False)
        # Coloring the vertical lines 
        self.color_rect("maze_num_wall", 0, self.maze.height * self.cell_size, self.wall_width, False)
        start = (self.cell_size - self.wall_width) * 4
        for i in range(1, self.maze.width):
            self.color_rect("maze_num_wall", start, self.maze.height * self.cell_size, 2 * self.wall_width, False)
            start += self.cell_size * 4
        self.color_rect("maze_num_wall", start, self.maze.height * self.cell_size, self.wall_width, False)
        # Coloring the number 42
        for cell in self.maze.num_42_cells:
            self.color_cell("maze_num_wall", cell, False)
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)

    def color_wall(self, element: str, curr_cell: tuple[int, int], next_cell: tuple[int, int],
                   taken_cells: list[tuple[int, int]], paint: bool = True) -> int:

        if next_cell in taken_cells:
            return (0)
        x_curr, y_curr = curr_cell
        x_next, y_next = next_cell
        curr_cell_start = (y_curr * self.size_line + x_curr * 4) * self.cell_size
        curr_cell_start += (self.size_line + 4) * self.wall_width
        next_cell_start = (y_next * self.size_line + x_next * 4) * self.cell_size
        next_cell_start += (self.size_line + 4) * self.wall_width
        start = max(curr_cell_start, next_cell_start)
        if y_curr == y_next and abs(x_curr - x_next) == 1:
            start -= 4 * 2 * self.wall_width
            self.color_rect(element, start, self.maze_width, 2 * self.wall_width)
            return (1)
        elif x_curr == x_next and abs(y_curr - y_next) == 1:
            start -= self.size_line * 2 * self.wall_width
            self.color_rect(element, start, 2 * self.wall_width, self.maze_width)
            return (1)
        return (0)

    def algorithm_sequence(self) -> Generator[None, None, None]:

        cell_sequence = self.maze.moves_sequence.copy()
        curr_cell = cell_sequence.pop(0)
        self.color_cell("background", curr_cell)
        cell_hist = [curr_cell]
        taken_cells = [curr_cell]
        yield
        for next_cell in cell_sequence:
            while not self.color_wall("background", curr_cell, next_cell, taken_cells):
                cell_hist.pop()
                curr_cell = cell_hist[-1]
            else:
                self.color_cell("background", next_cell)
                cell_hist.append(next_cell)
                taken_cells.append(next_cell)
                curr_cell = next_cell
                yield
        self.pixel_dict["background"] = set(self.pixel_dict["background"])
        self.pixel_dict["maze_num_wall"] = set(self.pixel_dict["maze_num_wall"]) - self.pixel_dict["background"]
        self.pixel_dict["background"] = list(self.pixel_dict["background"])
        self.pixel_dict["maze_num_wall"] = list(self.pixel_dict["maze_num_wall"])

    def start_visual(self) -> None:

        self.insert_text()
        self.draw_grid()
        self.mlx.mlx_key_hook(self.win_ptr, self.on_key, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.animation, None)
        self.mlx.mlx_loop(self.mlx_ptr)

    # This function is responsable for the whole animation 
    def animation(self, param) -> None:

        if self.building_maze:
            now = time.monotonic()
            if (not self.last_time or now - self.last_time > self.delay):
                try:
                    next(self.algorithm_gen)
                    self.last_time = time.monotonic()
                except StopIteration:
                    self.building_maze = False
                    if not self.maze.maze_type:
                        self.deleting_walls = True
                    for cell1, cell2 in self.maze.walls_to_burn.items():
                        self.color_wall("walls_to_delete", cell1, cell2, [], False)
                    self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)
        elif self.deleting_walls:
            if (self.color_dict["walls_to_delete"] != [0, 0, 255]):
                now = time.monotonic()
                if (now - self.last_time > self.burst_delay):
                    b, g, r = self.color_dict["walls_to_delete"]
                    self.color_dict["walls_to_delete"] = [0, 0, r + 1]
                    self.color_element("walls_to_delete")
                    self.last_time = time.monotonic()
            else:
                self.color_dict["walls_to_delete"] = self.color_dict["background"]
                self.color_element("walls_to_delete")
                self.pixel_dict["background"] += self.color_dict["walls_to_delete"]
                del self.pixel_dict["walls_to_delete"]
                del self.color_dict["walls_to_delete"]
                self.color_cell("entry", self.start)
                self.color_cell("exit", self.end)
                self.deleting_walls = False
        return
 
    # This function is responsable for drawing the moves player does with the arrows
    def move(self) -> None:

        if self.curr_cell == self.end:
            self.color_element("background")
            self.end = (randint(0, self.maze.width - 1),
                        randint(0, self.maze.height - 1))
            if self.end in self.maze.num_42_cells:
                self.end = (randint(0, self.maze.width - 1),
                            randint(0, self.maze.height - 1))
            self.pixel_dict["exit"] = []
            self.color_cell("exit", self.end, False)
            self.pixel_dict["player_path"] = []
            self.pixel_dict["entry"] = []
        self.pixel_dict["position"] = []
        self.color_cell("position", self.curr_cell, False)
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)

    def on_key(self, keycode, param) -> None:

        # Escape keycode to quit window 
        if keycode == 65307:
            self.mlx.mlx_loop_exit(self.mlx_ptr)
        # - Keycode to half the animation speed  
        if keycode == 65451 and self.building_maze:
            self.delay /= 2
        # + Keycode to double the animation speed 
        if keycode == 65453 and self.building_maze:
            self.delay *= 2
        # Space Keycode to change colors
        if keycode == 32 and not (self.building_maze or self.deleting_walls):
            self.change_colors()
            for element in self.pixel_dict.keys():
                self.color_element(element, self.color_dict[element])
        # N Keycode to generate a new maze 
        if keycode == 110 and not (self.building_maze or self.deleting_walls):
            self.maze = MazeGenerator(self.maze.width, self.maze.height, self.maze.start,
                                      self.maze.end, self.maze.output_file, 
                                      self.maze.maze_type, self.maze.num_42_cells)
            self.maze.create_maze()
            self.maze.write_output()
            self.start = self.maze.start
            self.curr_cell = self.maze.start
            self.color_element("maze_num_wall", [0, 0, 0])
            self.color_element("background", [0, 0, 0])
            self.pixel_dict = {key: [] for key in self.pixel_dict}
            self.pixel_dict["walls_to_delete"] = []
            self.color_dict["walls_to_delete"] = [0, 0, 100]
            self.draw_grid()
            self.building_maze = True
            self.algorithm_gen = self.algorithm_sequence()
        # S key that makes the solution pop up 
        if keycode == 115 and not (self.building_maze or self.deleting_walls):
            start = self.curr_cell
            end = self.end
            self.pixel_dict["solution"] = []
            for cell in self.maze.solve_maze(start, end):
                self.color_cell("solution", cell, False)
            self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)
        # H key that hide the solution 
        if keycode == 104 and not (self.building_maze or self.deleting_walls):
            self.color_element("solution", self.color_dict["background"])
            self.color_element("player_path")
            self.color_element("position")
            self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)
        # Arrows to move single player 
        if keycode in [65361, 65362, 65363, 65364] and not (self.building_maze or self.deleting_walls):
            if self.curr_cell != self.start:
                self.color_cell("player_path", self.curr_cell, False)
            # Left arrow and is able to move left 
            if keycode == 65361 and not self.maze.walls_config[self.curr_cell][3]:
                x_pos, y_pos = self.curr_cell
                self.curr_cell = (x_pos - 1, y_pos)
                self.move()
            # Up arrow and is able to move up 
            elif keycode == 65362 and not self.maze.walls_config[self.curr_cell][0]:
                x_pos, y_pos = self.curr_cell
                self.curr_cell = (x_pos, y_pos - 1)
                self.move()
            # Right arrow and is able to move right 
            elif keycode == 65363 and not self.maze.walls_config[self.curr_cell][1]:
                x_pos, y_pos = self.curr_cell
                self.curr_cell = (x_pos + 1, y_pos)
                self.move()
            # Down arrow and is able to move down 
            elif keycode == 65364 and not self.maze.walls_config[self.curr_cell][2]:
                x_pos, y_pos = self.curr_cell
                self.curr_cell = (x_pos, y_pos + 1)
                self.move()
