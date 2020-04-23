# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_eevee_materials_override

import bpy
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


def register():
    register_class(EEVEE_MATERIALS_OVERRIDE_OT_extend_to_all)
    register_class(EEVEE_MATERIALS_OVERRIDE_OT_clay_override)
    register_class(EEVEE_MATERIALS_OVERRIDE_OT_uv_grid_override)
    register_class(EEVEE_MATERIALS_OVERRIDE_OT_custom_override)


def unregister():
    unregister_class(EEVEE_MATERIALS_OVERRIDE_OT_custom_override)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_OT_uv_grid_override)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_OT_clay_override)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_OT_extend_to_all)
