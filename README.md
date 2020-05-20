# bin2src
Convert an arbitrary file to .S / .c / .cpp / .cs source file, and generate also a header .h

This turns out to be very useful to include arbitrary data in a program (ex: inserting of an small image in a program without need to access to a filesystem nor to deal with permissions issues). Moreover, the API to use inserted data is really straightforward : inserted data are accessible as global variables, because there are loaded in the virtual addressing space during the boot step of the program.

```
$ python3 bin2src.py
Usage: bin2src.py <INPUT_FILE> <OUTPUT_SOURCE> [<OUTPUT_HEADER>]
with <OUTPUT_SOURCE> : *.s / *.S / *.c / *.cpp / *.cs
  ex: bin2src.py /etc/passwd coco.cpp coco.h
  ex: bin2src.py /etc/passwd coco.S coco.h

$ python3 bin2src.py molecule.ply molecule.c molecule.h
```
