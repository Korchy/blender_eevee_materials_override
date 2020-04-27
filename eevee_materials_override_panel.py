# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_eevee_materials_override

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class EEVEE_MATERIALS_OVERRIDE_PT_panel(Panel):
    bl_idname = 'EEVEE_MATERIALS_OVERRIDE_PT_panel'
    bl_label = 'EEVEE Materials Override'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Override'

    def draw(self, context):
        layout = self.layout
        split = layout.split(factor=0.85)
        col_l = split.column()
        col_r = split.column()
        if context.window_manager.eevee_materials_override_vars.enable:
            col_l.prop(context.window_manager.eevee_materials_override_vars, 'enable', icon='PAUSE', text='Disable')
        else:
            col_l.prop(context.window_manager.eevee_materials_override_vars, 'enable', icon='PLAY', text='Enable')
        col_r.operator('eevee_materials_override.extend_to_all', icon='CON_LOCLIKE', text='')
        box = layout.box()
        box.label(text='Override with:')
        box.operator('eevee_materials_override.clay_override', icon='SHADING_RENDERED', text='Clay')
        box.operator('eevee_materials_override.uv_grid_override', icon='UV', text='UV Grid')
        box.operator('eevee_materials_override.custom_override', icon='MATERIAL', text='Custom Material')
        box.prop(context.window_manager.eevee_materials_override_vars, 'custom_material', text='')


def register():
    register_class(EEVEE_MATERIALS_OVERRIDE_PT_panel)


def unregister():
    unregister_class(EEVEE_MATERIALS_OVERRIDE_PT_panel)
