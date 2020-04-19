# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_eevee_materials_override


import json
import os


class Addon:

    cfg_file_name = 'cfg.json'

    @classmethod
    def dev_mode(cls):
        rez = False
        conf_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), cls.cfg_file_name)
        if os.path.exists(conf_file_path):
            with open(conf_file_path) as conf_file:
                json_data = json.load(conf_file)
                if 'dev_mode' in json_data and json_data['dev_mode']:
                    rez = True
                conf_file.close()
        return rez
