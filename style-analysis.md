# Style Comparison Across Fabric-Based Projects

## Introduction

This document provides a comprehensive analysis of coding patterns, architecture decisions, and styling approaches used in three Fabric-based shell projects: Ax-Shell, Modus, and HyDePanel. The goal is to identify patterns, strengths, and weaknesses in each implementation to establish a unified style guide for our Sway implementation.

## Code Organization

### Ax-Shell

Ax-Shell follows a hierarchical structure with clear separation between different components:

- Main application entry point in `main.py` initializes core components
- Modules are organized in a dedicated `modules/` directory
- Each UI component is defined in its own file (e.g., `bar.py`, `dock.py`)
- Helper utilities and constant definitions are centralized in `utils/`
- Assets are stored in a dedicated `assets/` directory
- Configuration is managed in `config/`

Example directory structure:
```
Ax-Shell/
├── assets/
│   ├── fonts/
│   ├── icons/
│   └── wallpaper/
├── config/
│   ├── assets/
│   └── config.py
├── main.py
├── modules/
│   ├── bar/
│   ├── dock.py
│   ├── emoji.py
│   ├── kanban.py
│   ├── launcher/
│   ├── notification_popup.py
│   ├── osd.py
│   └── tools.py
├── services/
│   ├── brightness.py
│   ├── mpris.py
│   ├── network.py
│   └── screen_record.py
├── styles/
└── utils/
    ├── colors.py
    ├── functions.py
    ├── hyprland_monitor.py
    ├── icon_resolver.py
    └── icons.py
```

### Modus

Modus has a simpler, flatter structure with a focus on modularity:

- Modules are directly under `modules/` with minimal nesting
- Each module is self-contained and focused on a specific functionality
- Services are kept in a dedicated `services/` directory
- Configuration is handled through a centralized JSON file
- Utility functions are collected in a flat `utils/` directory

Example directory structure:
```
Modus/
├── assets/
│   ├── icons/
│   ├── logo.svg
│   ├── screenshots/
│   └── wallpaper/
├── config/
│   ├── assets/
│   │   ├── config.json
│   │   └── modus.json
│   ├── config.py
│   └── scripts/
├── install.sh
├── main.py
├── modules/
│   ├── bar/
│   │   ├── bar.py
│   │   └── components/
│   ├── dock.py
│   ├── launcher/
│   │   └── launcher.py
│   ├── notification_popup.py
│   └── osd.py
├── services/
│   ├── brightness.py
│   ├── network.py
│   └── screen_record.py
└── utils/
    ├── colors.py
    ├── custom_image.py
    ├── icon_resolver.py
    └── icons.py
```

### HyDePanel

HyDePanel has the most structured organization, with a clear division between different types of modules:

- Core panel functionality is organized in a dedicated `bar/` directory
- Individual modules are organized by functionality within `widgets/`
- Services and utilities are more granularly divided
- Configuration is based on JSON with an extensive schema
- The `init.sh` script handles dependencies management and virtual environment setup

Example directory structure:
```
HyDePanel/
├── bar/
│   ├── components/
│   │   ├── battery.py
│   │   ├── metric.py
│   │   ├── system_indicators.py
│   │   ├── updates.py
│   │   └── workspace.py
│   └── panel.py
├── example/
│   └── config.json
├── init.sh
├── main.py
├── modules/
│   ├── bluetooth.py
│   ├── calendar.py
│   ├── cliphist.py
│   ├── hypr_idle.py
│   └── power_button.py
├── services/
│   ├── audio.py
│   ├── bluetooth.py
│   ├── mpris.py
│   └── network.py
├── styles/
│   └── themes/
├── widgets/
│   ├── battery.py
│   ├── bluetooth.py
│   ├── brightness.py
│   ├── calendar.py
│   ├── media.py
│   ├── quick_settings/
│   ├── taskbar.py
│   ├── volume.py
│   └── workspaces.py
└── utils/
    ├── colors.py
    ├── functions.py
    ├── icons.py
    └── widget_utils.py
```

