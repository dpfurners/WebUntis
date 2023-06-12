from tkinter import ttk
import datetime

import tkcalendar as tkc


class OverallTab(ttk.Frame):
    def __init__(self, parent: ttk.Notebook, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        now = datetime.date.today()
        self.calender = tkc.Calendar(parent, year=now.year, month=now.month, day=now.day)

        self.ov_less = None
        self.ov_hours = None

        self.configure(height=200, width=326)
        self.columnconfigure(index=0, weight=1, minsize=200)
        self.columnconfigure(index=1, weight=1, minsize=126)
        # The rows that are not needed are just there to have a nice formatting
        self.rowconfigure(index=0, weight=1, minsize=33)
        self.rowconfigure(index=1, weight=1, minsize=33)
        self.rowconfigure(index=2, weight=1, minsize=33)
        self.rowconfigure(index=3, weight=1, minsize=33)
        self.rowconfigure(index=4, weight=1, minsize=34)
        self.rowconfigure(index=5, weight=1, minsize=34)

        self.setup_widgets()

        self.updatable = {"overall_l": self.ov_less, "overall_h": self.ov_hours}

    def setup_widgets(self):
        # Overall Lessons
        self_text = ttk.Label(self, text="Overall Lessons:")
        self_text.grid(row=0, column=0, sticky="nw")
        self.ov_less = ttk.Label(self, text="")
        self.ov_less.grid(row=0, column=1, sticky="ne")

        # Overall Hours
        self_desc_text = ttk.Label(self, text="Overall Hours:")
        self_desc_text.grid(row=1, column=0, sticky="nw")
        self.ov_hours = ttk.Label(self, text="")
        self.ov_hours.grid(row=1, column=1, sticky="ne")


class CancelledTab(ttk.Frame):
    def __init__(self, parent: ttk.Notebook, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        now = datetime.date.today()
        self.calender = tkc.Calendar(parent, year=now.year, month=now.month, day=now.day)

        self.cn_less = None
        self.cn_hours = None

        self.configure(height=200, width=326)
        self.columnconfigure(index=0, weight=1, minsize=200)
        self.columnconfigure(index=1, weight=1, minsize=126)
        # The rows that are not needed are just there to have a nice formatting
        self.rowconfigure(index=0, weight=1, minsize=33)
        self.rowconfigure(index=1, weight=1, minsize=33)
        self.rowconfigure(index=2, weight=1, minsize=33)
        self.rowconfigure(index=3, weight=1, minsize=33)
        self.rowconfigure(index=4, weight=1, minsize=34)
        self.rowconfigure(index=5, weight=1, minsize=34)

        self.setup_widgets()

        self.updatable = {"canc_l": self.cn_less, "canc_h": self.cn_hours}

    def setup_widgets(self):
        # Overall Lessons
        self_text = ttk.Label(self, text="Cancelled Lessons:")
        self_text.grid(row=0, column=0, sticky="nw")
        self.cn_less = ttk.Label(self, text="")
        self.cn_less.grid(row=0, column=1, sticky="ne")

        # Overall Hours
        self_desc_text = ttk.Label(self, text="Cancelled Hours:")
        self_desc_text.grid(row=1, column=0, sticky="nw")
        self.cn_hours = ttk.Label(self, text="")
        self.cn_hours.grid(row=1, column=1, sticky="ne")


class SubstitutedTab(ttk.Frame):
    def __init__(self, parent: ttk.Notebook, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        now = datetime.date.today()
        self.calender = tkc.Calendar(parent, year=now.year, month=now.month, day=now.day)

        self.sb_less = None
        self.sb_hours = None

        self.configure(height=200, width=326)
        self.columnconfigure(index=0, weight=1, minsize=200)
        self.columnconfigure(index=1, weight=1, minsize=126)
        # The rows that are not needed are just there to have a nice formatting
        self.rowconfigure(index=0, weight=1, minsize=33)
        self.rowconfigure(index=1, weight=1, minsize=33)
        self.rowconfigure(index=2, weight=1, minsize=33)
        self.rowconfigure(index=3, weight=1, minsize=33)
        self.rowconfigure(index=4, weight=1, minsize=34)
        self.rowconfigure(index=5, weight=1, minsize=34)

        self.setup_widgets()

        self.updatable = {"sb_l": self.sb_less, "sb_h": self.sb_hours}

    def setup_widgets(self):
        # Overall Lessons
        self_text = ttk.Label(self, text="Substituted Lessons:")
        self_text.grid(row=0, column=0, sticky="nw")
        self.sb_less = ttk.Label(self, text="")
        self.sb_less.grid(row=0, column=1, sticky="ne")

        # Overall Hours
        self_desc_text = ttk.Label(self, text="Substituted Hours:")
        self_desc_text.grid(row=1, column=0, sticky="nw")
        self.sb_hours = ttk.Label(self, text="")
        self.sb_hours.grid(row=1, column=1, sticky="ne")


class LessonTab(ttk.Frame):
    def __init__(self, parent: ttk.Notebook, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.ls0 = None
        self.ls1 = None
        self.ls2 = None
        self.ls3 = None
        self.ls4 = None
        self.ls5 = None
        self.ls6 = None
        self.ls7 = None
        self.ls8 = None
        self.ls9 = None

        self.updatable = {}

        self.configure(height=200, width=326)
        self.columnconfigure(index=0, weight=1, minsize=138)
        self.columnconfigure(index=1, weight=1, minsize=138)
        self.columnconfigure(index=2, weight=1, minsize=50)
        self.rowconfigure(index=0, weight=1, minsize=20)
        self.rowconfigure(index=1, weight=1, minsize=20)
        self.rowconfigure(index=2, weight=1, minsize=20)
        self.rowconfigure(index=3, weight=1, minsize=20)
        self.rowconfigure(index=4, weight=1, minsize=20)
        self.rowconfigure(index=5, weight=1, minsize=20)
        self.rowconfigure(index=6, weight=1, minsize=20)
        self.rowconfigure(index=7, weight=1, minsize=20)
        self.rowconfigure(index=8, weight=1, minsize=20)
        self.rowconfigure(index=9, weight=1, minsize=20)

        self.setup_widgets()

    def setup_widgets(self):
        # Hour 0
        ls0_s = ttk.Label(self, text="")
        ls0_s.grid(row=0, column=0, sticky="nw")
        ls0_e = ttk.Label(self, text="")
        ls0_e.grid(row=0, column=1, sticky="nw")
        ls0_n = ttk.Label(self, text="")
        ls0_n.grid(row=0, column=2, sticky="ne")

        self.ls0 = {"start": ls0_s, "end": ls0_e, "name": ls0_n}

        # Hour 1
        ls1_s = ttk.Label(self, text="")
        ls1_s.grid(row=1, column=0, sticky="nw")
        ls1_e = ttk.Label(self, text="")
        ls1_e.grid(row=1, column=1, sticky="nw")
        ls1_n = ttk.Label(self, text="")
        ls1_n.grid(row=1, column=2, sticky="ne")

        self.ls1 = {"start": ls1_s, "end": ls1_e, "name": ls1_n}

        # Hour 2
        ls2_s = ttk.Label(self, text="")
        ls2_s.grid(row=2, column=0, sticky="nw")
        ls2_e = ttk.Label(self, text="")
        ls2_e.grid(row=2, column=1, sticky="nw")
        ls2_n = ttk.Label(self, text="")
        ls2_n.grid(row=2, column=2, sticky="ne")

        self.ls2 = {"start": ls2_s, "end": ls2_e, "name": ls2_n}

        # Hour 3
        ls3_s = ttk.Label(self, text="")
        ls3_s.grid(row=3, column=0, sticky="nw")
        ls3_e = ttk.Label(self, text="")
        ls3_e.grid(row=3, column=1, sticky="nw")
        ls3_n = ttk.Label(self, text="")
        ls3_n.grid(row=3, column=2, sticky="ne")

        self.ls3 = {"start": ls3_s, "end": ls3_e, "name": ls3_n}

        # Hour 4
        ls4_s = ttk.Label(self, text="")
        ls4_s.grid(row=4, column=0, sticky="nw")
        ls4_e = ttk.Label(self, text="")
        ls4_e.grid(row=4, column=1, sticky="nw")
        ls4_n = ttk.Label(self, text="")
        ls4_n.grid(row=4, column=2, sticky="ne")

        self.ls4 = {"start": ls4_s, "end": ls4_e, "name": ls4_n}

        # Hour 5
        ls5_s = ttk.Label(self, text="")
        ls5_s.grid(row=5, column=0, sticky="nw")
        ls5_e = ttk.Label(self, text="")
        ls5_e.grid(row=5, column=1, sticky="nw")
        ls5_n = ttk.Label(self, text="")
        ls5_n.grid(row=5, column=2, sticky="ne")

        self.ls5 = {"start": ls5_s, "end": ls5_e, "name": ls5_n}

        # Hour 6
        ls6_s = ttk.Label(self, text="")
        ls6_s.grid(row=6, column=0, sticky="nw")
        ls6_e = ttk.Label(self, text="")
        ls6_e.grid(row=6, column=1, sticky="nw")
        ls6_n = ttk.Label(self, text="")
        ls6_n.grid(row=6, column=2, sticky="ne")

        self.ls6 = {"start": ls6_s, "end": ls6_e, "name": ls6_n}

        # Hour 7
        ls7_s = ttk.Label(self, text="")
        ls7_s.grid(row=7, column=0, sticky="nw")
        ls7_e = ttk.Label(self, text="")
        ls7_e.grid(row=7, column=1, sticky="nw")
        ls7_n = ttk.Label(self, text="")
        ls7_n.grid(row=7, column=2, sticky="ne")

        self.ls7 = {"start": ls7_s, "end": ls7_e, "name": ls7_n}

        # Hour 8
        ls8_s = ttk.Label(self, text="")
        ls8_s.grid(row=8, column=0, sticky="nw")
        ls8_e = ttk.Label(self, text="")
        ls8_e.grid(row=8, column=1, sticky="nw")
        ls8_n = ttk.Label(self, text="")
        ls8_n.grid(row=8, column=2, sticky="ne")

        self.ls8 = {"start": ls8_s, "end": ls8_e, "name": ls8_n}

        # Hour 9
        ls9_s = ttk.Label(self, text="")
        ls9_s.grid(row=9, column=0, sticky="nw")
        ls9_e = ttk.Label(self, text="")
        ls9_e.grid(row=9, column=1, sticky="nw")
        ls9_n = ttk.Label(self, text="")
        ls9_n.grid(row=9, column=2, sticky="ne")

        self.ls9 = {"start": ls9_s, "end": ls9_e, "name": ls9_n}

        self.updatable = {
            "lesson0": self.ls0,
            "lesson1": self.ls1,
            "lesson2": self.ls2,
            "lesson3": self.ls3,
            "lesson4": self.ls4,
            "lesson5": self.ls5,
            "lesson6": self.ls6,
            "lesson7": self.ls7,
            "lesson8": self.ls8,
            "lesson9": self.ls9,
        }
