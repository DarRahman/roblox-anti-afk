# Roblox Anti-AFK

A lightweight Windows desktop application designed to prevent being disconnected from Roblox due to the default 20-minute idle kick.

It works by sending background mouse movement and click messages directly to the Roblox window handle, ensuring that the idle timer is reset without interrupting your active window or moving your physical mouse cursor.

## Features

- **Background Input Simulation**: Sends inputs directly to Roblox using Windows API calls. Your physical mouse cursor remains completely free to use.
- **Randomized Intervals**: Action triggers are randomized between 2 and 4 minutes to resemble natural activity.
- **Minimalist GUI**: Simple start/stop interface with a built-in countdown timer and activity log.

## Prerequisites

- Windows OS
- Python 3.x
- `pywin32` library

## Installation

1. Install the required Windows API bindings for Python:
   ```bash
   pip install pywin32
   ```

2. Download `anti_afk_gui.py` and place it in your project directory.

## Usage

1. Open Roblox. Ensure it is in windowed mode (not fullscreen).
2. You can leave the Roblox window running in the background behind other applications, but **do not minimize it** to the taskbar.
3. Run the script:
   ```bash
   python anti_afk_gui.py
   ```
4. Click **Start** to run the anti-AFK loop.
5. Click **Stop** to halt execution.

## License

This project is open-source and available under the MIT License.
