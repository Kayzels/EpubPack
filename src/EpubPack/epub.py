import os
from pathlib import Path
from typing import override
import zipfile
from .utils import snakeCaseString


class EpubException(Exception):
    """Represents specific exceptions that occur when packing an epub"""

    def __init__(self, message: str):
        self.message: str = message

    @override
    def __str__(self) -> str:
        return str(self.message)


class Epub:
    """Epub class representing an epub being made at a specific location, from an unzipped epub folder.

    Attributes:
        - original_path (`Path`): Folder containing the epub files that should be made
        - epub_name (`Path`): Full path and name of the epub file being made
    """

    def __init__(self, unzip_path: Path, save_folder: Path) -> None:
        """Create an Epub object, that will represent an epub being made at a specific location, from an unzipped epub folder.

        Args:
            - unzip_path: Folder containing the epub files that should be made
            - save_folder: Location to save the new epub file
        """
        if not unzip_path.is_dir():
            raise EpubException(
                f"The path provided needs to be a folder. Given: {str(unzip_path)}"
            )
        self.original_path: Path = unzip_path
        """Folder containing the epub files that should be made"""

        file_name = snakeCaseString(unzip_path.stem)
        if not save_folder.exists():
            save_folder.mkdir(parents=True)
        self.epub_name: Path = (save_folder / file_name).with_suffix(".epub")
        """Full path and name of the epub file being made"""

    @override
    def __repr__(self) -> str:
        return f"Original Folder: {self.original_path}\nEpub filename: {self.epub_name}"

    def pack(self) -> None:
        """Pack the unzipped files into an epub created at the desired location

        Raises:
            - EpubException: Thrown when an error occurs, such as the folder not existing, or a missing mimetype file.
        """
        mimetype_file = self.original_path / "mimetype"
        with zipfile.ZipFile(self.epub_name, mode="w") as epub_file:
            try:
                epub_file.write(mimetype_file, "mimetype")
            except FileNotFoundError:
                raise EpubException(
                    f"Mimetype file does not exist. Cannot pack epub. For: {self.epub_name}"
                )
            files_to_add: list[Path] = []

            for root, _, files in os.walk(self.original_path):
                for file_name in files:
                    if file_name != "mimetype":
                        rel_dir = os.path.relpath(root, self.original_path)
                        rel_file = os.path.join(rel_dir, file_name)
                        files_to_add.append(Path(rel_file))

            for file_path in files_to_add:
                epub_file.write(self.original_path / file_path, file_path)
