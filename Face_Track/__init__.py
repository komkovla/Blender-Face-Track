import sys
import importlib
from .src import conf
sys.path.append("./src/")

bl_info = {
    'name': 'Face Track',
    'author': 'Vladislav Komkov',
    "location": "View3D > Sidebar > Face Track",
    "description": "Addon for face mesh creation and motion capture using web cam or video input",
    "warning": "Requires installation of dependencies",
    "wiki_url": "https://gitlab.fit.cvut.cz/BI-PGA/b221/komkovla",
    "tracker_url": "https://gitlab.fit.cvut.cz/BI-PGA/b221/komkovla/-/issues",
    "support": "COMMUNITY",
    'category': 'All',
    'version': (0, 0, 2),
    'blender': (3, 0, 0)
    }

modulesNames = [
    'install_dep',
    'add_face', 
    'prepare_face', 
    'video_track', 
    'face_track_panel',
    'preferences_panel',
    ]
modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))



for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        print("reload: ", currentModuleFullName)
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        print("import: ", currentModuleFullName)
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()
                print('register: ', currentModuleName)
    if conf.init():
        conf.MODULES_INSTALLED = True

def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
                print('unregister: ', currentModuleName)

if __name__ == "__main__":
    register()