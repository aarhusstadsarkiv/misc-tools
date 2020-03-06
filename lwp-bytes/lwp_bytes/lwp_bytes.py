import json
import re
from pathlib import Path
from collections import Counter


def check_lwp_bytes(json_file: Path) -> None:
    json_data = json.load(json_file.open(encoding="utf-8"))
    no_match = json_data.get("warnings", {}).get("No match", [])
    file_count: Counter = Counter()
    byte_regex = re.compile(
        r"(?i)^576f726450726f0dfb000000000000000005"
        "985c8172030040ccc1bfffbdf970"
    )
    for file_dict in no_match:
        file_path = Path(next(iter(file_dict)))
        with file_path.open("rb") as in_file:
            byte_data = in_file.read(64)
            if byte_regex.match(byte_data.hex()):
                file_count.update(["lwp_file"])
            else:
                file_count.update(["other_file"])
    print(dict(file_count))


def main() -> None:
    check_lwp_bytes(
        Path(
            "D:/data/batches/batch_1/org_files/"
            "_digiarch/reports/identification_warnings.json"
        )
    )


if __name__ == "__main__":
    main()