## Coding Conventions

### Ax-Shell

Ax-Shell follows Python conventions with some unique characteristics:

1. **Class Structure**:
   - Classes are highly component-oriented
   - Constructor parameters are extensively used
   - Child widgets are often defined within the constructor

2. **Naming Conventions**:
   - `snake_case` for methods and variables
   - `CamelCase` for classes
   - Descriptive names that indicate widget type (e.g., `BluetoothButton`)

3. **Comments and Documentation**:
   - Moderate commenting
   - Function-level docstrings in some places
   - Limited module-level documentation

4. **Error Handling**:
   - Minimal explicit error handling
   - Most errors are passed up the call stack

5. **Event Handling**:
   - Heavy use of lambda functions for callbacks
   - Signal connections defined inline with widget creation

Example from `bar.py`:
```python
self.date_time = DateTime(name="date-time", formatters=["%H:%M"], h_align="center", v_align="center")

self.button_apps = Button(
    name="button-bar",
    on_clicked=lambda *_: self.search_apps(),
    child=Label(
        name="button-bar-label",
        markup=icons.apps
    )
)
self.button_apps.connect("enter_notify_event", self.on_button_enter)
self.button_apps.connect("leave_notify_event", self.on_button_leave)
```

### Modus

Modus employs a more functional approach with emphasis on readability:

1. **Class Structure**:
   - Smaller classes with focused responsibility
   - Heavier use of helper methods
   - More explicit widget hierarchies

2. **Naming Conventions**:
   - Consistent `snake_case` for methods and variables
   - `CamelCase` for classes
   - Shorter but still descriptive names

3. **Comments and Documentation**:
   - More extensive commenting, especially for complex functionality
   - More consistent use of docstrings
   - Better explanation of non-obvious code

4. **Error Handling**:
   - More explicit try/except blocks
   - Better logging of errors
   - Graceful fallbacks for failed operations

5. **Event Handling**:
   - More dedicated handler methods instead of lambdas
   - Signal connections often grouped together
   - Better organization of event flow

Example from `weather.py`:
```python
def fetch_weather(self):
    GLib.Thread.new("weather-fetch", self._fetch_weather_thread, None)
    return True

def _fetch_weather_thread(self, data):
    location = self.get_location()
    if location:
        url = f"https://wttr.in/{urllib.parse.quote(location)}?format=%c+%t"
    else:
        url = "https://wttr.in/?format=%c+%t"
    try:
        response = self.session.get(url, timeout=5)
        if response.ok:
            weather_data = response.text.strip()
            if "Unknown" in weather_data:
                GLib.idle_add(self.set_visible, False)
            else:
                GLib.idle_add(self.set_visible, True)
                GLib.idle_add(self.label.set_label, weather_data.replace(" ", ""))
        else:
            GLib.idle_add(self.label.set_markup, f"{icons.cloud_off} Unavailable")
            GLib.idle_add(self.set_visible, False)
    except Exception as e:
        print(f"Error fetching weather: {e}")
        GLib.idle_add(self.label.set_markup, f"{icons.cloud_off} Error")
        GLib.idle_add(self.set_visible, False)
```

### HyDePanel

HyDePanel shows the most structured code organization with consistent patterns:

1. **Class Structure**:
   - Strong adherence to single responsibility principle
   - Better separation between UI and logic
   - More consistent widget hierarchy patterns

2. **Naming Conventions**:
   - Very consistent `snake_case` for methods and variables
   - `CamelCase` for classes
   - Clear naming convention for different types of components

3. **Comments and Documentation**:
   - Comprehensive docstrings for classes and methods
   - Clear explanations of parameters and return values
   - Module-level documentation explaining purpose

4. **Error Handling**:
   - Structured error handling with specific exception types
   - Extensive logging with different severity levels
   - Better recovery strategies for failures

5. **Event Handling**:
   - Consistent use of dedicated handler methods
   - Clear separation between UI events and business logic
   - Better management of event propagation

