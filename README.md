# ittk
## ITxxxx ToolKit

ITE firmware manipulation toolkit

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
