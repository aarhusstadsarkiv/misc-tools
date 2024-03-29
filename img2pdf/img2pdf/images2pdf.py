"""Tool for reading and converting image files.

"""

__version__ = "1.2.0"

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import sys
from pathlib import Path
from typing import List, Any, Dict, Optional
from PIL import Image, ImageFile, ExifTags, UnidentifiedImageError
from natsort import natsorted
from gooey import Gooey, GooeyParser

import codecs

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------
utf8_stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
utf8_stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")
if sys.stdout.encoding != "UTF-8":
    sys.stdout = utf8_stdout  # type: ignore
if sys.stderr.encoding != "UTF-8":
    sys.stderr = utf8_stderr  # type: ignore

ImageFile.LOAD_TRUNCATED_IMAGES = True

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


class ImageConvertError(Exception):
    """Implements error to raise when conversion fails."""


# -----------------------------------------------------------------------------
# Function Definitions
# -----------------------------------------------------------------------------


def images2pdf(image_path: Path, out_file: Path) -> None:
    """Converts images from the input path to a PDF file.

    Parameters
    ----------
    image_path : pathlib.Path
        Directory where images for conversion reside.
    out_file: Path
        File to write images to.

    Raises
    ------
    ImageConvertError
        Raised when errors in conversion occur. Errors from PIL are caught
        and re-raised with this error. If no images are loaded, this error
        is raised as well.

    """

    out_pdf: Path = out_file.with_suffix(".pdf")
    images: List[Any] = []
    files_str: List[str] = [
        str(f) for f in image_path.rglob("*") if f.is_file()
    ]
    files: List[Path] = [Path(file) for file in natsorted(files_str)]
    load_errs: List[str] = []

    for file in files:
        try:
            im: Any = Image.open(file)
        except UnidentifiedImageError:
            msg = f"Failed to open {file} as an image."
            print(msg, flush=True)
            load_errs.append(msg)
        except Exception as e:
            raise ImageConvertError(e)
        else:
            print(f"Loading {file}", flush=True)
            im.load()

            # Cannot save alpha channel to PDF
            if im.mode == "RGBA":
                im = im.convert("RGB")

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

            images.append(im)

    if not images:
        raise ImageConvertError(
            "No images loaded! Please double check your path."
        )
    try:
        print(f"Writing images to {out_pdf}", flush=True)
        images[0].save(
            out_pdf,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=images[1:],
        )
    except Exception as e:
        raise ImageConvertError(e)

    for err in load_errs:
        print(f"WARNING! {err}", flush=True)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


@Gooey(
    program_name=f"Images to PDF version {__version__}",
    default_size=(800, 550),
    show_restart_button=False,
    show_failure_modal=False,
    show_success_modal=False,
)
def main() -> None:
    """Main functionality. Uses Gooey for argparsing so we get a nice GUI!"""

    # Argparsing
    parser = GooeyParser(description="Convert images to a single PDF file.")
    input_group = parser.add_argument_group("Input")
    output_group = parser.add_argument_group("Output")
    input_group.add_argument(
        "image_path",
        metavar="Image folder",
        help="Folder with images that should be written to a PDF file.",
        widget="DirChooser",
        type=Path,
    )
    output_group.add_argument(
        "outfile",
        metavar="Output file",
        help="PDF file to output images to.",
        widget="FileSaver",
        type=Path,
    )
    args = parser.parse_args()
    print(args.image_path, args.outfile, flush=True)

    # Run conversion
    try:
        images2pdf(Path(args.image_path), Path(args.outfile))
    except ImageConvertError as e:
        sys.exit(e)
    else:
        print(f"Successfully wrote images to {args.outfile}! :)", flush=True)


if __name__ == "__main__":
    main()
