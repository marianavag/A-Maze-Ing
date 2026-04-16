import sys


def create_dict(filename: str) -> dict[str, str]:
    # Create a dictionary with the keys and values
    file = open(filename, 'r')
    config_dict = {}
    while True:
        line = file.readline()
        if not line:
            break
        if line == "\n":
            raise TypeError("[ERROR] Empty line found")
        key, value = line.split("=")
        key = key.lower().strip()
        value = value.strip()
        config_dict[key] = value
    file.close()
    return (config_dict)


def check_keys(config_dict: dict[str, str]) -> None:
    # Check if every mandatory key appears
    mandatory_keys = [
        "width",
        "height",
        "entry",
        "exit",
        "output_file",
        "perfect"]
    missing_keys = []
    for key in mandatory_keys:
        if key not in config_dict:
            missing_keys.append(key)
    if missing_keys:
        error_message = "[ERROR] Key(s) "
        for key in missing_keys:
            error_message += "'" + key + "'" + ", "
        error_message = error_message[:-2]
        error_message += " not found"
        raise KeyError(error_message)


def check_types(config_dict: dict[str, str]) -> str | dict[str, any]:
    # Check types of the values
    # If no error ocurred it returns a dict with the values casted
    key_type_dict = {"int": ["width", "height"],
                     "int_tuple": ["entry", "exit"],
                     "text_file": ["output_file"],
                     "boolean": ["perfect"]}
    for key_type, keys in key_type_dict.items():
        if key_type == "int":
            for key in keys:
                if key in config_dict:
                    try:
                        config_dict[key] = int(config_dict[key])
                    except ValueError:
                        return (f"[ERROR] '{key}' has to be an int value")
        if key_type == "int_tuple":
            for key in keys:
                if key in config_dict:
                    try:
                        x, y = config_dict[key].split(",")
                        config_dict[key] = (int(x), int(y))
                    except ValueError:
                        return (f"[ERROR] '{key}' has to be a size "
                                "2 tuple with int values")
        if key_type == "text_file":
            for key in keys:
                if key in config_dict:
                    filename = config_dict[key]
                    if filename[-4:] != ".txt":
                        raise TypeError(f"[ERROR] '{key}' has to be .txt file")
        if key_type == "boolean":
            for key in keys:
                if key in config_dict:
                    value = config_dict[key].lower()
                    if value == "true":
                        config_dict[key] = True
                    elif value == "false":
                        config_dict[key] = False
                    else:
                        raise TypeError(f"[ERROR] '{key}' has to be boolean")
    return (config_dict)


def parsing_keys() -> str | dict[str, any]:
    # Full parsing function for keys that runs the others above
    # Returns a string if an error ocurred or nothing if everything worked
    filename = sys.argv[1]
    try:
        config_dict = create_dict(filename)
    except FileNotFoundError:
        return ("[ERROR] No file named {filename} was found")
    except PermissionError:
        return ("[ERROR] File {filename} has no permission to read")
    except TypeError as message:
        return (message.args[0])
    except ValueError:
        return ("[ERROR] Invalid key, value pairing. Should be 'KEY=VALUE'")
    try:
        check_keys(config_dict)
    except KeyError as message:
        return (message.args[0])
    try:
        config_dict = check_types(config_dict)
        if isinstance(config_dict, str):
            return (config_dict)
    except TypeError as message:
        return (message.args[0])
    return (config_dict)


def parsing_values(config_dict: dict[str, any],
                   taken_cells: list[tuple[int, int]]) -> str | None:
    # Verify if all parameters are valid
    width = config_dict["width"]
    height = config_dict["height"]
    if width < 9:
        raise ValueError("[ERROR] Width has to be at minimum 9")
    if height < 8:
        raise ValueError("[ERROR] Height has to be at minimim 8")
    entry_cell = config_dict["entry"]
    x_entry, y_entry = entry_cell
    exit_cell = config_dict["exit"]
    x_exit, y_exit = exit_cell
    if (x_entry < 0 or x_entry >= width or y_entry < 0 or y_entry >= height):
        raise ValueError(f"[ERROR] Start coordinate '({x_entry}, {y_entry})' "
                         f"has to be inside maze "
                         f"(positive and smaller then {width})")
    if (x_exit < 0 or x_exit >= width or y_exit < 0 or y_exit >= height):
        raise ValueError(f"[ERROR] Finish coordinate '({x_exit}, {y_exit})' "
                         f"has to be inside maze "
                         f"(positive and smaller then {width})")
    if (entry_cell in taken_cells) or (exit_cell in taken_cells):
        raise ValueError("[ERROR] Entry and exit coordinates cannot be on 42")


def get_42_cells(config_dict: dict[str, any]) -> list[tuple[int, int]]:
    # Defines the cells with 42
    width = config_dict["width"]
    height = config_dict["height"]
    x_mid = width // 2 - 1
    y_mid = height // 2 - 1
    return ([(x_mid - 3, y_mid - 2),
             (x_mid + 1, y_mid - 2),
             (x_mid + 2, y_mid - 2),
             (x_mid + 3, y_mid - 2),
             (x_mid - 3, y_mid - 1),
             (x_mid + 3, y_mid - 1),
             (x_mid - 3, y_mid),
             (x_mid - 2, y_mid),
             (x_mid - 1, y_mid),
             (x_mid + 1, y_mid),
             (x_mid + 2, y_mid),
             (x_mid + 3, y_mid),
             (x_mid - 1, y_mid + 1),
             (x_mid + 1, y_mid + 1),
             (x_mid - 1, y_mid + 2),
             (x_mid + 1, y_mid + 2),
             (x_mid + 2, y_mid + 2),
             (x_mid + 3, y_mid + 2)])
