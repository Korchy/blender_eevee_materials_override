# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_eevee_materials_override

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .eevee_materials_override import EeveeMaterialsOverride


class EEVEE_MATERIALS_OVERRIDE_OT_extend_to_all(Operator):
    bl_idname = 'eevee_materials_override.extend_to_all'
    bl_label = 'Extend to all materials'
    bl_description = 'Extend override to all scene materials'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        EeveeMaterialsOverride.extend_to_all_materials(
            scene_data=bpy.data
        )
        context.window_manager.eevee_materials_override_vars.enable = True
        return {'FINISHED'}


class EEVEE_MATERIALS_OVERRIDE_OT_clay_override(Operator):
    bl_idname = 'eevee_materials_override.clay_override'
    bl_label = 'Override with Clay'
    bl_description = 'Override with clay material'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        EeveeMaterialsOverride.override_clay(
            scene_data=bpy.data
        )
        context.window_manager.eevee_materials_override_vars.enable = True
        return {'FINISHED'}


class EEVEE_MATERIALS_OVERRIDE_OT_uv_grid_override(Operator):
    bl_idname = 'eevee_materials_override.uv_grid_override'
    bl_label = 'Override with UV Grid'
    bl_description = 'Override with UV Grid material'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        EeveeMaterialsOverride.override_uv_grid(
            scene_data=bpy.data
        )
        context.window_manager.eevee_materials_override_vars.enable = True
        return {'FINISHED'}


class EEVEE_MATERIALS_OVERRIDE_OT_custom_override(Operator):
    bl_idname = 'eevee_materials_override.custom_override'
    bl_label = 'Override with Custom Material'
    bl_description = 'Override with custom material'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        EeveeMaterialsOverride.override_custom(
            scene_data=bpy.data,
            custom_material=context.window_manager.eevee_materials_override_vars.custom_material
        )
        context.window_manager.eevee_materials_override_vars.enable = True
        return {'FINISHED'}


class EEVEE_MATERIALS_OVERRIDE_OT_clean_materials(Operator):
    bl_idname = 'eevee_materials_override.clean_materials'
    bl_label = 'Clean'
    bl_description = 'Clean all materials from override node groups'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        EeveeMaterialsOverride.clean_materials(
            scene_data=bpy.data
        )
        context.window_manager.eevee_materials_override_vars.enable = False
        return {'FINISHED'}


class EEVEE_MATERIALS_OVERRIDE_OT_override_selected(Operator):
    bl_idname = 'eevee_materials_override.override_selected'
    bl_label = 'Override for selected objects'
    bl_description = 'Override materials for selected objects'
    bl_options = {'REGISTER', 'UNDO'}

    material_type: EnumProperty(
        items=[
            ('CLAY', 'CLAY', 'CLAY'),
            ('UV_GRID', 'UV_GRID', 'UV_GRID'),
            ('CUSTOM', 'CUSTOM', 'CUSTOM')
        ]
    )

    def execute(self, context):
        EeveeMaterialsOverride.override_objects(
            context=context,
            scene_data=bpy.data,
            objects=context.selected_objects,
            material_type=self.material_type
        )
        return {'FINISHED'}


class EEVEE_MATERIALS_OVERRIDE_OT_restore_selected(Operator):
    bl_idname = 'eevee_materials_override.restore_selected'
    bl_label = 'Restore for Selected Objects'
    bl_description = 'Restore materials for selected objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # restore materials from backup for selected objects
        EeveeMaterialsOverride.restore_objects(
            objects=context.selected_objects
        )
        return {'FINISHED'}


class EEVEE_MATERIALS_OVERRIDE_OT_remove_backup(Operator):
    bl_idname = 'eevee_materials_override.remove_backup'
    bl_label = 'Remove Backup'
    bl_description = 'Remove Materials Backup for all Objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # remove all backup for all objects
        EeveeMaterialsOverride.remove_all_objects_backup(
            scene_data=bpy.data
        )
        return {'FINISHED'}


def register():
    register_class(EEVEE_MATERIALS_OVERRIDE_OT_extend_to_all)
    register_class(EEVEE_MATERIALS_OVERRIDE_OT_clay_override)
    register_class(EEVEE_MATERIALS_OVERRIDE_OT_uv_grid_override)
    register_class(EEVEE_MATERIALS_OVERRIDE_OT_custom_override)
    register_class(EEVEE_MATERIALS_OVERRIDE_OT_clean_materials)
    register_class(EEVEE_MATERIALS_OVERRIDE_OT_override_selected)
    register_class(EEVEE_MATERIALS_OVERRIDE_OT_restore_selected)
    register_class(EEVEE_MATERIALS_OVERRIDE_OT_remove_backup)


def unregister():
    unregister_class(EEVEE_MATERIALS_OVERRIDE_OT_remove_backup)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_OT_restore_selected)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_OT_override_selected)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_OT_clean_materials)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_OT_custom_override)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_OT_uv_grid_override)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_OT_clay_override)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_OT_extend_to_all)
