# Face track

## Overview

Addon for easy face motion caption process of up to several minutes for digitalization and animation of the face in the picture using your webcam or prerecorded video.

### UI
<img src="use_example/ui1.png" alt="drawing" width="400"/>
<img src="use_example/ui2.png" alt="drawing" width="400"/>

### Use example
- There are also some blend files, but I recommend you install and try it for yourself

<img src="use_example/video_test.gif" alt="drawing" width="400"/>
<img src="use_example/game_of_fit.png" alt="drawing" width="400"/>
<img src="use_example/collection1.png" alt="drawing" width="400"/>

## Installation

Instal like any other blender add-on from preferences.
- open preferences - addons
- install addon
- select *Face Track.zip*
- enable add-on
- Install dependencies from extended add-on preferences
- Face Track panel should appear in the _toolbar_ of the *3D _View_ (the shortcut is 'N' for opening the toolbar while in *3D View*)

`!!! Tested on Blender 3.4.0 for Windows !!!`

### Known Issues:

| platform |  possible Issues 	|  possible solution 	|
|--- |---	|---	|
| all |  cv2 wheel fails 	|   blender < 2.93 -> install newer version	|
| all |  permission denied 	|  start blender as Administrator (sudo for linux) while installing dependencies	|
| mac os(arm)  |  mediapipe wheel fails on *apple m1* 	|   *apple arm* processors do not support mediapipe use *intel* | version of **blender**	|
| mac os | problem with camera starting | might be coused by mac trying to use iphone as a webcam |

- If you still have trouble installing dependencies you can install them by hand
  - start blender python **as admin** (in mac os arm, start terminal in Rosetta)
    - find the path of the executable in the blender _script tab_* by typing `import sys` `sys.executable`
    - open it in terminal
  - type
```
import subprocess
import sys
subprocess.run([sys.executable, '-m','pip', 'install', 'mediapipe', 'opencv-contrib-python'])
```

## Credits

This addon was created by Vladislav Komkov. If you find any issues or have any suggestions, please feel free to [create an issue](https://github.com/komkovla/Blender-Face-Track/issues/new) on the repository. Thank you for using Dynamic Section!
