
bl_info = {
    "name" : "NodeVoidKeeper",
    "author" : "MagnumVD",
    "description" : "Keeps your nodes centered at the origin, so you can't lose them",
    "blender" : (3, 6, 0),
    "version" : (1, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Node"
}

import bpy
from bpy.app.handlers import persistent
from .functions import center_nodes

debug = True

@persistent
def nodevoidkeeper_save_pre(dummy):
    if debug:
        print('nodevoidkeeper_save_pre')
    center_nodes.run()

@persistent
def nodevoidkeeper_load_post(dummy):
    if debug:
        print('nodevoidkeeper_load_post')
    center_nodes.run()

def register():
    bpy.app.handlers.save_pre.append(nodevoidkeeper_save_pre)
    bpy.app.handlers.load_post.append(nodevoidkeeper_load_post)

def unregister():
    bpy.app.handlers.save_pre.remove(nodevoidkeeper_save_pre)
    bpy.app.handlers.load_post.remove(nodevoidkeeper_load_post)

if __name__ == "__main__":
    register()