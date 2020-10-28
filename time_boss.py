from time import perf_counter
from typing import List, Dict
import numpy as np

class TimeBoss:
    """
    Implements timing via context managers.

    Usage:
    ------
        ```
        with TimeBoss("timer1"):
            # computation
            with TimeBoss("timer2"):
                # more computation
        TimeBoss.result()
    """

    root_timers: List["TimeBoss"] = []
    timer_stack: List["TimeBoss"] = []
    all_timers: Dict[str, "TimeBoss"] = {}

    def __init__(self, name: str):
        if name in TimeBoss.all_timers:
            self.__dict__ = TimeBoss.all_timers[name].__dict__
            return

        self.sub_timers: List["TimeBoss"] = []

        self.timings: List[float] = []
        self.n_calls = 0

        self.name = name
        self._start = 0

        # if the stack is not empty, add ourselves on top. Otherwise add ourselves to root timers.
        if TimeBoss.timer_stack:
            parent_timer = TimeBoss.timer_stack[-1]
            # Add sourselves as subtimer to the timer currently on the stack.
            parent_timer.add_timer(self)
        else:
            TimeBoss.root_timers.append(self)
        TimeBoss.all_timers[name] = self

    def __enter__(self):
        self._start = perf_counter()
        TimeBoss.timer_stack.append(self)

    def __exit__(self, type, value, traceback):
        dt = perf_counter() - self._start
        self.timings.append(dt)
        self.n_calls += 1
        TimeBoss.timer_stack.pop()

    def add_timer(self, timer: "TimeBoss"):
        """Add a subtimer"""

        self.sub_timers.append(timer)

    @staticmethod
    def print_res(timer: "TimeBoss", unit: str, level:int):
        """Pretty print the timing result"""

        unit_conv = {"s": 1, "ms": 1E3, "mus": 1E6}
        if not unit in unit_conv:
            unit = "s"
        unitf = unit_conv[unit]

        tot_time = sum(timer.timings) * unitf
        mean_time = np.average(timer.timings) * unitf
        std_time = np.std(timer.timings) * unitf
        res_string =  f"{tot_time:.3f} elapsed in {timer.n_calls} calls ({mean_time:.3f} +- {std_time:.3f} per call) [{unit}]"
        level_str = "\t"*level
        print(f"{level_str}{timer.name}: {res_string}")

    def _result(self, unit: str, level=0):
        """Helper function to print the results of this timer and recursively of all subtimers"""
        self.print_res(self, unit, level)
        for subt in self.sub_timers:
            subt._result(unit, level + 1)

    @classmethod
    def result(cls, unit="s"):
        """Print the results of all timers"""
        for timer in cls.root_timers:
            timer._result(unit)
