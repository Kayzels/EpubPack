# EpubPack

Welcome to EpubPack!
The aim of this program is to make it easier to pack
loose folders for epubs into an epub.
That is, if you have a folder containing all
the html, css, and other goodies needed for an epub file,
but it's all separate, you can use this to put them together.

This is a Python command line program, with the usage

```text
usage: EpubPack.py [-h] [-v] (-f FILES | -i [INPUT ...]) -d DESTINATION

Pack a list of unzipped epub files into epub files in a given save directory

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f FILES, --files FILES
                        File containing a list of folders to be packed
  -i [INPUT ...], --input [INPUT ...]
                        List of folder(s) to be packed, typed directly as arguments
  -d DESTINATION, --destination DESTINATION
                        Location where epub files should be saved to
```

If we want to create two epub files, and they are in `folders/folder1` and `folders/folder2`,
and we want to save them to an `output/` folder, there are two ways to do it:

1. Create a text file (let's call it `epubs.txt`) that contains the following:

  ```text
  folders/folder1
  folders/folder2
  ```

  And then type the command

  ```shell
  python EpubPack.py -f epubs.txt -d output
  ```

2. Type the folder paths in directly:

  ```shell
  python EpubPack.py -i folders/folder1 folders/folder2 -d output
  ```

---
