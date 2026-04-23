*This project has been created as part of the 42 curriculum by rcarmo-n, mgomes-v.*

# A-Maze-ing


## Description

`A-Maze-ing` is a Python-based maze generator and solver. The project aims to create randomized mazes based on customizable configurations (dimensions, random seeds, entry/exit points), ensuring that the center of the maze contains a fixed structure (the "42" logo). The project includes a functional graphical interface that allows users to navigate the maze manually, trigger an automatic solver, and interact with the environment in real-time.


## Instructions

### Prerequisites & Libraries
This project utilizes the `MiniLibX (MLX)` library for its graphical interface. The MLX is a simple windowing framework that allows for pixel manipulation, image rendering, and keyboard/mouse event handling. Ensure the MLX environment is correctly set up for your operating system before running the application.

### Installation
The project includes a Makefile to automate the setup. To install dependencies and the mazegen package in editable mode, run:
```bash
make install
```
Or manually specify a different config file:
```bash
python3 main.py your_config.txt
```

### Execution
To generate and visualize the maze using the default configuration file:
```bash
make run
```

### Controls
- `Arrow Keys`: Move the player through the maze.
- `SPACE`: Randomly change the interface colors.
- `N`: Generate a brand new maze.
- `S`: Show the solution path.
- `H`: Hide the solution path.
- `ESC`: Close the application.


## Configuration File Structure

The configuration file (`config.txt`) must follow this strict `KEY=VALUE` format:
- `WIDTH`: The width of the maze (minimum 9).
- `HEIGHT`: The height of the maze (minimum 8).
- `ENTRY`: Starting coordinates (x,y).
- `EXIT`: Finish coordinates (x,y).
- `OUTPUT_FILE`: The name of the `maze.txt` file where the maze will be saved in hexadecimal format.
- `PERFECT`: Boolean (`True/False`) indicating if the maze should be perfect (no loops).
- `SEED (Optional)`: An integer value to replicate random generation.


## Maze Generation Algorithm

The implemented algorithm is based on a variant of the **Depth-First Search (DFS) with iterative backtracking**.

Why this algorithm?
1. **Guaranteed Solvability**: It ensures every cell is reachable, always creating a path between the entry and exit points.
2. **Visual Complexity**: It generates long, winding corridors, which are more challenging and aesthetically pleasing than algorithms like Prim's.
3. **Memory Efficiency**: By using an iterative approach instead of a recursive one, we avoid "maximum recursion depth" errors on large-scale mazes.


## Code Reusability

The project was designed with strict modularity to allow its components to be integrated into other software or expanded for different use cases.

### Reusable Components
- `parsing.py`: A standalone type-checking and key-validation engine. It can be adapted for any project requiring strict configuration file reading (`KEY=VALUE` format).
- `MazeGenerator` Class: The core logic for generation and solving is completely decoupled from the visualization.
- `Image` Class (Draw): Acts as a specialized wrapper for the `MiniLibX (MLX)` library. It can be reused in other graphical projects that require efficient pixel buffer manipulation and event hook management in Python.

### How to reuse it in other projects
1 - **Install the package**:
Run `make install` or `pip install -e .` in the project root.
2 - **Import and Execute**:
```bash
from mazegen.maze_generator import MazeGenerator

# Initialize with dimensions and constraints
maze = MazeGenerator(width=20, height=20, start=(0,0), end=(19,19), ...)

# Generate the maze data structure
maze.create_maze()

# Get the solution path as a list of coordinates
path = maze.solve_maze((0,0), (19,19))
```

3 - **Data Structure:**:
The maze is stored in `self.walls_config`, a dictionary where keys are `(x, y)` tuples and values are lists of integers representing walls `[Up, Right, Down, Left]`.


## Team & Project Management

### Team roles
**rcarmo-d** - Core Maze Logic, DFS Algorithm, Pathfinding Solver, Pixel Buffers.
**mgomes-v** - MLX Graphics, Parsing Engine, Reusability Structure, Makefile/README.

### Evolution & Challenges
- **Scope Creep**: Initially, we only planned a static visualizer with simple color animations. We evolved this into a **fully playable game**, which required complex integration of keyboard hooks and real-time rendering.
- **The "42" Obstacle**: Ensuring the maze stayed solvable while navigating around a fixed central logo was the biggest algorithmic challenge.

### Future Improvements
- **Refactoring**: Simplify the nested `if` structures in `parsing.py` to improve readability and organization.
- **Code Cleanup**: Consolidating repetitive wall-drawing logic into a single helper function.
- **Performance**: Optimizing pixel buffer updates to only re-render changed cells rather than the entire frame.

### Tools used
- **MiniLibX (MLX)**: Graphical library used for window management, pixel rendering, and keyboard event handling.
- **Python 3.10+**: The core programming language.
- **Flake8 & Mypy**: Used for linting and static type checking to ensure code quality and PEP 8 compliance.
- **Setuptools**: Used for packaging the project (via `pyproject.toml`), making the `mazegen` module reusable.
- **Make**: Used for automating installation, running, and cleaning the project.


## Advanced Features Implemented

- **Interactive Game Mode:** Real-time navigation using arrow keys via MLX keyboard hooks.
- **Live Pathfinding**: Instant visual solution toggle (`S` key) using a built-in solver.
- **On-the-fly Generation**: Generate new mazes (`N`) and randomize colors (`SPACE`) without restarting.
- **Logo Constraint**: Integrated the "42" logo into the logic while keeping the maze traversable.
- **Seed Support**: Included a `SEED` parameter to allow the reproduction of specific layouts.
- **Project Portability**: Fully packaged using `pyproject.toml` for easy installation and reuse.


## Resources

Classic references (maze generation and DFS):
- Depth-First Search (DFS): https://en.wikipedia.org/wiki/Depth-first_search
- Maze generation algorithms: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Backtracking: https://en.wikipedia.org/wiki/Backtracking
- Python packaging (pyproject.toml): https://packaging.python.org/

**AI Usage**
AI was utilized in a supportive role during the final stages of the project:
- Documentation & Structure: Provided support for refining algorithm explanations and organizing the README sections for better clarity.
- Manual Integrity: All core implementation decisions, architectural choices, and code validation remained strictly manual to ensure the project met curriculum standards.