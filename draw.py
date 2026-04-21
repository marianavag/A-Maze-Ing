import time
import random
from mlx import Mlx
from maze_generator import MazeGenerator
from random import randint


class Image:

    def __init__(self, maze: MazeGenerator, title: str, texts: list[str], cell_size: int,
                 width: int, height: int, color_dict: dict[str, list[int]]) -> None:

        self.maze = maze
        self.start = self.maze.start
        self.end = self.maze.end
        self.curr_cell = self.maze.start
        self.title = title
        self.texts = texts
        self.cell_size = cell_size
        self.width = cell_size * width
        self.height = cell_size * height + 20 * len(texts)
        self.color_dict = color_dict
        self.color_dark = ["solution"]
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(self.mlx_ptr, self.width,
                                               self.height, self.title)
        self.img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, self.width,
                                              cell_size * height)
        buf, bpp, size_line, fmt = self.mlx.mlx_get_data_addr(self.img_ptr)
        self.buf = buf
        self.size_line = size_line
        self.pixel_dict = self.get_pixel_dict()

    def change_colors(self) -> None:

        for element in self.color_dict.keys():
            for i in range(3):
                b = randint(0, 255)
                g = randint(0, 255)
                r = randint(0, 255)
            self.color_dict[element] = [b, g, r]

    def color_image(self) -> None:

        for element in self.pixel_dict.keys():
            b, g, r = self.color_dict[element]
            if element in self.color_dark:
                b, g, r = 0, 0, 0
            for index in self.pixel_dict[element]:
                self.buf[index + 0] = b
                self.buf[index + 1] = g
                self.buf[index + 2] = r
                self.buf[index + 3] = 255
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)

    def reset_elements_color(self, elements: list[str]) -> None:

        self.color_dark += elements
        if "solution" not in self.color_dark:
            self.color_dark.append("solution")
        self.color_image()
        for element in elements:
            if element != "solution":
                self.color_dark.remove(element)

    def get_block_pixels(self, pos_list: list[int], block_size: int) -> None:

        pixel_list = []
        add = (self.cell_size - block_size) // 2
        for pos in pos_list:
            x_pos, y_pos = pos
            index = (y_pos * self.size_line + x_pos * 4) * self.cell_size
            index += add * self.size_line + add * 4
            for j in range(block_size):
                for i in range(block_size):
                    pixel_list.append(index)
                    index += 4
                index -= block_size * 4
                index += self.size_line
        return (pixel_list)

    def get_pixel_dict(self) -> dict[str, list[int]]:

        pixel_dict = dict()
        # Get maze walls pixels 
        wall_indexs = []
        for pos, walls in self.maze.walls_config.items():
            x_pos, y_pos = pos
            up, right, down, left = walls
            if up:
                index = (y_pos * self.size_line + x_pos * 4) * self.cell_size
                for i in range(self.cell_size):
                    wall_indexs.append(index)
                    index += 4
            if right:
                index = (y_pos * self.size_line + x_pos * 4) * self.cell_size 
                index += (self.cell_size - 1) * 4
                for i in range(self.cell_size):
                    wall_indexs.append(index)
                    index += self.size_line
            if down:
                index = (y_pos * self.size_line + x_pos * 4) * self.cell_size
                index += (self.cell_size - 1) * self.size_line
                for i in range(self.cell_size):
                    wall_indexs.append(index)
                    index += 4
            if left:
                index = (y_pos * self.size_line + x_pos * 4) * self.cell_size
                for i in range(self.cell_size):
                    wall_indexs.append(index)
                    index += self.size_line
        # Get 42 number pixels
        number_42_indexs = self.get_block_pixels(self.maze.num_42_cells, self.cell_size)
        pixel_dict["maze_num_wall"] = number_42_indexs + wall_indexs 
        # Initialize solution, player_path and entry pixels 
        pixel_dict["solution"] = []
        pixel_dict["player_path"] = []
        pixel_dict["position"] = [] 
        # Get entry pixels
        entry_indexs = self.get_block_pixels([self.start], self.cell_size - 2)
        pixel_dict["entry"] = entry_indexs
        # Get exit pixels
        exit_indexs = self.get_block_pixels([self.end], self.cell_size - 2)
        pixel_dict["exit"] = exit_indexs
        return(pixel_dict)

    def start_visual(self) -> None:

        self.color_image()
        y_pos = self.height - 20 * len(self.texts)
        for text in self.texts:
            self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr, 0, y_pos, 0xFFFFFF, text)
            y_pos += 20
        self.mlx.mlx_key_hook(self.win_ptr, self.on_key, ())
        self.mlx.mlx_loop(self.mlx_ptr)

    # This function is responsable for drawing the moves player does with the arrows
    def move(self) -> None:

        if self.curr_cell == self.end:
            self.reset_elements_color(["exit", "player_path", "entry"])
            self.end = (random.randint(0, self.maze.width - 1),
                        random.randint(0, self.maze.height - 1))
            if self.end in self.maze.num_42_cells:
                self.end = (random.randint(0, self.maze.width - 1),
                            random.randint(0, self.maze.height - 1))
            exit_indexs = self.get_block_pixels([self.end], self.cell_size - 2)
            self.pixel_dict["exit"] = exit_indexs
            self.pixel_dict["player_path"] = []
            self.pixel_dict["entry"] = []
        cell_pixels = self.get_block_pixels([self.curr_cell], self.cell_size - 10)
        for pixel in cell_pixels:
            self.pixel_dict["player_path"].append(pixel)
        self.pixel_dict["position"] = cell_pixels
        self.color_image()

    def on_key(self, keycode, param) -> None:

        # Escape keycode to quit window 
        if keycode == 65307:
            self.mlx.mlx_loop_exit(self.mlx_ptr)
        # Space Keycode to change colors 
        if keycode == 32:
            self.change_colors()
            self.color_image()
        # N Keycode to generate a new maze 
        if keycode == 110:
            self.maze = MazeGenerator(self.maze.width, self.maze.height, self.maze.start,
                                      self.maze.end, self.maze.output_file, 
                                      self.maze.maze_type, self.maze.num_42_cells)
            self.maze.create_maze()
            self.maze.write_output()
            self.curr_cell = self.maze.start
            self.reset_elements_color(["maze_num_wall", "player_path", "position"])
            self.pixel_dict = self.get_pixel_dict()
            self.color_image()
        # S key that makes the solution pop up 
        if keycode == 115:
            start = self.curr_cell
            end = self.end
            solution_indexs = self.get_block_pixels(self.maze.solve_maze(start, end),
                                                    self.cell_size - 8)
            self.pixel_dict["solution"] = solution_indexs
            if "solution" in self.color_dark:
                self.color_dark.remove("solution")
            self.color_image()
        # H key that hide the solution 
        if keycode == 104:
            if "solution" not in self.color_dark:
                self.color_dark.append("solution")
            self.color_image()
        # Arrows to move single player 
        if keycode in [65361, 65362, 65363, 65364]:
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
