# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_eevee_materials_override

import bpy
from bpy.types import Panel, UIList
from bpy.utils import register_class, unregister_class


class EEVEE_MATERIALS_OVERRIDE_PT_panel(Panel):
    bl_idname = 'EEVEE_MATERIALS_OVERRIDE_PT_panel'
    bl_label = 'Materials Override - Materials mode'
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
        box = layout.box()
        box.label(text='Exclude material from override')
        box.template_list(
            listtype_name='EEVEE_MATERIALS_OVERRIDE_UL_materials_list',
            list_id='Mat_list',
            dataptr=bpy.data,
            propname='materials',
            active_dataptr=context.window_manager,
            active_propname='eevee_materials_override_fake_index'
        )


class EEVEE_MATERIALS_OVERRIDE_PT_panel_obj(Panel):
    bl_idname = 'EEVEE_MATERIALS_OVERRIDE_PT_panel_obj'
    bl_label = 'Materials Override - Objects mode'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Override'

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        # override
        box.label(text='Override for selected objects with:')
        op = box.operator('eevee_materials_override.override_selected', icon='SHADING_RENDERED', text='Clay')
        op.material_type = 'CLAY'
        op = box.operator('eevee_materials_override.override_selected', icon='UV', text='UV Grid')
        op.material_type = 'UV_GRID'
        op = box.operator('eevee_materials_override.override_selected', icon='MATERIAL', text='Custom Material')
        op.material_type = 'CUSTOM'
        box.prop(context.window_manager.eevee_materials_override_vars, 'custom_material', text='')
        # restore
        layout.operator('eevee_materials_override.restore_selected', icon='LOOP_BACK')


class EEVEE_MATERIALS_OVERRIDE_PT_panel_clean(Panel):
    bl_idname = 'EEVEE_MATERIALS_OVERRIDE_PT_panel_clean'
    bl_label = 'Materials Override - Cleaning'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Override'

    def draw(self, context):
        layout = self.layout
        # Materials mode
        box = layout.box()
        box.label(text='For All Materials:')
        box.operator('eevee_materials_override.clean_materials', icon='BRUSH_DATA')
        # Objects mode
        box = layout.box()
        box.label(text='For All Objects:')
        box.operator('eevee_materials_override.remove_backup', icon='CANCEL')


class EEVEE_MATERIALS_OVERRIDE_UL_materials_list(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index=0, flt_flag=0):
        layout.label(text=item.name, icon_value=icon)
        layout.separator(factor=2.0)
        layout.prop(data=item, property='eevee_materials_override_exclude', text='excluded')


def register():
    register_class(EEVEE_MATERIALS_OVERRIDE_UL_materials_list)
    register_class(EEVEE_MATERIALS_OVERRIDE_PT_panel)
    register_class(EEVEE_MATERIALS_OVERRIDE_PT_panel_obj)
    register_class(EEVEE_MATERIALS_OVERRIDE_PT_panel_clean)


def unregister():
    unregister_class(EEVEE_MATERIALS_OVERRIDE_PT_panel_clean)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_PT_panel_obj)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_PT_panel)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_UL_materials_list)
