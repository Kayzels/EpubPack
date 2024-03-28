from pathlib import Path
import argparse
from PyQt6.QtWidgets import QApplication
from epub import Epub, EpubException


class EpubPack:
    """Represents the tool that packs the various epub folders in the file sent

    Attributes:
        - folders (`list[Path]`): A file that contains paths to different epub folders that should be packed
        - save_folder (`Path`): The location where the epub files should be saved
    """

    def __init__(self, folders: list[Path], save_folder: Path) -> None:
        """Create an EpubPack object, used to pack multiple epub folders into an epub file

        Args:
            - folders: A file that contains paths to different epub folders that should be packed
            - save_folder: The location where the epub files should be saved
        """
        self.folders = folders
        """A file that contains paths to different epub folders that should be packed"""
        self.save_folder = save_folder
        """The location where the epub files should be saved"""

    def pack(self):
        """Pack the different folders in the `folders` attribute"""
        for index, folder in enumerate(self.folders):
            epub = Epub(folder, self.save_folder)
            try:
                epub.pack()
                print(
                    f"[{index + 1}/{len(self.folders)}] Completed packing {folder.stem}"
                )
            except EpubException as e:
                print(e.message)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Pack a list of unzipped epub files into epub files in a given save directory"
    )
    parser.add_argument(
        "-v", "--v", action="version", version=f"{parser.prog} version 0.1.0"
    )
    parser.add_argument("-f", "--files", required=True, type=str)

    parser.add_argument("-d", "--destination", required=True, type=str)
    return parser


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    folders_to_pack: list[Path] = []
    args.files = args.files.replace("\\", "/")
    with open(args.files, mode="r") as file_folders:
        lines = file_folders.read().splitlines()
        for index, line in enumerate(lines):
            lines[index] = line.replace("\\", "/")
            lines[index] = line.strip('"')
        for line in lines:
            folders_to_pack.append(Path(line))
    destination = Path(args.destination)

    packer = EpubPack(folders_to_pack, destination)
    packer.pack()
    app = QApplication([])
