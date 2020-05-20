# bin2src
Convert an arbitrary file to .S / .c / .cpp / .cs source file, and generate also a header .h

```
$ python3 bin2src.py
Usage: bin2src.py <INPUT_FILE> <OUTPUT_SOURCE> [<OUTPUT_HEADER>]
with <OUTPUT_SOURCE> : *.s / *.S / *.c / *.cpp / *.cs
  ex: bin2src.py /etc/passwd coco.cpp coco.h
  ex: bin2src.py /etc/passwd coco.S coco.h

$ python3 bin2src.py molecule.ply molecule.c molecule.h
```
