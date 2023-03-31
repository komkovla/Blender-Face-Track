# Face track

## Overview

Addon for easy face motion caption process up to several minutes for digitalization and animation of the face in the picture using your webcam or prerecorded video.

### UI
<img src="use_example/ui1.png" alt="drawing" width="400"/>
<img src="use_example/ui2.png" alt="drawing" width="400"/>

### Use example
- There are also some blend files, but i recomend you to install and try it for yourself

<img src="use_example/video_test.gif" alt="drawing" width="400"/>
<img src="use_example/game_of_fit.png" alt="drawing" width="400"/>
<img src="use_example/collection1.png" alt="drawing" width="400"/>

## Installation

Instal like any other blender add-on from preferences.
- open preferencess - addons
- install addon
- select *Face Track.zip*
- enable add-on
- Install dependancies from extended addon preferencies
- Face Track panel should appear in *toolbar* of the *3D View* (shortcut is 'N' for opening tool bar while in *3D View*)
- Enjoy

`!!! Tested on Blender 3.4.0 for Windows !!!`

### Known Issues:

| platform |  possible Issues 	|  possible solution 	|
|--- |---	|---	|
| all |  cv2 wheel fails 	|   blender < 2.93 -> install newer version	|
| all |  permission denied 	|  start blender as Administrator (sudo for linux) while installing dependencies	|
| mac os(arm)  |  mediapipe wheel fails on *apple m1* 	|   *apple arm* processors do not support mediapipe use *intel* | version of **blender**	|
| mac os | problem with camera starting | might be coused by mac trying to use iphone as a webcam |

- If you still have trouble installing dependancies you can install it by hand
  - start blender python **as admin** (in mac os arm, start terminal in Rosetta)
    - find path of executable in blender *script tab* by typing `import sys` `sys.executable`
  - type
  ```
>>> import subprocess
>>> import sys
>>> subprocess.run([sys.executable, '-m','pip', 'install', 'mediapipe', 'opencv-contrib-python'])
  ```
  - 

