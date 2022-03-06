from __future__ import annotations
import os
import glob
from pathlib import Path
import sys
import sys
from turtle import width
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format
import click
from PIL import Image


SUPPORTED_FILE_TYPES: list[str] = [".jpg", ".png"]


def name_file(fp: Path, suffix) -> str:
    return f"{fp.stem}{suffix}{fp.suffix}"


def resize(fp: str, scale: Union[float, int]) -> Image:
    _scale = lambda dim, s: int(dim * s / 100)
    im: PIL.Image.Image = Image.open(fp)
    width, height = im.size
    new_width: int = _scale(width, scale)
    new_height: int = _scale(height, scale)
    new_dim: tuple = (new_width, new_height)
    return im.resize(new_dim)


@click.command()
@click.option("-p", "--photo",help="photo Path")
@click.option("-s", "--scale", default=50, help="Percent as whole number to scale. eg. 40")
@click.option("-q", "--quiet", default=False, is_flag=True, help="Suppresses stdout.")

def main(photo: str, scale: int, quiet: bool):
    if photo:
        for image in (images := Path().glob(photo)):
            if image.suffix not in SUPPORTED_FILE_TYPES:
                continue
            im = resize(image, scale)
            nw, nh = im.size
            suffix: str = f"_{scale}_{nw}x{nh}"
            resize_name: str = name_file(image, suffix)
            _dir: Path = image.absolute().parent
            im.save(_dir / resize_name)
            if not quiet:
                print(
                    f"resized image saved to {resize_name}.")
        if images == []:
            print(f"No images found at search photo '{photo}'.")
            return
    else:
        print('No photo provided.'
              '\n\n'
              'Usage: resize.py -p <photo_path> -s <scale>')

if __name__ == '__main__':
    cprint(figlet_format('Co-Coder Resizer!'),
       'yellow', attrs=['bold'])
    print("use --help for help")
    main()