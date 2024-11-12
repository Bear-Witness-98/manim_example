import numpy as np
from manim import (
    BLUE,
    DEFAULT_STROKE_WIDTH,
    PI,
    RED,
    Create,
    ThreeDAxes,
    ThreeDScene,
    VGroup,
    VMobject,
    color_gradient,
    linear,
)

EPS = 1e-16


class TestScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=(-2, 2, 0.1),
            y_range=(-2, 2, 0.1),
            z_range=(-0, 2, 0.1),
            depth=8,
        )

        axes.set(width=DEFAULT_STROKE_WIDTH)
        axes.center()

        self.set_camera_orientation(phi=2 * PI / 5, theta=PI / 5)
        self.add(axes)

        radii = np.linspace(0, 2, 20)
        grad = color_gradient([BLUE, RED], len(radii))
        curves = VGroup()
        for r, color in zip(radii, grad):
            curve = VMobject()
            cone = [
                ((r**2) * np.cos(theta), (r**2) * np.sin(theta), r)
                for theta in np.linspace(0, 2 * np.pi, 100)
            ]
            curve.set_points_smoothly([axes.c2p(*point) for point in cone])
            curve.set_stroke(color, 2, opacity=0.9)

            curves.add(curve)

        together = False

        total_runtime = 10
        rate_function = linear
        if together:
            self.play(
                *[Create(curve) for curve in curves],
                run_time=total_runtime,
                rate_func=rate_function,
            )
        else:
            for curve, radius in zip(curves[::-1], radii[::-1]):
                self.play(
                    Create(curve),
                    run_time=total_runtime * radius / sum(radii) + EPS,
                    rate_func=rate_function,
                )
                self.add(axes)
