"""Tool for reading and converting image files.

"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import sys
from pathlib import Path
from typing import List, Any
from PIL import Image, UnidentifiedImageError
from natsort import natsorted
from gooey import Gooey, GooeyParser
from __init__ import __version__

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

    for file in files:
        try:
            im: Any = Image.open(file)
        except UnidentifiedImageError:
            print(f"Failed to open {file} as an image.")
        except Exception as e:
            raise ImageConvertError(e)
        else:
            if im.mode == "RGBA":
                im = im.convert("RGB")
            images.append(im)

    if not images:
        raise ImageConvertError(
            "No images loaded! Please double check your path."
        )
    try:
        images[0].save(
            out_pdf,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=images[1:],
        )
    except Exception as e:
        raise ImageConvertError(e)


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
    """Main functionality. Uses Gooey for argparsing so we get a nice GUI!."""

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
    )
    args = parser.parse_args()

    # Run conversion
    try:
        images2pdf(Path(args.image_path), Path(args.outfile))
    except ImageConvertError as e:
        sys.exit(e)
    else:
        print(f"Successfully wrote images to {args.outfile}! :)")


if __name__ == "__main__":
    main()
