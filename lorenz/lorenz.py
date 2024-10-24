# from manim import *
# from scipy.integrate import odeint
# from scipy.integrate import solve_ivp


# def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
#     x, y, z = state
#     dxdt = sigma * (y - x)
#     dydt = x * (rho - z) - y
#     dzdt = x * y - beta * z
#     return [dxdt, dydt, dzdt]


# def ode_solution_points(function, state0, time, dt=0.01):
#     solution = solve_ivp(
#         function,
#         t_span=(0, time),
#         y0=state0,
#         t_eval=np.arange(0, time, dt)
#     )
#     return solution.y.T


# def for_later():
#     tail = VGroup(
#         TracingTail(dot, time_traced=3).match_color(dot)
#         for dot in dots
#     )


# class LorenzAttractor(InteractiveScene):
#     def construct(self):
#         # Set up axes
#         axes = ThreeDAxes(
#             x_range=(-50, 50, 5),
#             y_range=(-50, 50, 5),
#             z_range=(-0, 50, 5),
#             width=16,
#             height=16,
#             depth=8,
#         )
#         axes.set_width(FRAME_WIDTH)
#         axes.center()

#         self.frame.reorient(43, 76, 1, IN, 10)
#         self.frame.add_updater(lambda m, dt: m.increment_theta(dt * 3 * DEGREES))
#         self.add(axes)

#         # Add the equations
#         equations = Tex(
#             R"""
#             \begin{aligned}
#             \frac{\mathrm{d} x}{\mathrm{~d} t} & =\sigma(y-x) \\
#             \frac{\mathrm{d} y}{\mathrm{~d} t} & =x(\rho-z)-y \\
#             \frac{\mathrm{d} z}{\mathrm{~d} t} & =x y-\beta z
#             \end{aligned}
#             """,
#             t2c={
#                 "x": RED,
#                 "y": GREEN,
#                 "z": BLUE,
#             },
#             font_size=30
#         )
#         equations.fix_in_frame()
#         equations.to_corner(UL)
#         equations.set_backstroke()
#         self.play(Write(equations))

#         # Compute a set of solutions
#         epsilon = 1e-5
#         evolution_time = 30
#         n_points = 10
#         states = [
#             [10, 10, 10 + n * epsilon]
#             for n in range(n_points)
#         ]
#         colors = color_gradient([BLUE_E, BLUE_A], len(states))

#         curves = VGroup()
#         for state, color in zip(states, colors):
#             points = ode_solution_points(lorenz_system, state, evolution_time)
#             curve = VMobject().set_points_smoothly(axes.c2p(*points.T))
#             curve.set_stroke(color, 1, opacity=0.25)
#             curves.add(curve)

#         curves.set_stroke(width=2, opacity=1)

#         # Display dots moving along those trajectories
#         dots = Group(GlowDot(color=color, radius=0.25) for color in colors)

#         def update_dots(dots, curves=curves):
#             for dot, curve in zip(dots, curves):
#                 dot.move_to(curve.get_end())

#         dots.add_updater(update_dots)

#         tail = VGroup(
#             TracingTail(dot, time_traced=3).match_color(dot)
#             for dot in dots
#         )

#         self.add(dots)
#         self.add(tail)
#         curves.set_opacity(0)
#         self.play(
#             *(
#                 ShowCreation(curve, rate_func=linear)
#                 for curve in curves
#             ),
#             run_time=evolution_time,
#         )

import numpy as np
from manim import (
    BLUE,
    BLUE_A,
    BLUE_E,
    DEFAULT_STROKE_WIDTH,
    DEGREES,
    GREEN,
    IN,
    LEFT,
    PI,
    RED,
    RIGHT,
    UL,
    Circle,
    Create,
    Dot,
    Group,
    Scene,
    Tex,
    ThreeDAxes,
    ThreeDScene,
    TracedPath,
    VGroup,
    VMobject,
    Write,
    color_gradient,
    linear,
)
from scipy.integrate import odeint, solve_ivp


def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function, t_span=(0, time), y0=state0, t_eval=np.arange(0, time, dt)
    )
    return solution.y.T


class LorenzAttractor(ThreeDScene):
    def construct(self):
        # Set up axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(-0, 50, 5),
            depth=8,
        )

        axes.set_width(DEFAULT_STROKE_WIDTH)
        axes.center()

        # camera still cant move :F
        self.set_camera_orientation(phi=2 * PI / 5, theta=PI / 5)
        # self.frame.reorient(43, 76, 1, IN, 10)
        # self.frame.add_updater(lambda m, dt: m.increment_theta(dt * 3 * DEGREES))
        self.add(axes)

        # Add the equations
        equations = Tex(
            R"""
                This a very profound and deep text \\
                $ \frac{\mathrm{d} x}{\mathrm{d} y} = \sigma(y-x) $ \\
                $ \frac{\mathrm{d} y}{\mathrm{~d} t} = x(\rho-z) - y $ \\
                $ \frac{\mathrm{d} z}{\mathrm{~d} t}  = xy - \beta z $
            """,
            # god only knows how to use this below:
            # tex_to_color_map={
            #     "x": RED,
            #     "y": GREEN,
            #     "z": BLUE,
            # },
            font_size=30,
        )

        equations.to_corner(UL)
        equations.set_background_stroke()
        self.move_camera(
            phi=2 * PI / 5,
            theta=-PI / 5,
            run_time=7,
        )

        self.begin_ambient_camera_rotation(rate=1, about="theta")

        self.add_fixed_in_frame_mobjects(equations)
        self.play(Write(equations))

        self.stop_ambient_camera_rotation(about="theta")

        # compute solutions to the differential equation
        # Compute a set of solutions
        epsilon = 1e-5
        evolution_time = 30
        n_points = 10
        states = [[10, 10, 10 + n * epsilon] for n in range(n_points)]
        colors = color_gradient([BLUE_E, BLUE_A], len(states))

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            curve = VMobject().set_points_smoothly(points)
            curve.set_stroke(color, 1, opacity=0.25)
            curves.add(curve)

        curves.set_stroke(width=2, opacity=1)

        # Display dots moving along those trajectories
        sth = [Dot(color=color, radius=0.25) for color in colors]
        dots = Group(*sth)

        def update_dots(dots: Group, curves=curves):
            for dot, curve in zip(dots.submobjects, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)

        sth_else = [
            TracedPath(dot, dissipating_time=3).match_color(dot) for dot in dots
        ]
        tail = VGroup(*sth_else)

        self.add(dots)
        self.add(tail)
        curves.set_opacity(0)
        # import ipdb

        # ipdb.set_trace()
        self.play(
            [dots for dots in curve for curve in curves],
            run_time=evolution_time,
        )


class TracedPathExample(Scene):
    def construct(self):
        circ = Circle(color=RED).shift(4 * LEFT)
        dot = Dot(color=RED).move_to(circ.get_start())
        rolling_circle = VGroup(circ, dot)
        trace = TracedPath(circ.get_start)
        rolling_circle.add_updater(lambda m: m.rotate(-0.3))
        self.add(trace, rolling_circle)
        self.play(rolling_circle.animate.shift(8 * RIGHT), run_time=4, rate_func=linear)


class DissipatingPathExample(Scene):
    def construct(self):
        a = Dot(RIGHT * 2)
        b = TracedPath(a.get_center, dissipating_time=0.5, stroke_opacity=[0, 1])
        self.add(a, b)
        self.play(a.animate(path_arc=PI / 4).shift(LEFT * 2))
        self.play(a.animate(path_arc=-PI / 4).shift(LEFT * 2))
        self.wait()
