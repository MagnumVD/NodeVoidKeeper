
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

def dump(obj):
    for attr in dir(obj):
        if hasattr( obj, attr ):
            print( "obj.%s = %s" % (attr, getattr(obj, attr)))

nodegridscale = 20 #figured out by experimenting, don't mess with it

import bpy
import numpy
from bpy.app.handlers import persistent

def nodes_to_origin(nodetree):
    
    nodes = nodetree.nodes
    
    # Get parent
    is_parent = []
    for node in nodes:
        if node.parent is None:
            is_parent += [1]
        else:
            is_parent += [0]
    
    # Get average pos of all nodes
    pos = numpy.zeros(len(nodes)*2)
    nodes.foreach_get('location', pos)
    
    avg_pos = numpy.average(pos.reshape(-1,2), axis=0, weights=is_parent)
    
    # make avg_pos align to the grid
    avg_pos = (avg_pos[0] - avg_pos[0] % nodegridscale, avg_pos[1] - avg_pos[1] % nodegridscale)
    
    # Only move unparented nodes
    centered_pos = (pos.reshape(-1,2)-avg_pos*numpy.array(is_parent)[: , numpy.newaxis]).flatten()
    
    # Move nodes midpoint to (0,0)
    nodes.foreach_set('location', centered_pos)

def center_view(nodetree):
    nodes = nodetree.nodes
    
    # Get parent
    is_parent = []
    for node in nodes:
        if node.parent is None:
            is_parent += [1]
        else:
            is_parent += [0]
    
    # Get average pos of all nodes
    pos = numpy.zeros(len(nodes)*2)
    nodes.foreach_get('location', pos)
    
    avg_pos = numpy.average(pos.reshape(-1,2), axis=0, weights=is_parent)
    
    # make avg_pos align to the grid
    avg_pos = (avg_pos[0] - avg_pos[0] % nodegridscale, avg_pos[1] - avg_pos[1] % nodegridscale)
    
    # Pan the viewport
    delta = numpy.array(nodetree.view_center)-numpy.array(avg_pos)*1.25
    region = bpy.context.region
    deltax, deltay = numpy.array(region.view2d.view_to_region(delta[0], delta[1], clip=False)) - numpy.array(region.view2d.view_to_region(nodetree.view_center[0],nodetree.view_center[1],clip=False))
    bpy.ops.view2d.pan(deltax=deltax, deltay=deltay)
        


@persistent
def nvk_center_nodes(dummy):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'NODE_EDITOR':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        with bpy.context.temp_override(window=window, area=area, region=region):
                            if bpy.context.space_data.edit_tree is not None:
                                center_view(bpy.context.space_data.edit_tree)
        
    
    # Center all nodes in all nodetrees
    for material in bpy.data.materials:
        if not material.node_tree == None:
            nodes_to_origin(material.node_tree)
    
    for scene in bpy.data.scenes:
        if not scene.node_tree == None:
            nodes_to_origin(scene.node_tree)
    
    for nodegroup in bpy.data.node_groups:
        nodes_to_origin(nodegroup)
        
    
    # Update the viewport
    for area in bpy.context.screen.areas:
        area.tag_redraw()
    


def register():
    bpy.app.handlers.save_pre.append(nvk_center_nodes)
    bpy.app.handlers.load_post.append(nvk_center_nodes)

def unregister():
    bpy.app.handlers.save_pre.remove(nvk_center_nodes)
    bpy.app.handlers.load_post.remove(nvk_center_nodes)

if __name__ == "__main__":
    register()