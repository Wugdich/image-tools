from time import localtime, strftime
from random import randint

import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont

from database import IdsDatabase


def random_logo() -> None:
    # TODO: Change text color between black and white due to background color
    red, green, blue = randint(0, 255), randint(0, 255), randint(0, 255)
    background = Image.new(mode='RGB', size=(600, 600), color=(red,green,blue))

    # Get a drawing context
    draw = ImageDraw.Draw(background)
    x, y = 140, 250
    unique_id = str(_get_unique_id())
    # Use a true type font
    font = ImageFont.truetype("./fonts/Ubuntu-B.ttf", size=120)
    # Draw text
    draw.text(xy=(x, y), text=unique_id, font=font, fill=(255,255,255))
    path = f"./images/unique_ids/unique_id_{unique_id}.jpg"
    background.save(path)
    print(f"New unique id save to - {path}")


def _get_unique_id() -> int:
    db = IdsDatabase()
    exist_ids = db.get_ids()
    while True:
        guess_num = randint(10_000, 100_000)
        if guess_num not in exist_ids:
            db.insert_new_id(guess_num)
            db.close()
            return guess_num



def rgb_wallpaper(resolution: tuple) -> None:
    height, width = resolution
    red = np.zeros(resolution)
    green = np.zeros(resolution)
    blue = np.zeros(resolution)

    # Green square pixels. This square places in center so it's pixels
    # used as offset base for two another squares.
    gp = [
            height // 2 - 100, height // 2 + 100,
            width // 2 - 100, width // 2 + 100,
            ]
    # Red square pixels.
    rp = [p - 50 for p in gp]
    # Blue square pixels.
    bp = [p + 50 for p in gp]

    red[rp[0]:rp[1], rp[2]:rp[3]] = 255
    green[gp[0]:gp[1], gp[2]:gp[3]] = 255
    blue[bp[0]:bp[1], bp[2]:bp[3]] = 255

    red_img = Image.fromarray(red).convert("L")
    green_img = Image.fromarray(green).convert("L")
    blue_img = Image.fromarray(blue).convert("L")

    final_img = Image.merge("RGB", (red_img, green_img, blue_img))
    uniq_number = strftime("%Y%m%d%H%M%S", localtime())
    final_img_filename = f"./images/redgreenblue{uniq_number}.jpg"
    final_img.save(final_img_filename)
    print(f"Image saved to {final_img_filename}")


def tile(*images: Image.Image, vertical:bool=False) -> Image.Image:
    width, height = images[0].width, images[0].height
    tiled_size = (
            (width, height * len(images))
            if vertical
            else (width * len(images), height)
            )
    tiled_img = Image.new(images[0].mode, tiled_size)
    row, col = 0, 0
    for image in images:
        tiled_img.paste(image, (row,col))
        if vertical: col += height
        else: row += width

    return tiled_img


def erode(cycles: int, image: Image.Image) -> Image.Image:
    for _ in range(cycles):
        image = image.filter(ImageFilter.MinFilter(3))
    return image


def dilate(cycles: int, image: Image.Image) -> Image.Image:
    for _ in range(cycles):
        image = image.filter(ImageFilter.MaxFilter(3))
    return image


def main() -> None:
    random_logo()


if __name__ == '__main__':
    main()

