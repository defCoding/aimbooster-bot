# Aimbooster Bot
A bot that beats the classic gamemode on http://aimbooster.com.

## Context
I've always wanted to make a script that could actually play a game on some external website, so this was a fun experience of using `pyautogui` and `pywin32` to take control of my mouse. The program takes a screenshot of the game area established by the user, and then searches that screenshot for pixels that match the color of the bullseye. If it sees it, it clicks at that location. To speed up the program, the script only checks every 5 pixels, as there isn't really a need to check every pixel.

![Bullseye Color](https://i.imgur.com/zgAe7hH.png)

There were a couple of issues I had to tackle in the game. In the game, once the player clicks on the target, it disappears. However, the screenshot won't show the target disappearing, so as the game scanned each pixel, it would inevitably scan another pixel on a bullseye that it already clicked, which would result in a misclick since the target wouldn't be there anymore. One way to fix this was to `break` out of the loop after clicking, forcing another screenshot, which would refresh the screen to the new state after the target disappeared. So the code looked something like this:

```py
while not keyboard.is_pressed('q'):
    snapshot = pyautogui.screenshot(region=(x, y, width, height))

    # Check every 5 pixels to remove unnecessary computation.
    for pixel in range(0, width * height, 5):
        img_x, img_y = (pixel % width, pixel // width)
        pix_rgb = snapshot.getpixel((img_x, img_y))

        if pix_rgb == bullseye_rgb:
            click(x + img_x, y + img_y)
            # Have to break here or else it will try to click the target again.
            # Sleep delay is to give frame enough time to update and remove the target.
            time.sleep(0.1)
            break
```

This fix worked at lower speeds, but would fail at higher speeds. If the rate of target spawn was fast enough, then the targets on the lower half of the screen would never be clicked. Clicking on a target on the upper half the screen would result in a new screenshot being taken, and that new screenshot would contain another target on the upper half, which would trigger another screenshot, and so on and so forth. So the `for` loop would never reach the lower pixels before being broken out of.

### Example
#### First Screenshot
![First screenshot](https://i.imgur.com/sbJyr5a.png)

#### Second Screenshot After Clicking the Target Above
![Second screenshot](https://i.imgur.com/qndPw2e.png)

I needed some way of not allowing clicks within a certain range of areas that had already been clicked. I could simply store the coordinates of areas that were already clicked in some list, and before clicking any new spot, do a linear scan through the list to ensure that the new spot was not within some range of the spots already in the list. However, this would be an `O(n)` computation and I wanted something faster.

Instead, I wrote up a simple KD-Tree implementation in `kdtree.py`, and clicked coordinates were stored in the KD-Tree. Before making a new click, we would check to see that the coordinate was not already in the KD-Tree, provided some tolerance. With the KD-Tree implementation, the search was reduced to `O(log n)`.


## How to Use
You will need to have `pip` installed. [Instructions here.](https://pip.pypa.io/en/stable/installing/)

Run `pip install -r requirements.txt` while in the cloned repository to install the required libraries.

Then run `python bot.py` and follow the instructions in the terminal. Please note that when asked to press 'Enter', the focus must be on the terminal window.


## Preview
The bot can play up to ~18 targets/sec. The preview shows 15 targets/sec.
![Preview](https://i.imgur.com/iXsEdFA.gif)
