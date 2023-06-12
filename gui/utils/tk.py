import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from dateutil.parser import parse

from .api import load_day, load_day_info
from .tabs import OverallTab, CancelledTab, SubstitutedTab, LessonTab


def get_data(inp: ttk.Entry, labels: dict[dict, any], root: tk.Tk) -> None:
    date = parse(inp.get())
    if date.time() == datetime.datetime.min.time():
        date = date.date()
    day = load_day(date)
    day_info = load_day_info(date)
    if reason := day.get("reason"):
        messagebox.showinfo("No Data", f"You choose a date that is a {reason}")
        inp.delete(0, len(inp.get()))
        return

    # Update Overall Tab
    labels.get("overa")["overall_l"].config(text=day_info["lesson_info"]["overall_lessons"])
    labels.get("overa")["overall_h"].config(text=day_info["lesson_info"]["overall_hours"])

    # Update Cancelled Tab
    labels.get("canc")["canc_l"].config(text=day_info["lesson_info"]["cancelled_lessons"])
    labels.get("canc")["canc_h"].config(text=day_info["lesson_info"]["cancelled_hours"])

    # Update Substituted Tab
    labels.get("subs")["sb_l"].config(text=day_info["lesson_info"]["substituted_lessons"])
    labels.get("subs")["sb_h"].config(text=day_info["lesson_info"]["substituted_hours"])

    for ind, lesson in enumerate(labels.get("lessons").keys()):
        try:
            day_info["lesson_overview"][ind]
            labels.get("lessons")[lesson]["start"].config(text="")
            labels.get("lessons")[lesson]["end"].config(text="")
            labels.get("lessons")[lesson]["name"].config(text=day_info["lesson_overview"][ind])
        except IndexError:
            pass
    root.update()


def setup_widgets(root: tk.Tk, key: str | None = None) -> None:
    update_labels = {}

    root.resizable(False, False)
    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=1)
    root.columnconfigure(index=2, weight=1)
    root.rowconfigure(index=0, weight=1, minsize=30)
    root.rowconfigure(index=1, weight=1)
    root.rowconfigure(index=2, weight=1)

    inp = ttk.Entry(root)
    inp.grid(row=0, column=0, columnspan=2, sticky="nwe")
    button = ttk.Button(root, text="Load_Data")
    button.grid(row=0, column=2, sticky="nw")

    # Notebook
    notebook = ttk.Notebook()
    notebook.grid(row=1, column=0, columnspan=3, rowspan=2, sticky="nw")

    # Weather Tab
    overa = OverallTab(notebook)
    notebook.add(overa, text="Overall")
    update_labels["overa"] = overa.updatable

    # Temperature Tab
    canc = CancelledTab(notebook)
    notebook.add(canc, text="Cancelled")
    update_labels["canc"] = canc.updatable

    # Wind Tab
    subs = SubstitutedTab(notebook)
    notebook.add(subs, text="Substituted")
    update_labels["subs"] = subs.updatable

    # Additional Tab
    lessons = LessonTab(notebook)
    notebook.add(lessons, text="Lessons")
    update_labels["lessons"] = lessons.updatable

    # Bind the button
    button.bind("<Button-1>", lambda event: get_data(inp, update_labels, root))


def initialize_tk(root: tk.Tk = None, theme: str | None = None, key: str | None = None) -> tk.Tk:
    if root is None:
        root = tk.Tk()
    root.title("Weather App")
    root.option_add("*tearOff", False)  # This is always a good idea

    # Center the window
    root.minsize(root.winfo_width(), root.winfo_height())
    x_coordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_coordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_coordinate, y_coordinate))

    # Create a style
    if theme is not None:
        style = ttk.Style(root)

        # Import the tcl file
        root.tk.call("source", "C:/_path/themes/tkinter/forest/forest-dark.tcl")

        # Set the theme with the theme_use method
        style.theme_use(theme)
        setup_widgets(root)
        return root
    setup_widgets(root, key)
    return root
