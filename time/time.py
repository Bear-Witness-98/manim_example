# the idea here is to have a time series, and approximate it with multiple
# types of curves. Computing the error in each case

import numpy as np
from manim import BLUE, GRAY, RED, Axes, Create, Scene, VGroup, VMobject, linear


class TimeScene(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-np.pi, 9 * np.pi],
            y_range=[-1.5, 1.5],
            axis_config={"color": GRAY, "include_ticks": False},
            tips=True,
        )
        self.add(axes)

        curves = VGroup()

        curve = VMobject()
        graph = [(x, np.sin(x)) for x in np.linspace(0, 8 * np.pi, 100)]
        curve.set_points_smoothly([axes.c2p(*point) for point in graph])
        curve.set_stroke(BLUE, 2, opacity=0.9)

        curves.add(curve)

        self.play(
            Create(curve),
            run_time=5,
            rate_func=linear,
        )

        curve = VMobject()
        graph = [(x, np.cos(x)) for x in np.linspace(0, 8 * np.pi, 100)]
        curve.set_points_smoothly([axes.c2p(*point) for point in graph])
        curve.set_stroke(RED, 2, opacity=0.9)

        self.play(
            Create(curve),
            run_time=5,
            rate_func=linear,
        )
