"""Tool for reading and converting image files.

"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from pathlib import Path
from typing import List, Any
from PIL import Image, UnidentifiedImageError

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
    files: List[Path] = [
        file for file in image_path.rglob("*") if file.is_file()
    ]
    for file in files:
        try:
            im = Image.open(file)
        except UnidentifiedImageError:
            pass
        else:
            images.append(im)

    images[0].save(
        out_pdf,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=images[1:],
    )


images2pdf(Path(r"C:\data\test_img"), Path(r"C:\data\test_img\test.pdf"))
