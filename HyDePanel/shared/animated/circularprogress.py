from fabric.widgets.circularprogressbar import CircularProgressBar

from ..animator import Animator


class AnimatedCircularProgressBar(CircularProgressBar):
    """A circular progress bar widget with animation support."""

    def __init__(self, duration=0.6, bezier_curve=(0.34, 1.56, 0.64, 1.0), **kwargs):
        super().__init__(**kwargs)

        self.animator = (
            Animator(
                # edit the following parameters to customize the animation
                bezier_curve=bezier_curve,
                duration=duration,
                min_value=self.min_value,
                max_value=self.value,
                tick_widget=self,
                notify_value=lambda p, *_: self.set_value(p.value),
            )
            .build()
            .play()
            .unwrap()
        )

    def animate_value(self, value: float):
        self.animator.pause()
        self.animator.min_value = self.value
        self.animator.max_value = value
        self.animator.play()
        return
