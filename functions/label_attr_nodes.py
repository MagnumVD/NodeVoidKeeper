def dump(obj):
    for attr in dir(obj):
        if hasattr( obj, attr ):
            print( "obj.%s = %s" % (attr, getattr(obj, attr)))

import bpy

def run(nodetree):
    for node in nodetree.nodes:
        match node.bl_idname:
            case 'GeometryNodeStoreNamedAttribute':
                property=node.inputs['Name']
            case 'GeometryNodeInputNamedAttribute':
                property=node.inputs['Name']
            case 'GeometryNodeRemoveAttribute':
                if node.pattern_mode=='EXACT':
                    property=node.inputs['Name']
                else:
                    continue
                
            case _:
                continue
        
        if property.default_value == '':
            node.label = property.default_value
            node.id_data.interface_update(bpy.context)