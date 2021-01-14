# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_eevee_materials_override

import bpy
from bpy.props import BoolProperty, PointerProperty, IntProperty, CollectionProperty
from bpy.types import PropertyGroup, WindowManager, Material, Object
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
        # link to the user material for override
        type=Material
    )


class EEVEE_MATERIALS_OVERRIDE_obj_mat_backup(PropertyGroup):

    material: PointerProperty(
        # link to the material which was override for current object (its material slot)
        type=Material
    )


def register():
    register_class(EEVEE_MATERIALS_OVERRIDE_Vars)
    register_class(EEVEE_MATERIALS_OVERRIDE_obj_mat_backup)
    WindowManager.eevee_materials_override_vars = PointerProperty(type=EEVEE_MATERIALS_OVERRIDE_Vars)
    WindowManager.eevee_materials_override_fake_index = IntProperty()   # fake index for excluded materials list
    Material.eevee_materials_override_exclude = BoolProperty(
        default=False,
        update=lambda self, context: EeveeMaterialsOverride.change_material_exclude(self)
    )
    Object.eevee_materials_override_mat_backup = CollectionProperty(type=EEVEE_MATERIALS_OVERRIDE_obj_mat_backup)


def unregister():
    del Object.eevee_materials_override_mat_backup
    del WindowManager.eevee_materials_override_fake_index
    del WindowManager.eevee_materials_override_vars
    del Material.eevee_materials_override_exclude
    unregister_class(EEVEE_MATERIALS_OVERRIDE_obj_mat_backup)
    unregister_class(EEVEE_MATERIALS_OVERRIDE_Vars)