Example from `volume.py`:
```python
class VolumeWidget(EventBoxWidget):
    """a widget that displays and controls the volume."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(
            widget_config,
            events=["scroll", "smooth-scroll", "enter-notify-event"],
            **kwargs,
        )

        # Initialize the audio service
        self.audio = audio_service

        self.config = widget_config["volume"]

        # Create a circular progress bar to display the volume level
        self.progress_bar = CircularProgressBar(
            style_classes="overlay-progress-bar",
            pie=True,
            size=24,
        )

        self.volume_label = Label(visible=False, style_classes="panel-text")

        self.icon = text_icon(
            icon=volume_text_icons["medium"],
            size=self.config["icon_size"],
            props={
                "style_classes": "panel-icon overlay-icon",
            },
        )

        # Create an event box to handle scroll events for volume control
        self.box = Box(
            spacing=4,
            name="volume",
            style_classes="panel-box",
            children=(
                Overlay(child=self.progress_bar, overlays=self.icon, name="overlay"),
                self.volume_label,
            ),
        )
        # Connect the audio service to update the progress bar on volume change
        self.audio.connect("notify::speaker", self.on_speaker_changed)
        # Connect the event box to handle scroll events
        self.connect("scroll-event", self.on_scroll)

        # Add the event box as a child
        self.add(self.box)

        if self.config["label"]:
            self.volume_label.show()
```

## CSS Styling Approach

### Ax-Shell

Ax-Shell uses a minimalist styling approach with a focus on functional design:

1. **CSS Organization**:
   - CSS is loaded dynamically through the application
   - Uses a combination of direct styling and class-based styles
   - Style is applied uniformly to reduce visual discontinuity

2. **Visual Design**:
   - Relatively flat design with minimal shadows
   - Consistent rounded corners on UI elements
   - Muted color palette with clear accent colors

3. **Animation**:
   - Minimal animations, mostly for transitions
   - Simple effects for hover states
   - Consistent timing for transitions

4. **Responsiveness**:
   - Limited responsiveness considerations
   - Fixed sizing for many elements
   - Some adaptability through percentage-based sizing

Example CSS from Ax-Shell:
```css
#bar-inner {
  padding: 4px;
  border: solid 2px;
  border-color: var(--border-color);
  background-color: var(--window-bg);
  min-height: 28px;
}

#workspaces {
  padding: 6px;
  min-width: 0px;
  background-color: var(--module-bg);
}

#workspaces > button {
  padding: 0px 8px;
  transition: padding 0.05s steps(8);
  background-color: var(--ws-inactive);
}
```

### Modus

Modus employs a more visually rich styling approach:

1. **CSS Organization**:
   - Clean separation of colors and structural styling
   - Extensive use of CSS variables for theming
   - More structured hierarchy of styling rules

2. **Visual Design**:
   - More depth with subtle shadows and gradients
   - Consistent use of rounded corners and padding
   - Richer color palette with carefully selected accent colors

3. **Animation**:
   - More extensive use of animations for state changes
   - Smooth transitions between UI states
   - Better visual feedback for user interactions

4. **Responsiveness**:
   - Better handling of different screen sizes
   - More flexible layouts using CSS Grid and Flexbox
   - Dynamic resizing of components based on content

Example CSS from Modus:
```css
#window-inner {
    border: solid 2px;
    border-color: var(--color11);
    background-color: var(--window-bg);
    border-radius: 100px;
    border-radius: 12px;
    padding: 10px;
}

#date-time > label {
    font-weight: 900;
    font-size: 28px;
}

#header {
    border: solid 1px var(--border-color);
    border-radius: 8px;
    box-shadow: 0px 18px 23px -6px rgba(0, 0, 0, 0.75);
    background: linear-gradient(90deg,
            alpha(var(--color11), 0.2),
            alpha(var(--background), 0.2),
            var(--module-bg));
}
```

### HyDePanel

HyDePanel has the most sophisticated styling approach:

1. **CSS Organization**:
   - Well-structured CSS with clear organization
   - Extensive use of CSS variables and themes
   - Components have consistent styling rules

