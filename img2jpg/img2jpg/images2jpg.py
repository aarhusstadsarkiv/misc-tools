"""Tool for reading and converting image files.

"""

__version__ = "0.1.0"


# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import codecs
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from PIL import ExifTags, Image, UnidentifiedImageError

from gooey import Gooey, GooeyParser
from natsort import natsorted

utf8_codec = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")

if sys.stdout.encoding != "UTF-8":
    sys.stdout = utf8_codec  # type: ignore
if sys.stderr.encoding != "UTF-8":
    sys.stderr = utf8_codec  # type: ignore

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


class ImageConvertError(Exception):
    """Implements error to raise when conversion fails."""


# -----------------------------------------------------------------------------
# Function Definitions
# -----------------------------------------------------------------------------


def _cptree_ignore(cur_dir: str, paths: List[str]) -> Set[str]:
    return {path for path in paths if not Path(cur_dir, path).is_dir()}


def out_path(file_path: Path, out_dir: Path, break_target: str) -> Path:
    parts = list(file_path.parts)
    new_parts = []

    for part in reversed(parts):
        if part == break_target:
            break
        new_parts.append(part)
    new_path = Path(out_dir, "/".join(reversed(new_parts)))
    new_path = new_path.with_name(f"{new_path.name}.jpg")
    return new_path


def images2jpg(
    image_path: Path,
    out_dir: Path,
    quality: int,
    max_width: int,
    max_height: int,
) -> None:
    """Converts images from the input path to a PDF file.

    Parameters
    ----------
    image_path : pathlib.Path
        Directory where images for conversion reside.
    out_dir : pathlib.Path
        Path to write images to.
    quality : int
        Quality of resulting JPEG
    scaling : int
        Scaling factor for image resizing

    Raises
    ------
    ImageConvertError
        Raised when errors in conversion occur. Errors from PIL are caught
        and re-raised with this error. If no images are loaded, this error
        is raised as well.

    """

    # out_pdf: Path = out_file.with_suffix(".pdf")
    files_str: List[str] = [
        str(f) for f in image_path.rglob("*") if f.is_file()
    ]
    files: List[Path] = [Path(file) for file in natsorted(files_str)]

    for index, file in enumerate(files):
        print(f"{index+1}/{len(files)}", flush=True)
        try:
            im: Any = Image.open(file)
        except UnidentifiedImageError:
            print(f"Failed to open {file} as an image.", flush=True)
        except Exception as e:
            raise ImageConvertError(e)
        else:
            shutil.copytree(
                image_path, out_dir, ignore=_cptree_ignore, dirs_exist_ok=True
            )
            image_out = out_path(file, out_dir, image_path.stem)
            im.load()

            # Resize max width/height is smaller than image width/height
            width, height = im.size
            scaling = 1
            if max_width and max_width / width < 1:
                scaling = max_width / width
            if max_height and max_height / height < 1:
                scaling = max_height / height
            if scaling != 1:
                new_size = (int(scaling * width), int(scaling * height))
                im = im.resize(new_size)

            # JPG image might be rotated
            if hasattr(im, "_getexif"):  # only present in JPGs
                # Find the orientation exif tag.
                for tag, tag_value in ExifTags.TAGS.items():
                    if tag_value == "Orientation":
                        orientation_key: int = tag
                        break

                # If exif data is present, rotate image according to
                # orientation value.
                if im.getexif() is not None:
                    exif: Dict[Any, Any] = dict(im.getexif().items())
                    orientation: Optional[int] = exif.get(orientation_key)
                    if orientation == 3:
                        im = im.rotate(180)
                    elif orientation == 6:
                        im = im.rotate(270)
                    elif orientation == 8:
                        im = im.rotate(90)

            try:
                im.save(image_out, "JPEG", quality=quality or 75)
            except Exception as error:
                raise ImageConvertError(error)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


@Gooey(
    program_name=f"Images to JPEG version {__version__}",
    default_size=(800, 900),
    show_restart_button=False,
    show_failure_modal=False,
    show_success_modal=False,
    progress_regex=r"(\d+)/(\d+)$",
    progress_expr="x[0] / x[1] * 100",
    hide_progress_msg=True,
)
def main() -> None:
    """Main functionality. Uses Gooey for argparsing so we get a nice GUI!"""

    # Argparsing
    parser = GooeyParser(description="Convert images to JPEG files.")
    input_group = parser.add_argument_group("Input")
    output_group = parser.add_argument_group("Output")
    jpg_group = parser.add_argument_group("JPEG Controls")
    quality_group = jpg_group.add_argument_group()
    scale_group = jpg_group.add_mutually_exclusive_group()
    input_group.add_argument(
        "image_path",
        metavar="Image folder",
        help="Folder with images that should be converted to JPEGs.",
        widget="DirChooser",
        type=Path,
    )
    output_group.add_argument(
        "outpath",
        metavar="Output path",
        help="Directory to output images to.",
        widget="DirChooser",
        type=Path,
    )
    quality_group.add_argument(
        "--quality",
        dest="quality",
        metavar="JPEG Quality",
        help="Integer between 0 (worst) and 95 (best)",
        gooey_options={
            "validator": {
                "test": " 0<= int(user_input) <= 95",
                "message": "Must be between 0 and 95 inclusive",
            }
        },
        type=Optional[int],
    )
    scale_group.add_argument(
        "--width",
        dest="max_width",
        metavar="Maximum width",
        help="Maximum resulting width in pixels",
        type=int,
    )
    scale_group.add_argument(
        "--height",
        dest="max_height",
        metavar="Maximum height",
        help="Maximum resulting height in pixels",
        type=int,
    )

    args = parser.parse_args()

    # Run conversion
    try:
        images2jpg(
            Path(args.image_path),
            Path(args.outpath),
            quality=args.quality,
            max_width=args.max_width,
            max_height=args.max_height,
        )
    except ImageConvertError as e:
        sys.exit(e)
    else:
        print(f"Successfully wrote images to {args.outpath}! :)", flush=True)


if __name__ == "__main__":
    main()
