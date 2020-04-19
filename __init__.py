# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_eevee_materials_override

from . import eevee_materials_override_params
from . import eevee_materials_override_ops
from . import eevee_materials_override_panel
from .addon import Addon


bl_info = {
    'name': 'eevee_materials_override',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 83, 0),
    'location': 'N-Panel > Override',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-add-on-e…terials-override/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-e…terials-override/',
    'description': 'Global scene materials override for the EEVEE render engine'
}


def register():
    if not Addon.dev_mode():
        eevee_materials_override_params.register()
        eevee_materials_override_ops.register()
        eevee_materials_override_panel.register()
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version!')


def unregister():
    if not Addon.dev_mode():
        eevee_materials_override_panel.unregister()
        eevee_materials_override_ops.unregister()
        eevee_materials_override_params.unregister()


if __name__ == '__main__':
    register()