2. **Visual Design**:
   - Polished design with attention to detail
   - Consistent use of spacing, borders, and colors
   - Well-designed visual hierarchy

3. **Animation**:
   - Thoughtful use of animations to enhance usability
   - Consistent timing and easing functions
   - Animations support the interface rather than distract

4. **Responsiveness**:
   - Better adaptability to different screen sizes
   - More fluid layouts that adjust to content
   - Consistent appearance across different configurations

Example CSS from HyDePanel:
```css
#notification {
    padding: 0.8rem;
    border: solid 1px var(--border-color);
    border-radius: 1rem;
    background-color: var(--background);
}

#notification .summary {
    font-size: 20px;
    font-weight: bold;
}

#notification .body {
    color: darker(var(--foreground));
    font-weight: normal;
}

button {
    padding: 0.6rem;
    font-weight: 600;
    border-radius: 3rem;
    background-color: var(--button-color);
}

button:hover {
    background-color: lighter(var(--button-color));
}
```

## Component Architecture

### Ax-Shell

Ax-Shell uses a component-based architecture with these characteristics:

1. **Widget Hierarchy**:
   - Deep nesting of widgets with many layers
   - Heavy use of boxes for layout
   - Complex widget trees for advanced UI elements

2. **Component Composition**:
   - Components are composed through inheritance and containment
   - UI elements are often defined entirely in constructors
   - Limited separation between presentation and logic

3. **State Management**:
   - State is typically managed within the component
   - Limited use of centralized state management
   - Observable properties are used for reactivity

4. **Modularity**:
   - Components are relatively self-contained
   - Some interdependencies between components
   - Services are used for shared functionality

Example component architecture:
```python
class Bar(Window):
    def __init__(self):
        super().__init__(...)
        
        self.workspaces = ...
        self.button_tools = ...
        self.systray = ...
        self.date_time = ...
        
        self.bar_inner = CenterBox(
            start_children=Box(
                children=[
                    self.button_apps,
                    Box(children=[self.workspaces]),
                    self.button_overview,
                    self.boxed_revealer_left,
                ]
            ),
            end_children=Box(
                children=[
                    self.boxed_revealer_right,
                    self.battery,
                    self.systray,
                    self.button_tools,
                    self.date_time,
                    self.button_power,
                ],
            ),
        )
        
        self.children = self.bar_inner
```

### Modus

Modus uses a more modular architecture:

1. **Widget Hierarchy**:
   - Flatter widget hierarchies
   - Better separation of concerns
   - More consistent layout patterns

2. **Component Composition**:
   - Better use of composition over inheritance
   - More factored creation of UI elements
   - Clearer separation between UI and behavior

3. **State Management**:
   - More centralized state management
   - Better use of reactive properties
   - Clearer data flow between components

4. **Modularity**:
   - More independent modules
   - Cleaner interfaces between components
   - Better reusability of code

Example component architecture:
```python
class StatusBar(Window):
    def __init__(self):
        super().__init__(...)
        
        self.bar_content = CenterBox(name="center-bar")
        
        self.bar_content.end_children = [
            StatusBarCorner("top-right"),
            Box(
                name="bar",
                spacing=4,
                children=[
                    self.recording_indicator,
                    self.tray,
                    self.battery,
                    self.applets,
                    self.date_time,
                    self.button_config,
                ],
                style_classes="end-container",
            ),
        ]

        self.bar_content.start_children = [
            Box(
                name="bar",
                spacing=4,
                children=[self.launcher, self.workspaces, self.stats, self.updates],
                style_classes="start-container",
            ),
            StatusBarCorner("top-left"),
        ]
        
        self.children = self.bar_content
```

### HyDePanel

HyDePanel uses the most structured component architecture:

1. **Widget Hierarchy**:
   - Cleaner widget hierarchies with logical structure
   - Better organization of related elements
   - More consistent patterns across different components

