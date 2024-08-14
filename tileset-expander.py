#!/usr/bin/env python3
_VERSION: str = "Tileset Expander 0.0"

import sys
import os
import warnings
from typing import Optional, Tuple

def _print_usage_basic():
    print("Usage: tileset-expander.py -i <input> -o <output>")

def _print_detailed_usage():
    print("Usage: tileset-expander.py -i <input> -o <output> [options]")
    print("Options:")
    print("  -i, --input <input>    Input file")
    print("  -o, --output <output>  Output file")
    print("  -v, --verbose          Verbose mode")
    print("  -V, --version          Print version")
    print("  -y, --yes              Overwrite without asking")
    print("  -n, --no               Do not overwrite")
    print("  -h, --help             Print this help")

def _parse_args() -> Tuple[Optional[str], Optional[str], bool, bool, bool]:
    args = sys.argv[1:]
    input_name: Optional[str] = None
    output_name: Optional[str] = None
    verbose: bool = False
    overwrite: bool = False
    no_overwrite: bool = False

    if len(args) == 0:
        _print_usage_basic()
        sys.exit(os.EX_USAGE)

    while len(args) > 0:
        op = args.pop(0)
        if op in ("-i", "--input"):
            input_name = args.pop(0)
        elif op in ("-o", "--output"):
            output_name = args.pop(0)
        elif op in ("-v", "--verbose"):
            verbose = True
        elif op in ("-V", "--version"):
            print(_VERSION)
            sys.exit(os.EX_OK)
        elif op in ("-y", "--yes"):
            overwrite = True
        elif op in ("-n", "--no"):
            no_overwrite = True
        elif op in ("-h", "--help"):
            _print_detailed_usage()
            sys.exit(os.EX_OK)

    return input_name, output_name, verbose, overwrite, no_overwrite

# Deactivates warnings and tracebacks
# Also hides annoying pygame messages
def _DO_NOT_USE_IF_ITS_A_MODULE():
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    sys.tracebacklimit = 0
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

def _check_files(input_file: str|None, output_file: str|None, overwrite: bool, no_overwrite: bool):
    if input_file is None:
        raise ValueError("missing input file")
    if output_file is None:
        raise ValueError("missing output file")

    if os.path.exists(output_file):
        print(f"{output_file} already exists!", end=" ")
        if not overwrite and (no_overwrite or input("Overwrite? (y/N): ").lower() != "y"):
            print("Aborted.")
            raise FileExistsError("Output file already exists")
        else:
            print("Overwriting...")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"{input_file} not found")


