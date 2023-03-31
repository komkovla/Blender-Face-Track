import bpy
from . import install_dep as dep
from .src import conf
import os

class preferences_panel(bpy.types.AddonPreferences):
    # Important to be the package name
    bl_idname = os.path.basename(os.path.dirname(__file__))


    def draw(self, context):
        
        # Install operator
        self.layout.operator(
            dep.installDependencies.bl_idname, 
            icon = 'PLUS', 
            text=dep.installDependencies.bl_label
            )
        # Info about dependancies
        for package in conf.package_names:
            if package.installing:
                icon='REC'
            elif package.installed:
                icon='CHECKMARK'
            else:
                icon = 'X'
            self.layout.label(text = package.name, icon = icon)

def register():
    bpy.utils.register_class(preferences_panel)

def unregister():
    bpy.utils.unregister_class(preferences_panel)