2. **Component Composition**:
   - Strong use of composition over inheritance
   - UI elements are created through helper methods
   - Better separation of concerns throughout

3. **State Management**:
   - Well-structured state management
   - Clearer data flow between components
   - Better reactivity patterns

4. **Modularity**:
   - Highly independent modules
   - Clean interfaces between components
   - Excellent reusability of code

Example component architecture:
```python
class BluetoothWidget(ButtonWidget):
    """A widget to display the Bluetooth status."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(widget_config, **kwargs)
        self.bluetooth_client = BluetoothClient()

        self.box = Box()

        self.children = self.box

        self.icons = icons.icons["bluetooth"]

        self.config = widget_config["bluetooth"]

        self.bluetooth_icon = Image(
            icon_name=self.icons["enabled"],
            icon_size=self.config["icon_size"],
        )

        self.bt_label = Label(label="", visible=False, style_classes="panel-text")

        self.bluetooth_client.connect("changed", self.update_bluetooth_status)

        self.update_bluetooth_status()
```

## Configuration Management

### Ax-Shell

Ax-Shell uses a relatively simple configuration approach:

1. **Configuration Format**:
   - Python-based configuration
   - Some settings in JSON
   - Limited separation between config and code

2. **Configuration Loading**:
   - Configuration loaded at startup
   - Limited support for runtime configuration changes
   - Some hardcoded defaults

3. **User Customization**:
   - Limited user customization options
   - Some theming capabilities
   - Configuration requires code modification

4. **Default Values**:
   - Many defaults embedded in code
   - Some fallbacks for missing configuration
   - Limited validation of configuration

Example configuration:
```python
# From main.py
if not os.path.isfile(CONFIG_FILE):
    exec_shell_command_async(f"python {get_relative_path('../config/config.py')}")
```

### Modus

Modus uses a more standardized configuration approach:

1. **Configuration Format**:
   - JSON-based configuration
   - Better separation between config and code
   - More structured organization of settings

2. **Configuration Loading**:
   - More flexible configuration loading
   - Better support for runtime changes
   - Clearer configuration validation

3. **User Customization**:
   - More user customization options
   - Stronger theming capabilities
   - Better documentation of configuration options

4. **Default Values**:
   - Better handling of default values
   - More consistent fallbacks
   - Improved validation of user configurations

Example configuration:
```json
{
    "wallpapers_dir": "/path/to/wallpapers",
    "theme": "dark",
    "modules": {
        "bar": {
            "enabled": true,
            "position": "top"
        }
    }
}
```

### HyDePanel

HyDePanel has the most sophisticated configuration system:

1. **Configuration Format**:
   - Well-structured JSON with schema validation
   - Complete separation of configuration and code
   - Hierarchical organization of settings

2. **Configuration Loading**:
   - Flexible, modular configuration loading
   - Excellent support for runtime changes
   - Strong validation with error reporting

3. **User Customization**:
   - Extensive user customization options
   - Comprehensive theming system
   - Well-documented configuration options

4. **Default Values**:
   - Clear default values for all settings
   - Consistent fallback strategy
   - Thorough validation with helpful error messages

Example configuration:
```json
{
  "$schema": "./hydepanel.schema.json",
  "battery": {
    "full_battery_level": 100,
    "hide_label_when_full": true,
    "label": true,
    "tooltip": true
  },
  "bluetooth": {
    "icon_size": 14,
    "label": true,
    "tooltip": true
  },
  "layout": {
    "left_section": [
      "workspaces",
      "window_title"
    ],
    "middle_section": [
      "date_time"
    ],
    "right_section": [
      "recorder",
      "@group:1",
      "@group:0",
      "system_tray"
    ]
  }
}
```

## Consolidated Style Guide Recommendations

Based on the analysis of all three projects, here are recommended style guidelines for our implementation:

### Code Organization

1. **Project Structure**:
   - Follow HyDePanel's clear organization with separate directories for modules, services, and utilities
   - Use a flat module structure for simpler components
   - Group related components in subdirectories when they form a cohesive unit

