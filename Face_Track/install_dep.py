import bpy
from .src import conf
import sys
import pathlib
import subprocess
import os
import warnings

class installDependencies(bpy.types.Operator):
    bl_idname = 'preferences.install_dep'
    bl_label = 'install dependencies'
    bl_options = {"REGISTER", "INTERNAL"}
    bl_description = ("Downloads and installs the required python packages for this add-on. "
                    "Internet connection is required. Blender may have to be started with "
                    "elevated permissions in order to install the package")
    def execute(self, context):
        if not try_import():
            if not install(self):
                return {"FINISHED"}
        conf.MODULES_INSTALLED = True
        print('modules installed: ', conf.MODULES_INSTALLED)
        return {"FINISHED"}

    @classmethod
    def poll(cls, context):
        return not conf.MODULES_INSTALLED

def register():
    bpy.utils.register_class(installDependencies)

def unregister():
    bpy.utils.unregister_class(installDependencies)

def try_import():
    if conf.import_module('cv2') == None or conf.import_module('mediapipe') == None:
        return False
    for i in range(2):
        conf.package_names[i] = conf.Package(conf.package_names[i].name, True, False)
    return True

def install(context):
    install_path = None
    
    # Find site-packages directory in all *path* paths
    for i in sys.path:
        if "site-packages" in i:
            install_path = pathlib.Path(i)
            global DEP_PATH
            DEP_PATH = install_path
            break
   
    # Site-packages directory is not in path
    if install_path is None:
        context.report({'INFO'}, "Path not found")
        conf.ShowMessageBox("Error installing dependencies, side-packages path not found, please consider submitting bug report")
        return False
    
    # Make sure pip is installed
    ensure_pip()

    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    # Get executable
    pyhon_path = get_python_exe()
    if pyhon_path is None:
        conf.ShowMessageBox("Python exe is not found")
        return False

    # Install each package
    for i in range(0, len(conf.package_names)):
        context.report({'INFO'}, "Installing %s" % conf.package_names[i].name)
        conf.package_names[i] = conf.Package(conf.package_names[i].name, conf.package_names[i].installed, True)
        
        # Install module
        try:
            subprocess.run([pyhon_path, '-m', 'pip', "install", '--target', str(install_path), conf.package_names[i].name, ], check=True)
        except subprocess.CalledProcessError:
            conf.ShowMessageBox("Couldn't install dependencies")
            return False

        conf.package_names[i] = conf.Package(conf.package_names[i].name, True, False)
    return True

def ensure_pip():
    try:
        # Check if pip is already installed
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
    except subprocess.CalledProcessError:
        import ensurepip
        # ensure the pip
        ensurepip.bootstrap()
        # https://github.com/robertguetzkow/blender-python-examples
        os.environ.pop("PIP_REQ_TRACKER", None)
        subprocess.run([sys.executable, '-m', 'pip', 'install', "--upgrade", 'pip', ], check=True)

# https://github.com/cgtinker/BlendArMocap/blob/8063bf2ced0b2a32f1d7d46a70e2e818a92c638c/src/cgt_blender/utils/dependencies.py
# handle for older versions support
def get_python_exe():
    version = bpy.app.version
    if version[0] > 2 or version[0] == 2 and version[1] >= 92:
        # in newer versions sys.executable should point to the py executable
        executable = sys.executable

    else:
        with warnings.catch_warnings():
            # catching depreciated warning
            warnings.simplefilter("ignore")
            try:
                # blender vers =< 2.91 contains a path to their py executable
                executable = bpy.app.binary_path_python
            except AttributeError:
                executable = None
                pass

    # some version the path points to the binary path instead of the py executable
    if executable == bpy.app.binary_path or executable == None:
        py_path = Path(sys.prefix) / "bin"
        py_exec = next(py_path.glob("python*"))  # first file that starts with "python" in "bin" dir
        executable = str(py_exec)
        print(f"cmd failed, redirecting to: {executable}")

    print(f"blender bin: {bpy.app.binary_path}, blender version: {version}")
    print(f"python exe: {executable}")
    return executable