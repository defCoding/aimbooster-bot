import pyautogui
import win32api, win32con
import keyboard
import time
import os
from kdtree import KDNode, EmptyKDNode

def clear_term():
    """Clears the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear') 

def get_next_click_pos():
    """Gets the x, y coordinates of the next left-click."""
    # 0x01 is the left mouse button key. If the button is pressed, the state is either -127 or -128
    while win32api.GetKeyState(0x01) > -127:
        time.sleep(0.001)

    pos = win32api.GetCursorPos()

    # Wait for click release.
    while win32api.GetKeyState(0x01) <= -127:
        time.sleep(0.001)

    return pos

def get_game_region():
    """Gets the bounds of the game in the window. Used for screenshotting the game."""
    print('Use alt-tab to get to the window as any click will be registered as the corner.')
    print('Click on the top-left corner of the game-window.')
    x1, y1 = get_next_click_pos()
    print(f'x: {x1} y: {y1}')

    print('Click on the bottom-right corner of the game-window.')
    x2, y2 = get_next_click_pos()
    print(f'x: {x2} y: {y2}')

    return (x1, y1, x2 - x1, y2 - y1)

def click(x, y):
    """Raises a mouse left-click action at the given coordinates. Uses pywin32 as it is faster than pyautogui."""
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


if __name__ == '__main__':
    clear_term()
    print('Welcome to the aimbooster bot. To begin, please go to https://aimbooster.com on your favorite browser.')
    print('Once you are there, we will need to set the bounds of the game.')
    input('Press Enter in the terminal when you are ready...')
    clear_term()
    x, y, width, height = get_game_region()
    clear_term()
    print('The bounds have been saved. Before we continue, make sure that the game can be completely seen on your screen.')
    print('You can stop the script at any time by pressing \'q\' on your keyboard.')
    print('Start the game first, and then bring the focus back to the terminal to start the script.')
    input('Press Enter in the terminal to start the script...')
    print('Script started.')

    bullseye_rgb = (255, 219, 195)
    
    while not keyboard.is_pressed('q'):
        snapshot = pyautogui.screenshot(region=(x, y, width, height))

        # Create KD-Tree to avoid clicking the same target multiple times.
        kdtree = EmptyKDNode()

        # Check every 5 pixels to remove unnecessary computation.
        for pixel in range(0, width * height, 10):
            img_x, img_y = (pixel % width, pixel // width)
            pix_rgb = snapshot.getpixel((img_x, img_y))

            # Only select pixels that are the right color and also are not near areas that have already been clicked.
            if pix_rgb == bullseye_rgb and not kdtree.exists((img_x, img_y), 10):
                # Add pixel to kd-tree.
                kdtree = kdtree.insert((img_x, img_y))
                click(x + img_x, y + img_y)

                # This sleep avoids multiple clicking, although I'm not sure why. It fixes it so I'm keeping it.
                time.sleep(0.005)