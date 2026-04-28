import sys
import random
from mazegen.draw import Image
from mazegen.maze_generator import MazeGenerator
import mazegen.parsing as parsing


def main() -> None:

    if len(sys.argv) != 2:
        print("[ERROR] Invalid input. Only takes one argument")
        sys.exit()
    config_dict = parsing.parsing_keys()
    if isinstance(config_dict, str):
        print(config_dict)
        sys.exit()
    num_42_cells = parsing.get_42_cells(config_dict)
    random.seed(config_dict["seed"])
    try:
        parsing.parsing_values(config_dict, num_42_cells)
    except ValueError as message:
        print(message)
        sys.exit()
    maze = MazeGenerator(config_dict["width"], config_dict["height"],
                         config_dict["entry"], config_dict["exit"],
                         config_dict["output_file"], config_dict["perfect"], num_42_cells)
    maze.create_maze()
    maze.write_output()
    color_dict = {"walls_to_delete": [0, 0, 100],
                  "background": [120, 50, 90],
                  "maze_num_wall": [120, 120, 120],
                  "solution": [0, 255, 0],
                  "entry": [255, 0, 0],
                  "exit": [0, 0, 255],
                  "player_path": [70, 70, 70],
                  "position": [150, 150, 150]}
    pixel_dict = {key: [] for key in color_dict.keys()}
    texts = ["====== A-Maze-Ing ======",
             "Use arrows to move",
             "Press +/- to change animation speed",
             "Press SPACE to Change Colors",
             "Press N to Re-generate maze",
             "Press S/H to Show/Hide Solution",
             "Press ESC to Quit"]
    maze_visual = Image(maze, "Maze Generator", texts, 25, maze.width,
                        maze.height, color_dict, pixel_dict)
    maze_visual.start_visual()


if __name__ == "__main__":
    main()
