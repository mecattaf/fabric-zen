import time
from datetime import datetime

from fabric import Fabricator
from fabric.utils import get_relative_path, invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from gi.repository import Gtk

from services import WeatherService
from shared import ButtonWidget, PopOverWindow, Separator
from utils import BarConfig
from utils.functions import convert_seconds_to_milliseconds
from utils.icons import weather_icons
from utils.widget_utils import text_icon


class WeatherMenu(Box):
    """A menu to display the weather information."""

    def __init__(
        self,
        data,
        **kwargs,
    ):
        super().__init__(
            style_classes="weather-box",
            orientation="v",
            h_expand=True,
            spacing=5,
            **kwargs,
        )

        # Get the current weather
        self.current_weather = data["current"]

        # Get the hourly forecast
        self.hourly_forecast = data["hourly"]

        # Get the sunrise and sunset times
        [self.sunrise_time, self.sunset_time] = [
            data["astronomy"]["sunrise"],
            data["astronomy"]["sunset"],
        ]

        self.weather_icons_dir = get_relative_path("../assets/icons/weather")

        self.current_weather_image = Image(
            self.get_weather_asset(self.current_weather["weatherCode"]),
            size=100,
            style_classes="weather",
        )

        self.title_box = CenterBox(
            style_classes="weather-header-box",
            start_children=(
                Box(
                    children=(
                        self.current_weather_image,
                        Box(
                            orientation="v",
                            v_align="center",
                            children=(
                                Label(
                                    style_classes="condition",
                                    label=f"{self.current_weather['weatherDesc'][0]['value']}",
                                ),
                                Label(
                                    style_classes="temperature",
                                    label=f"{self.current_weather['temp_C']}°C",
                                ),
                            ),
                        ),
                    ),
                )
            ),
            center_children=(
                Box(
                    name="weather-details",
                    orientation="v",
                    spacing=10,
                    v_align="center",
                    children=(
                        Label(
                            style_classes="windspeed",
                            label=f" {self.current_weather['windspeedKmph']} mph",
                        ),
                        Label(
                            style_classes="humidity",
                            label=f"󰖎 {self.current_weather['humidity']}%",
                        ),
                    ),
                )
            ),
            end_children=(
                Box(
                    orientation="v",
                    spacing=10,
                    v_align="center",
                    children=(
                        Label(
                            style_classes="location",
                            label=f"{data['location']}",
                        ),
                        Label(
                            style_classes="feels-like",
                            label=f"Feels Like {self.current_weather['FeelsLikeC']}°C",
                        ),
                    ),
                )
            ),
        )

        # Create a grid to display the hourly forecast

        self.forecast_box = Gtk.Grid(
            row_spacing=10,
            column_spacing=20,
            name="weather-grid",
            visible=True,
        )

        self.children = (
            self.title_box,
            Separator(
                orientation="vertical",
                name="weather-separator",
            ),
            self.forecast_box,
        )

        invoke_repeater(
            convert_seconds_to_milliseconds(3600),
            self.update_widget,
            initial_call=True,
        )

    def update_widget(self):
        current_time = int(time.strftime("%H00"))

        next_values = self.hourly_forecast[:4]

        if current_time > 1200:
            next_values = self.hourly_forecast[4:8]

        # show next 4 hours forecast
        for col in range(4):
            column_data = next_values[col]

            hour = Label(
                style_classes="weather-forecast-time",
                label=f"{self.convert_to_12hr_format(column_data['time'])}",
                h_align="center",
            )
            icon = Image(
                image_file=self.get_weather_asset(
                    column_data["weatherCode"],
                    self.convert_to_12hr_format(column_data["time"]),
                ),
                size=70,
                h_align="center",
                h_expand=True,
                style_classes="weather-forecast-icon",
            )

            temp = Label(
                style_classes="weather-forecast-temp",
                label=f"{column_data['tempC']}°C",
                h_align="center",
            )
            self.forecast_box.attach(hour, col, 0, 1, 1)
            self.forecast_box.attach(icon, col, 1, 1, 1)
            self.forecast_box.attach(temp, col, 2, 1, 1)

    # wttr.in time are in 300,400...2100 format , we need to convert it to 4:00...21:00
    def convert_to_12hr_format(self, time: str) -> str:
        time = int(time)
        hour = time // 100  # Get the hour (e.g., 1200 -> 12)
        minute = time % 100  # Get the minutes (e.g., 1200 -> 00)

        # Convert to 12-hour format
        period = "AM" if hour < 12 else "PM"

        # Adjust hour for 12-hour format
        if hour == 0:
            hour = 12
        elif hour > 12:
            hour -= 12

        # Format the time as a string
        return f"{hour}:{minute:02d} {period}"

    def check_if_day(self, current_time: str | None = None) -> str:
        time_format = "%I:%M %p"

        if current_time is None:
            current_time = datetime.now().strftime(time_format)

        current_time_obj = datetime.strptime(current_time, time_format)
        sunrise_time_obj = datetime.strptime(self.sunrise_time, time_format)
        sunset_time_obj = datetime.strptime(self.sunset_time, time_format)

        # Compare current time with sunrise and sunset
        return sunrise_time_obj <= current_time_obj < sunset_time_obj

    def get_weather_asset(self, code: int, time: str | None = None) -> str:
        is_day = self.check_if_day(time)
        image_name = "image" if is_day else "image-night"
        return f"{self.weather_icons_dir}/{weather_icons[str(code)][image_name]}.svg"


class WeatherWidget(ButtonWidget):
    """A widget to display the current weather."""

    def __init__(
        self,
        widget_config: BarConfig,
        bar,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            widget_config,
            name="weather-button",
            **kwargs,
        )

        self.weather_service = WeatherService().get_default()

        self.config = widget_config["weather"]

        self.bar = bar

        self.box = Box(
            name="weather",
            style_classes="panel-box",
        )

        self.children = self.box

        self.weather_icon = text_icon(
            icon="",
            size="15px",
            props={
                "style_classes": "weather-bar-icon",
            },
        )

        self.weather_fabricator = Fabricator(poll_from=self.weather_poll, stream=True)

        self.weather_label = Label(
            label="Fetching weather...",
            style_classes="panel-text",
        )
        self.box.children = (self.weather_icon, self.weather_label)

        # Set up a fabricator to call the update_label method at specified intervals
        self.weather_fabricator.connect("changed", self.update_ui)

    def weather_poll(self, fabricator):
        while True:
            yield {
                "weather": self.weather_service.simple_weather_info(
                    self.config["location"]
                )
            }
            time.sleep(self.config["interval"] / 1000)

    def update_ui(self, fabricator, value):
        # Update the label with the weather icon and temperature in the main thread
        res = value.get("weather")
        current_weather = res["current"]
        text_icon = weather_icons[current_weather["weatherCode"]]["icon"]
        self.weather_label.set_label(f"{current_weather['FeelsLikeC']}°C")
        self.weather_icon.set_label(text_icon)

        # Update the tooltip with the city and weather condition if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"{res['location']}, {current_weather['weatherDesc'][0]['value']}"
            )

        popup = PopOverWindow(
            parent=self.bar,
            name="date-menu-popover",
            child=(WeatherMenu(data=res)),
            visible=False,
            all_visible=False,
            margin="-18px 0 0 0",
            pointing_to=self,
        )

        self.connect(
            "clicked",
            lambda *_: popup.set_visible(not popup.get_visible()),
        )