def _expand_tileset_impl(input_name: str, output_name: str, verbose: bool = False):
    def log(message: str):
        if verbose:
            print(message)

    log("Initializing")
    import pygame
    pygame.init()

    SMALL_TILE_ROWS = 4
    SMALL_TILE_COLS = 4
    BIG_TILE_ROWS = 4
    BIG_TILE_COLS = 12
    ATLAS = [
        [ 7, 0, 4,14],[ 4,14, 4,14],[ 4,14, 2,15],[ 7, 0, 2,15],
        [ 7,12, 4,13],[ 4, 8, 4,13],[ 4, 8, 2, 6],[ 7,12, 2, 6],
        [12,12,10,13],[ 5, 8,10,13],[ 5, 8, 6, 6],[12,12, 6, 6],
        [12, 0,10,14],[ 5,14,10,14],[ 5,14, 6,15],[12, 0, 6,15],
        [ 9, 8,10,13],[ 4, 8, 4, 9],[ 4, 9, 4,13],[ 5, 8, 9,13],
        [12,12,10, 9],[ 5, 9, 9, 9],[ 9, 9,10, 9],[ 5, 9, 6, 6],
        [12,12, 9,13],[ 9, 8, 9, 9],[ 9, 9, 9,13],[ 9, 8, 6, 6],
        [ 5, 9,10,13],[ 5,14, 9,14],[ 9,14,10,14],[ 5, 8,10, 9],
        [ 7,12, 4, 9],[ 4, 9, 4, 9],[ 5, 9,10, 9],[ 4, 9, 2, 6],
        [ 5, 8, 9, 9],[ 5, 9, 9,13],[ 9, 9, 9, 9],[ 9, 9, 6, 6],
        [12,12, 9, 9],[ 3, 3, 3, 3],[ 9, 8,10, 9],[ 9, 9,10,13],
        [12, 0, 9,14],[ 9, 8, 9,13],[ 9,14, 9,14],[ 9,14, 6,15],
    ]

    log(f"Loading {input_name}")
    input_image = pygame.image.load(input_name)

    width, height = input_image.get_size()
    if width % SMALL_TILE_COLS != 0 or height % SMALL_TILE_ROWS != 0:
        raise ValueError("Input image should be an atlas of 4x4 tiles. Aborted.")

    small_tile_size = [width // SMALL_TILE_ROWS, height // SMALL_TILE_COLS]
    big_tile_size = [small_tile_size[0] * 2, small_tile_size[1] * 2]
    output_size = [big_tile_size[0] * BIG_TILE_COLS, big_tile_size[1] * BIG_TILE_ROWS]
    small_tileset: list[pygame.Surface] = []

    log("Extracting tiles")
    for _x in range(4):
        y = _x * small_tile_size[0]
        for _y in range(4):
            x = _y * small_tile_size[1]
            tile = pygame.Surface(small_tile_size, pygame.SRCALPHA)
            tile.blit(input_image, (0, 0), (y, x, *small_tile_size))
            small_tileset.append(tile)

    log("Expanding tileset")
    output_image = pygame.Surface(output_size, pygame.SRCALPHA)
    x = 0
    y = 0
    w, h = small_tile_size
    for pattern in ATLAS:
        p0, p1, p2, p3 = pattern
        tile = pygame.Surface(big_tile_size, pygame.SRCALPHA)
        tile.blit(small_tileset[p0], (0, 0), (0, 0, *small_tile_size))
        tile.blit(small_tileset[p1], (w, 0), (0, 0, *small_tile_size))
        tile.blit(small_tileset[p2], (0, h), (0, 0, *small_tile_size))
        tile.blit(small_tileset[p3], (w, h), (0, 0, *small_tile_size))

        output_image.blit(tile, (x * big_tile_size[0], y * big_tile_size[1]))

        y += 1
        if y == 4:
            y = 0
            x += 1

    log(f"Saving {output_name}")
    pygame.image.save(output_image, output_name)
    print(f"Tileset expanded: {output_name}")
    pygame.quit()

def expand_tileset(input_file: str, output_file: str, overwrite: bool = False, verbose: bool = False):
    _check_files(input_file, output_file, overwrite, not overwrite)
    _expand_tileset_impl(input_file, output_file, verbose)

if __name__ == "__main__":
    INPUT_NAME, OUTPUT_NAME, VERBOSE, OVERWRITE, NO_OVERWRITE = _parse_args()
    if VERBOSE:
        print(_VERSION)
        print(f"Input: {INPUT_NAME}")
        print(f"Output: {OUTPUT_NAME}")
        print(f"Overwrite: {OVERWRITE}")
        print(f"No Overwrite: {NO_OVERWRITE}")
    _DO_NOT_USE_IF_ITS_A_MODULE()
    try:
        _check_files(INPUT_NAME, OUTPUT_NAME, OVERWRITE, NO_OVERWRITE)
        _expand_tileset_impl(INPUT_NAME, OUTPUT_NAME, VERBOSE)
    except Exception as e:
        print(e, file=sys.stderr)
        if isinstance(e, FileNotFoundError):
            sys.exit(os.EX_NOINPUT)
        elif isinstance(e, FileExistsError):
            sys.exit(os.EX_CANTCREAT)
        elif isinstance(e, ValueError):
            sys.exit(os.EX_DATAERR)
        sys.exit(os.EX_USAGE)
    sys.exit(os.EX_OK)