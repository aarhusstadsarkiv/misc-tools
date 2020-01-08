"""Tool for reading and converting image files.

"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from pathlib import Path
from typing import List, Any
from PIL import Image
from natsort import natsorted

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


class ImageConvertError(Exception):
    """Implements error to raise when conversion fails."""


# -----------------------------------------------------------------------------
# Function Definitions
# -----------------------------------------------------------------------------


def images2pdf(image_path: Path, outfile: Path) -> None:
    """Description

    Parameters
    ----------
    param : type
        desc

    Returns
    -------
    return : type
        desc

    Raises
    ------
    BadError

    """
    out_pdf: Path = outfile.with_suffix(".pdf")
    images: List[Any] = []
    files_str: List[str] = [
        str(f) for f in image_path.rglob("*") if f.is_file()
    ]
    files = [Path(file) for file in natsorted(files_str)]
    for file in files:
        try:
            im = Image.open(file)
        except Exception:
            pass
        else:
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


images2pdf(
    Path(
        r"M:\Borgerservice-Biblioteker\Stadsarkivet\Projekter\RETRO\Materiale fra andre arkiver\Næstved Kommune\Aversi Sogneråd forhandlingsprotokol 1856-1891"
    ),
    Path(r"C:\data\test_img\test.pdf"),
)
