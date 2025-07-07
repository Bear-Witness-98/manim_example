# the idea here is to have a time series, and approximate it with multiple
# types of curves. Computing the error in each case

import numpy as np
from manim import (
    BLUE,
    DOWN,
    GRAY,
    GREEN,
    RED,
    ApplyFunction,
    Axes,
    Create,
    Scene,
    StealthTip,
    Tex,
    Text,
    Transform,
    VGroup,
    VMobject,
    linear,
)


class TimeScene(Scene):
    def construct(self):
        # set up axes with appropriate scale
        axes = Axes(
            x_range=[-np.pi, 9 * np.pi, np.pi],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={
                "color": GRAY,
                "tip_shape": StealthTip,
                "include_ticks": True,
                "font_size": 15,
            },
            tips=True,
        )
        # axes.add_coordinates()
        labels = axes.get_axis_labels(
            Tex(R"time ($\theta$)").scale(0.2), Text("voltage (V)").scale(0.2)
        )
        values_x = [
            (k * np.pi, rf"{k}$\pi$")
            for k in [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ]
        x_axis_labels = VGroup()
        for x_val, x_tex in values_x:
            tex = Tex(x_tex, font_size=15)
            tex.next_to(axes.c2p(x_val, 0), DOWN)  # Put tex on the position
            self.add(tex)  # Add tex in graph
            x_axis_labels.add(tex)
        self.add(axes, *x_axis_labels, labels)

        # add curves to the graph
        curves = VGroup()
        curve = VMobject()
        graph = np.array([(x, np.sin(x)) for x in np.linspace(0, 8 * np.pi, 100)])
        curve.set_points_smoothly([axes.c2p(*point) for point in graph])
        curve.set_stroke(BLUE, 2, opacity=0.9)
        curves.add(curve)

        self.play(
            Create(curve),
            run_time=5,
            rate_func=linear,
        )

        curve2 = VMobject()
        graph2 = [(x, np.cos(x)) for x in np.linspace(0, 8 * np.pi, 100)]
        curve2.set_points_smoothly([axes.c2p(*point) for point in graph2])
        curve2.set_stroke(RED, 2, opacity=0.9)

        self.play(
            Create(curve2),
            run_time=5,
            rate_func=linear,
        )

        curve3 = VMobject()
        graph3 = np.array(
            [(x, np.cos(x) - np.sin(x)) for x in np.linspace(0, 8 * np.pi, 100)]
        )
        curve3.set_points_smoothly([axes.c2p(*point) for point in graph3])
        curve3.set_stroke(RED, 2, opacity=0.9)

        def vertical_transform(point):
            x, y, z = point
            return np.array(
                [x, np.cos((x / np.pi) + 1.5) - np.sin((x / np.pi) + 1.5), z]
            )

        curve4 = curve2.copy().apply_function(vertical_transform)

        self.play(Transform(curve, curve4))

        self.wait()
