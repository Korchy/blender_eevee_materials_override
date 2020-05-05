# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_eevee_materials_override

from bpy.types import AddonPreferences
from bpy.props import BoolProperty
from bpy.utils import register_class, unregister_class


class EEVEE_MATERIALS_OVERRIDE_preferences(AddonPreferences):

    bl_idname = __package__

    override_no_material: BoolProperty(
        default=True,
        name='Override on objects without material'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'override_no_material')


def register():
    register_class(EEVEE_MATERIALS_OVERRIDE_preferences)


def unregister():
    unregister_class(EEVEE_MATERIALS_OVERRIDE_preferences)
