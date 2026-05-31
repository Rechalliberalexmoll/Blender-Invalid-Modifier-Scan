# ==========================
# InvalidModifierScan  Lite
# ==========================
bl_info = {
    "name": "Invalid Modifier Scan Lite",
    "author": "You",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Invalid Mod",
    "description": "Only list Boolean & Shrinkwrap with missing targets",
    "category": "Development",
}

import bpy

def scan_invalid_targets():
    bad = []
    for ob in bpy.data.objects:
        for md in ob.modifiers:
            if md.type == 'BOOLEAN' and not md.object:
                bad.append((ob.name, md.name, "Boolean → 无目标"))
            elif md.type == 'SHRINKWRAP' and not md.target:
                bad.append((ob.name, md.name, "Shrinkwrap → 无目标"))
    return bad

class MESH_OT_scan_invalid(bpy.types.Operator):
    bl_idname = "mesh.scan_invalid_mod"
    bl_label = "Scan Invalid Targets"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bad = scan_invalid_targets()
        for ob, md, reason in bad:
            self.report({'ERROR'}, f"{ob} · {md} : {reason}")
        if not bad:
            self.report({'INFO'}, "✅ 所有布尔 & 缩裹目标均有效")
        return {'FINISHED'}

class VIEW3D_PT_invalid_mod(bpy.types.Panel):
    bl_label = "Invalid Mod"
    bl_idname = "VIEW3D_PT_invalid_mod"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Invalid Mod"

    def draw(self, context):
        self.layout.operator(MESH_OT_scan_invalid.bl_idname, icon='MODIFIER')

classes = (MESH_OT_scan_invalid, VIEW3D_PT_invalid_mod)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()