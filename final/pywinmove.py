import ctypes
import win32gui

user32 = ctypes.windll.user32
screensize: tuple[int, int] = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def get_screensize():
    user32 = ctypes.windll.user32
    screensize: tuple[int, int] = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize


def move(window: str, x: int, y: int, width, length) -> None:    # type: ignore
    """
    The move function moves the specified window to a specified location.
    The move function takes four arguments:
        1) The name of the window as a string. This is case sensitive and should be enclosed in quotation marks if it contains spaces or special characters (e.g., &quot;Microsoft Word&quot;).
        2) The x-coordinate of the desired location on your screen, measured in pixels from the left edge of your screen to where you want your window located (e.g., 100).
        3) The y-coordinate of the desired location on your screen, measured in pixels from the top edge of your screen

    :param window: str: Specify the name of the window
    :param x: int: Set the x position of the window, y is used to set the y position
    :param y: int: Set the y position of the window, measured in pixels from the top edge of your screen
    :param width: Set the width of the window
    :param length: Set the height of the window
    :return: None
    """
    appname: str = window
    xpos: int = x
    ypos: int = y
    if width is None:
        width: int = int((screensize[0] / 10) * 9)
    if length is None:
        length: int = int((screensize[1] / 10) * 9)

    def enumHandler(hwnd, lParam):  # type: ignore
        if win32gui.IsWindowVisible(hwnd) and appname in win32gui.GetWindowText(hwnd):
            win32gui.MoveWindow(
                hwnd, xpos, ypos, width, length, True
            )  # type: ignore

    win32gui.EnumWindows(enumHandler, None)  # type: ignore
