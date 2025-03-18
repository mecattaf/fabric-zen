# Fabric Overview

Fabric is a Python-based desktop widgets framework that provides a high-level, signal-based workflow for creating customizable UI elements. It supports both X11 and Wayland, making it suitable for your Sway environment. The core strength of Fabric is that it uses Python as the configuration language, providing access to the full Python ecosystem while maintaining low resource usage.

# Current Functionality in Existing Dotfiles

I've analyzed the three main dotfiles repositories (HyDePanel, Ax-Shell, and Modus) along with the Fabric source code to create this comprehensive functionality table:

| Functionality | HyDePanel | Ax-Shell | Modus | Notes |
|---------------|:---------:|:--------:|:-----:|-------|
| **Status Bar** | ✅ | ✅ | ✅ | All implementations include date/time, battery, etc. |
| **Workspaces** | ✅ | ✅ | ✅ | Workspace indicators with support for Hyprland |
| **Notifications** | ✅ | ✅ | ✅ | Full notification system with action support |
| **System Tray** | ✅ | ✅ | ✅ | Available in all implementations |
| **App Launcher** | ✅ | ✅ | ✅ | Similar to Rofi/dmenu in functionality |
| **Clipboard Manager** | ❌ | ❌ | ✅ | Modus has cliphist integration |
| **Power Menu** | ✅ | ✅ | ✅ | Options for logout/sleep/restart/poweroff |
| **OSD Indicators** | ✅ | ✅ | ✅ | For brightness, volume, etc. |
| **Bluetooth Manager** | ✅ | ✅ | ✅ | Connects/disconnects devices |
| **WiFi/Network Manager** | ✅ | ❓ | ✅ | Partially implemented in some configs |
| **Calendar** | ✅ | ✅ | ✅ | Usually integrated with date/time modules |
| **Volume Control** | ✅ | ✅ | ✅ | Includes output device selection |
| **Media Controls** | ✅ | ✅ | ✅ | Playback controls via playerctl |
| **Brightness Control** | ✅ | ✅ | ✅ | Uses brightnessctl |
| **Quick Settings** | ✅ | ✅ | ✅ | Similar to modern OS quick settings panels |
| **Emoji Picker** | ❌ | ✅ | ✅ | Available in Ax-Shell and Modus |
| **Weather Widget** | ✅ | ✅ | ❌ | Shows weather conditions |
| **CPU/RAM Usage** | ✅ | ✅ | ❌ | System monitoring tools |
| **Battery Status** | ✅ | ✅ | ✅ | Shows battery level and charging status |
| **Audio Visualizer** | ✅ | ❌ | ❌ | CAVA integration in HyDePanel |
| **Screen Recorder** | ✅ | ✅ | ✅ | Records screen or areas |
| **Screenshot Tool** | ✅ | ✅ | ✅ | Captures screen or areas |
| **OCR Tool** | ✅ | ✅ | ❌ | Optical character recognition |
| **Color Picker** | ✅ | ✅ | ❌ | Picks colors from screen |
| **Todo/Kanban** | ❌ | ✅ | ✅ | Task management |
| **Terminal** | ❌ | ✅ | ❌ | Integrated terminal in Ax-Shell |
| **Wallpaper Selector** | ❌ | ✅ | ✅ | Changes desktop wallpaper |
| **Calculator** | ❌ | ✅ | ❌ | Simple calculator in Ax-Shell |
| **Workspaces Overview** | ❌ | ✅ | ❌ | Visual workspace switcher |
| **Virtual Keyboard** | ❌ | ❌ | ❌ | Not implemented yet in any config |

# Planned But Not Implemented Features

Based on roadmaps in the repositories:

| Planned Feature | Repository | Status |
|-----------------|------------|--------|
| **Virtual Keyboard** | None | Not started |
| **Multi-monitor support** | Ax-Shell | Planned |
| **Multimodal AI Assistant** | Ax-Shell | Planned |
| **Notification Panel** | Modus | Planned |
| **Vertical Layout** | Ax-Shell | Planned |
| **Network Manager UI** | Ax-Shell | Planned |

# Feasibility Assessment
1. **Replace wlogout**: Power menus are well-implemented in all Fabric configurations
2. **Replace waybar**: Status bars with all your required indicators are core to Fabric
3. **Replace mako**: Notification systems are robust in Fabric implementations
4. **Replace rofi**: App launchers, clipboard managers, and emoji selectors exist

# Sway to Fabric Functionality Mapping

## Core Functionality

