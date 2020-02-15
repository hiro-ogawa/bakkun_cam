from typing import Tuple
from PIL import Image


def resize_keep_aspect(img_in: Image, s: Tuple[int]) -> Image:
    x, y = img_in.size
    rate = min(s[0] / x, s[1] / y)
    new_size = (int(x*rate), int(y*rate))
    return new_size


def add_frame(input_img_fname: str, frame_image_png_fname: str) -> Image:
    base_color = (255, 255, 255)

    img_input = Image.open(input_img_fname)  # type: Image
    print(img_input.size)
    img_frame = Image.open(frame_image_png_fname)  # type: Image
    print(img_frame.size)

    new_size = resize_keep_aspect(img_input, img_frame.size)
    resized_im = img_input.resize(new_size, Image.LANCZOS)

    img_base = Image.new('RGB', img_frame.size, base_color)

    ax = int((img_base.width - new_size[0])/2)
    ay = int((img_base.height - new_size[1])/2)

    img_base.paste(resized_im, (ax, ay))

    # img_base.alpha_composite(img_frame)
    img = Image.composite(img_frame, img_base, img_frame)

    # resized_im = img_input.thumbnail(img_frame.size, Image.ANTIALIAS)
    # resized_im = img_input.thumbnail((100, 100), Image.ANTIALIAS)
    return img.convert('RGB')


def gen_thumbnail(image_in: Image, size: Tuple[int]):
    img = image_in.copy()
    img.thumbnail(size, Image.LANCZOS)
    return img


if __name__ == "__main__":
    input_fname = "raw_test_image.jpg"
    # input_fname = "raw.jpg"
    # frame_fname = "assets/frame2.png"
    frame_fname = "assets/frame_bakuhai.png"

    image = add_frame(input_fname, frame_fname)
    print(image.size)
    image.save("add_frame.jpg")
