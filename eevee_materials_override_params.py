# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_eevee_materials_override

import bpy
from bpy.props import BoolProperty, PointerProperty
from bpy.types import PropertyGroup, WindowManager, Material
from bpy.utils import register_class, unregister_class
from .eevee_materials_override import EeveeMaterialsOverride


class EEVEE_MATERIALS_OVERRIDE_Vars(PropertyGroup):

    enable: BoolProperty(
        default=False,
        name='Enable',
        update=lambda self, context: EeveeMaterialsOverride.change_mode(
            scene_data=bpy.data,
            mode=self.enable
        )
    )

    custom_material: PointerProperty(
        type=Material
    )


def register():
    register_class(EEVEE_MATERIALS_OVERRIDE_Vars)
    WindowManager.eevee_materials_override_vars = PointerProperty(type=EEVEE_MATERIALS_OVERRIDE_Vars)


def unregister():
    del WindowManager.eevee_materials_override_vars
    unregister_class(EEVEE_MATERIALS_OVERRIDE_Vars)
