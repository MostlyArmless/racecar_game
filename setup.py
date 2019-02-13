# Use this script to build the game into an executable
import cx_Freeze

executables = [cx_Freeze.Executable("test.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["racecar2.png", "quitscreen.png"]}},
    executables=executables)
