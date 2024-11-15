from pathlib import Path
import argparse
from .epub import Epub, EpubException
from .utils import fixPath
from typing import cast


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
        self.folders: list[Path] = folders
        """A file that contains paths to different epub folders that should be packed"""
        self.save_folder: Path = save_folder
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

    exclusive_group = parser.add_mutually_exclusive_group(required=True)

    exclusive_group.add_argument(
        "-f", "--files", type=str, help="File containing a list of files to be packed"
    )
    exclusive_group.add_argument(
        "-i",
        "--input",
        type=str,
        help="List of folder(s) to be packed, typed directly as arguments",
        nargs="*",
    )

    parser.add_argument(
        "-d",
        "--destination",
        required=True,
        type=str,
        help="Location where epub files should be saved to",
    )
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()
    folders_to_pack: list[Path] = []
    if args.files is not None:
        args.files = cast(str, args.files)
        args.files = fixPath(args.files)
        with open(args.files, mode="r") as file_folders:
            lines = file_folders.read().splitlines()
            for index, line in enumerate(lines):
                lines[index] = fixPath(lines[index])
            for line in lines:
                folders_to_pack.append(Path(line))
    elif args.input is not None:
        args.input = cast(list[str], args.input)
        for file in args.input:
            file = fixPath(file)
            folders_to_pack.append(Path(file))

    args.destination = cast(str, args.destination)
    args.destination = fixPath(args.destination)
    args.destination = args.destination.replace("\\", "/")
    args.destination = args.destination.strip('"')
    destination = Path(args.destination)

    packer = EpubPack(folders_to_pack, destination)
    packer.pack()
