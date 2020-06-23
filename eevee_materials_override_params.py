# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_eevee_materials_override

import bpy
from bpy.props import BoolProperty, PointerProperty, IntProperty
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
        # link to user material for override
        type=Material
    )


def register():
    register_class(EEVEE_MATERIALS_OVERRIDE_Vars)
    WindowManager.eevee_materials_override_vars = PointerProperty(type=EEVEE_MATERIALS_OVERRIDE_Vars)
    Material.eevee_materials_override_exclude = BoolProperty(
        default=False,
        update=lambda self, context: EeveeMaterialsOverride.change_material_exclude(self)
    )
    WindowManager.eevee_materials_override_fake_index = IntProperty()   # fake index for excluded materials list


def unregister():
    del WindowManager.eevee_materials_override_fake_index
    del Material.eevee_materials_override_exclude
    del WindowManager.eevee_materials_override_vars
    unregister_class(EEVEE_MATERIALS_OVERRIDE_Vars)
