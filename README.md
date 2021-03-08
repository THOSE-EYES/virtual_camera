# Cross-Platform Virtual Camera using Python
The app is dedicated to spawn and use virtual camera on Windows and Linux

## Usage
```py
from virtual_camera import CameraApplication
import numpy as np

width = 1280
height = 720
fps = 20
image = np.zeros((height, width, 3), np.uint8)  # RGB
app = CameraApplication(number = 1, width, height, fps)

while True:
    app.show(image, 0)
```

## Installation
This package works on Windows and Linux (no version for Mac OS). Install it from PyPI with:

```sh
pip install -i https://test.pypi.org/simple/ virtual-camera
```