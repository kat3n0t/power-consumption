import sys
from cx_Freeze import setup, Executable

app_name = "PowerConsumption"

base = None
target_name = app_name
if sys.platform == "win32":
    base = "gui"
    target_name += ".exe"

build_exe_options = {
    "optimize": 2,
    "excludes": ["email", "tkinter", "html", "http", "xml"]
}

setup(
    name=app_name,
    version="1",
    author="Виртенбергер В.А.",
    description="Программа «Расход электроэнергии»",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name=target_name)]
)
