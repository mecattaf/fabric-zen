from fabric.widgets.box import Box
from fabric.widgets.shapes import Corner
from fabric.widgets.wayland import WaylandWindow as Window


class MyCorner(Box):
    """A container for a corner shape."""

    def __init__(self, corner, size):
        super().__init__(
            name="corner-container",
            children=Corner(
                name="corner",
                orientation=corner,
                size=size,
            ),
        )


class ScreenCorners(Window):
    """A window that displays all four corners."""

    def __init__(
        self,
        size=20,
    ):
        super().__init__(
            name="corners",
            layer="top",
            anchor="top bottom left right",
            exclusivity="normal",
            pass_through=True,
            visible=False,
            all_visible=False,
        )

        self.all_corners = Box(
            name="all-corners",
            orientation="v",
            h_expand=True,
            v_expand=True,
            h_align="fill",
            v_align="fill",
            children=[
                Box(
                    name="top-corners",
                    orientation="h",
                    h_align="fill",
                    children=[
                        MyCorner("top-left", size),
                        Box(h_expand=True),
                        MyCorner("top-right", size),
                    ],
                ),
                Box(v_expand=True),
                Box(
                    name="bottom-corners",
                    orientation="h",
                    h_align="fill",
                    children=[
                        MyCorner("bottom-left", size),
                        Box(h_expand=True),
                        MyCorner("bottom-right", size),
                    ],
                ),
            ],
        )

        self.add(self.all_corners)

        self.show_all()