| Current Implementation | Description | Fabric Alternative | Status | Notes |
|------------------------|-------------|-------------------|--------|-------|
| Waybar | Status bar with date/time, battery, etc. | Fabric Status Bar | ✅ Available | All Fabric configs (HyDePanel, Ax-Shell, Modus) have comprehensive status bars |
| Workspace Management | Workspace switching, movement | Fabric Workspaces Module | ✅ Available | Available in all configurations, needs adaptation from Hyprland to Sway |
| Mako | Notification daemon | Fabric Notifications | ✅ Available | Full notification support with actions in all configs |
| Wlogout | Power menu | Fabric Power Menu | ✅ Available | Complete implementations in all configs for logout/sleep/restart/poweroff |
| Rofi (app launcher) | Application launcher | Fabric App Launcher | ✅ Available | All configs have app launchers similar to Rofi |
| Rofi (clipboard) | Clipboard history via cliphist | Fabric Clipboard Manager | ✅ Available | Available in Modus using cliphist integration |
| Rofi (emoji) | Emoji selector | Fabric Emoji Picker | ✅ Available | Implemented in Ax-Shell and Modus |
| Blueman-manager | External Bluetooth manager | Fabric Bluetooth Manager | ✅ Available | All Fabric configs integrate Bluetooth management directly into the shell UI |
| Nmtui | Terminal-based network manager | Fabric Network Manager | ✅ Available | HyDePanel and Modus integrate network management into the shell UI |
| Pavucontrol | External audio settings utility | Fabric Audio Controls | ✅ Available | All Fabric configs integrate audio device management directly into the shell UI |
| Missing | Virtual keyboard | Fabric Virtual Keyboard | ❌ Planned | Not yet implemented in any config |

## Media and System Controls

| Current Implementation | Description | Fabric Alternative | Status | Notes |
|------------------------|-------------|-------------------|--------|-------|
| Volume Control Scripts | Volume adjustment with OSD | Fabric Volume Controls | ✅ Available | All configs include volume control with OSD |
| Brightness Control Scripts | Brightness adjustment with OSD | Fabric Brightness Controls | ✅ Available | All configs include brightness control with OSD |
| Playerctl bindings | Media playback controls | Fabric Media Controls | ✅ Available | Available in all configurations |
| Color Picker Script | Screen color picker | Fabric Color Picker | ✅ Available | Implemented in Ax-Shell |

## Utilities and Productivity

| Current Implementation | Description | Fabric Alternative | Status | Notes |
|------------------------|-------------|-------------------|--------|-------|
| Screenshot Scripts | Full and area screenshots | Fabric Screenshot Tool | ✅ Available | All configs have screenshot functionality |
| Swappy Scripts | Screenshot editing | Fabric Screenshot Editor | ✅ Available | Can be integrated with screenshot tools |
| Workspace Indicator Script | Shows active workspace | Fabric Workspaces | ✅ Available | Part of Fabric workspace management |
| Missing | Todo/Kanban board | Fabric Todo/Kanban | ✅ Available | Implemented in Ax-Shell and Modus |
| Missing | Calendar | Fabric Calendar | ✅ Available | Available in all configurations |
| Dashboard | Central control panel | ✅ Available | Ax-Shell has comprehensive dashboard |
| Workspaces Overview | Visual workspace switcher | ✅ Available | Available in Ax-Shell |
| Quick Settings | Fast access to common settings | ✅ Available | Available in all configurations |
| OCR Tool | Text recognition from images | ✅ Available | Available in HyDePanel and Ax-Shell |


Repo map:
- OG fabric repo  look at examples and fabric and scripts folders
- docs folder has the documentation as taken from the official fabric wiki
- hydepanel must modify to make sway compatible, notice all the avaulable modules; and has great readme including how it tells us to initialize
- modus has great functionality, look at what they require us to install
- ax-shell also great functionality, must understand install script. note how they also ask to install fabric-cli (which needs to be created as spec) and same with Gray. also investigate the use of tesseract as it is high value
- ags has the on screen keyboard to draw from is in ags/modules/onscreenkeyboard
- eww-kb has another keyboard in shell/kbd

notes:
- might need to create sway related alternatives to hyprland items? perhaps look at waybar mapping since it has both?
- look into all one-liners in swaywm config, and all scripts in swaywm folder of config as we will replace them


PS Might have to add two new COPRs 

clean up the install script and my copr repo since we will be removing some of the packages from there: https://github.com/solopasha/hyprlandRPM/tree/master/astal

We moved away from AGS because the original author put some funbctionality behind paywall:
Theming
Bar
Notifications
On Screen Display
Powermenu
Launcher
Application Drawer

Unfinished Roadmap for ags paid version
[ ] css api
[ ] launcher plugin api
[ ] bar plugin api
[ ] more flexible theming integrations
[ ] dock (compositor independent using toplevel protocol)
[ ] quick settings
[ ] app drawer swipe gestures
[ ] functional network launcher plugin
[ ] applauncher compositor independent clients plugin
[ ] functional calendar plugin with evolution-data-server and local files
[ ] GSConnect/KDE connect integration
[ ] migrate to GTK4 as much as possible
[ ] vertical bar
[ ] lockscreen
[ ] greetd greeter
[ ] polkit agent
[ ] launcher AI plugin
[ ] Bar floating style
[ ] launcher web search plugin
