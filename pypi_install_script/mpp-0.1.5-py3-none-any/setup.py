import json
import os
import shutil

from mpp.src.utils import ask, constants as cst, files


def setup(args=None):
    """
    Asks information to the user and setup the environment

    Args:
        args (argparse args): parameters from parser.parse_args()
    """

    with open(cst.path_questions) as f:
        questions = json.load(f)

    # Get information to forecast user's mpp_config
    current_dir = os.path.basename(os.getcwd())
    username = os.path.basename(os.path.expanduser("~"))

    # Ask questions
    mpp_config = dict()
    mpp_config["name"] = ask.question(questions["name"], current_dir, required=True)
    mpp_config["author"] = ask.question(questions["author"], username, required=True)
    mpp_config["version"] = "0.0.0"
    mpp_config["console"] = "y"
    mpp_config["icon"] = "resources/images/icon.ico"
    mpp_config["hidden-imports"] = list()

    # Create folders
    os.makedirs("resources/images", exist_ok=True)
    os.makedirs("src", exist_ok=True)

    # Add icon
    if not os.path.exists(mpp_config["icon"]):
        shutil.copy(cst.path_ico_default, mpp_config["icon"])
    # Write configuration file
    files.write_mpp_config(mpp_config)
    # Write main file
    if not os.path.exists("main.py"):
        with open("main.py", "w") as f:
            f.write(cst.pattern_main_py % mpp_config)

    print("")
    print(f"The project's version is {mpp_config['version']}.")
    print(f"The project's icon can be found here: {mpp_config['icon']}.")
    print("The `main.py` file can now be edited.")
    print("")
    print("Use `mpp --help` to display all possible commands.")
    print("Use `mpp <command> -h` to display the help for a command.")
    print("Use `mpp config --list` to show your project settings.")
