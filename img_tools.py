from PIL import Image, ImageFilter


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
    filename = "./images/testing-img.jpg"
    with Image.open(filename) as img:
        img.load()


    red, green, blue = img.split()
    zeroes = red.point(lambda _: 0)
    red_merge = Image.merge(
            "RGB", (red, zeroes, zeroes)
            )
    green_merge = Image.merge(
            "RGB", (zeroes, green, zeroes)
            )
    blue_merge = Image.merge(
            "RGB", (zeroes, zeroes, blue)
            )
    tiled_img = tile(red_merge, green_merge, blue_merge)
    tiled_img.show()


if __name__ == '__main__':
    main()

