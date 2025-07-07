import numpy as np
from manim import (
    BLUE,
    DEFAULT_STROKE_WIDTH,
    LEFT,
    PI,
    RED,
    RIGHT,
    TAU,
    UL,
    Circle,
    Create,
    Dot,
    Scene,
    Surface,
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
from scipy.integrate import solve_ivp


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

        # Add equations to fixed frame
        self.add_fixed_in_frame_mobjects(equations)
        self.play(Write(equations))

        # Begin camera rotation
        self.begin_ambient_camera_rotation(rate=0.25, about="theta")

        # compute solutions to the differential equation
        # Compute a set of solutions
        epsilon = 1
        evolution_time = 30
        n_points = 5
        states = [[10, 10, 10 + n * epsilon] for n in range(n_points)]
        colors = color_gradient([BLUE, RED], len(states))

        curves = VGroup()
        for state, color in zip(states, colors):
            # compute the evolution points for the initial conditions
            points = ode_solution_points(lorenz_system, state, evolution_time)
            # convert to manim object and set style
            curve = VMobject()
            curve.set_points_smoothly([axes.c2p(*point) for point in points])
            curve.set_stroke(color, 2, opacity=0.9)
            # add to Vgroup
            curves.add(curve)
            # self.play(Create(curve), run_time=20)

        # self.add(curves)
        self.play(
            *[Create(curve) for curve in curves],
            run_time=30,
            rate_func=linear,
        )
        # Stop camera rotation at the end
        self.stop_ambient_camera_rotation(about="theta")

        surface = Surface(
            lambda u, v: axes.c2p(*self.func(u, v)),
            u_range=[-40, 40],
            v_range=[-40, 40],
            resolution=8,
        )

        surface2 = Surface(
            lambda u, v: axes.c2p(*self.func2(u, v)),
            u_range=[-40, 40],
            v_range=[-40, 40],
            resolution=8,
        )

        self.play(Create(surface))
        self.play(Create(surface2))

        self.wait(5)

    def func(self, u, v):
        return np.array([u, v, 0])

    def func2(self, u, v):
        return np.array([u, v, 2 * u - v])


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
