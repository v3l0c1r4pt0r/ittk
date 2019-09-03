# ittk
## ITxxxx ToolKit

ITE firmware manipulation toolkit

## Command line interface

Main tool of ITTK is now itetool.py. It allows to list content of ITEPKG image
or extract files from it for further processing.

Its usage is:

```
usage: itetool.py [-h] [-l | -u [ID]] [-d DIR] file

positional arguments:
  file                  ITEPKG file to work on

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            List container elements
  -u [ID], --unpack [ID]
                        Unpack element of ID to directory (default=-1=all)
  -d DIR, --directory DIR
                        Unpack to DIR, instead of CWD
```

* to list contents of image file.itepkg: `./itetool.py -l file.itepkg`
* to unpack all data from file.itepkg: `./itetool.py -u -dout file.itepkg`

## Programming interfaces

```python
import os
from itepkg.itepkg import ITEPKG
with open('sample.pkg') as fp:
    pkg = os.read(fp.fileno(), 0xffffffff)
i = ITEPKG.from_bytes(pkg)
```

After that `i` object contains parsed structure of ITEPKG file, with easy access
to contained filesystem and SMEDIA02 containers.