2. **Module Organization**:
   - Each module should focus on a single responsibility
   - Related functionality should be grouped logically
   - Common utilities should be extracted to shared locations

3. **File Organization**:
   - One class per file for major components
   - Related small classes can be grouped in a single file
   - Utility functions should be organized by domain

### Coding Style

1. **Naming Conventions**:
   - Use `snake_case` for methods, functions, and variables
   - Use `CamelCase` for classes
   - Use descriptive names that indicate purpose
   - Prefix private methods and variables with underscore

2. **Class Structure**:
   - Follow HyDePanel's clear separation of concerns
   - Use composition over inheritance where possible
   - Keep constructors focused on initialization, not behavior
   - Extract complex logic to helper methods

3. **Comments and Documentation**:
   - Use docstrings for all classes and public methods
   - Include parameter and return type documentation
   - Explain complex or non-obvious logic
   - Add module-level docstrings explaining purpose

4. **Error Handling**:
   - Use structured exception handling
   - Catch specific exception types when possible
   - Log errors with appropriate severity
   - Provide graceful fallbacks for failures

5. **Event Handling**:
   - Use dedicated handler methods instead of lambdas
   - Maintain clear separation between UI events and business logic
   - Group related event connections together
   - Use descriptive names for event handlers

### CSS Styling

1. **CSS Organization**:
   - Use CSS variables for all colors and key dimensions
   - Organize styles by component with clear hierarchy
   - Use consistent naming for classes and IDs
   - Group related styles together

2. **Visual Design**:
   - Adopt a consistent visual language across all components
   - Use a color palette with base, accent, and semantic colors
   - Maintain consistent spacing, padding, and margins
   - Use rounded corners and borders consistently

3. **Animation**:
   - Use animations purposefully to enhance usability
   - Maintain consistent timing and easing functions
   - Ensure animations degrade gracefully when disabled
   - Use transitions for state changes

4. **Responsiveness**:
   - Design for adaptability to different screen sizes
   - Use relative units instead of absolute when possible
   - Test layouts with different content sizes
   - Consider different display densities

### Component Architecture

1. **Widget Hierarchy**:
   - Keep widget trees as flat as reasonable
   - Use logical grouping of related elements
   - Follow consistent patterns across components
   - Avoid excessive nesting

2. **Component Composition**:
   - Use composition over inheritance
   - Extract reusable parts into helper methods
   - Maintain separation between UI structure and behavior
   - Create clear interfaces between components

3. **State Management**:
   - Use a consistent state management approach
   - Define clear data flow between components
   - Use reactive properties for UI updates
   - Minimize global state

4. **Modularity**:
   - Design components to be independent when possible
   - Create clear interfaces between modules
   - Use services for shared functionality
   - Ensure new components can be added without major changes

### Configuration Management

1. **Configuration Format**:
   - Use JSON for configuration with schema validation
   - Separate configuration completely from code
   - Organize settings hierarchically
   - Use consistent naming and structure

2. **Configuration Loading**:
   - Support flexible configuration loading
   - Handle runtime configuration changes
   - Validate configuration against schema
   - Provide helpful error messages for invalid configuration

3. **User Customization**:
   - Make all reasonable aspects customizable
   - Document all configuration options
   - Provide sensible defaults
   - Support theming and visual customization

4. **Default Values**:
   - Define clear defaults for all settings
   - Implement consistent fallback strategy
   - Validate all user input
   - Provide helpful feedback for configuration issues

## Conclusion

By combining the strengths of all three projects, we can create a cohesive, well-structured implementation for Sway that maintains the best aspects of each while addressing their weaknesses. The recommendations in this style guide draw from the most effective patterns across all three projects to create a consistent, maintainable codebase.

The implementation should prioritize:

1. HyDePanel's strong organization and structure
2. Modus's clean, modular approach to components
3. Ax-Shell's comprehensive feature set
4. A consistent visual language that balances aesthetics with usability

This approach will result in a Fabric implementation for Sway that is maintainable, extensible, and provides an excellent user experience.
