# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_eevee_materials_override

import bpy


class EeveeMaterialsOverride:

    _overrider_id = 'eevee_materials_overrider'
    _overrider_name = 'EEVEE Materials Overrider'
    _clay_id = 'eevee_materials_clay'
    _clay_name = 'Clay'
    _uv_grid_id = 'eevee_materials_uv_grid'
    _uv_grid_name = 'UVGrid'
    _default_override_material_name = 'eevee_override_default'
    _override_base = 'override_base'    # marker for base materials for override (don't override themself)

    @classmethod
    def override_clay(cls, scene_data):
        # override with clay material
        override_nodetree = cls.override_nodegroup(node_groups=scene_data.node_groups)
        clay_nodetree = cls.clay_nodegroup(node_groups=scene_data.node_groups)
        cls.set_override_material(override_nodetree=override_nodetree, material_nodetree=clay_nodetree)
        cls.extend_to_all_materials(scene_data=scene_data)

    @classmethod
    def override_custom(cls, scene_data, custom_material):
        # override with custom material
        if custom_material:
            override_nodetree = cls.override_nodegroup(node_groups=scene_data.node_groups)
            custom_nodetree = cls.node_tree_from_material(material=custom_material)
            if custom_nodetree:
                cls.set_override_material(
                    override_nodetree=override_nodetree,
                    material_nodetree=custom_nodetree
                )
                cls.extend_to_all_materials(scene_data=scene_data)

    @classmethod
    def override_uv_grid(cls, scene_data):
        # override with UV-grid material
        override_nodetree = cls.override_nodegroup(node_groups=scene_data.node_groups)
        uv_grid_nodetree = cls.uv_grid_nodegroup(scene_data=scene_data)
        cls.set_override_material(override_nodetree=override_nodetree, material_nodetree=uv_grid_nodetree)
        cls.extend_to_all_materials(scene_data=scene_data)

    @classmethod
    def extend_to_all_materials(cls, scene_data):
        # extend override node group to all scene materials
        # create override node group
        override_nodegroup = cls.override_nodegroup(node_groups=scene_data.node_groups)
        if override_nodegroup:
            # init objects without material with the default material
            if bpy.context.preferences.addons[__package__].preferences.override_no_material:
                cls._default_material_init(scene_data=scene_data)
            # extend to all materials
            materials = (material for material in scene_data.materials
                         if material.node_tree and cls._override_base not in material)
            for material in materials:
                override_node = next((node for node in material.node_tree.nodes if cls._overrider_id in node), None)
                # node_material_output = next((node for node in material.node_tree.nodes
                #                              if node.name == 'Material Output'), None)
                node_material_output = next(
                    (node for node in material.node_tree.nodes
                     if node.type == 'OUTPUT_MATERIAL' and node.is_active_output is True),
                    None)
                if node_material_output:
                    if not override_node:
                        override_node = material.node_tree.nodes.new(type='ShaderNodeGroup')
                        override_node.node_tree = override_nodegroup
                        override_node[cls._overrider_id] = True  # id marker
                        override_node.name = cls._overrider_name
                        override_node.location = (node_material_output.location.x,
                                                  node_material_output.location.y + override_node.height + 25)
                    linked = next((link for link in material.node_tree.links
                                   if link.to_node == node_material_output and link.from_node == override_node), None)
                    if not linked:
                        link_to_output_node = next(
                            (link for link in material.node_tree.links
                             if link.to_node == node_material_output
                             and link.to_socket == node_material_output.inputs['Surface']),
                            None)
                        if link_to_output_node:
                            link_to_output_node_from_socket = link_to_output_node.from_socket
                            material.node_tree.links.remove(link_to_output_node)
                            material.node_tree.links.new(
                                link_to_output_node_from_socket,
                                override_node.inputs['Surface']
                            )
                        material.node_tree.links.new(
                            override_node.outputs['BSDF'],
                            node_material_output.inputs['Surface']
                        )
                # if this material excluded from override - mute override node group
                if material.eevee_materials_override_exclude and override_node:
                    override_node.mute = True

    @classmethod
    def override_objects(cls, context, scene_data, objects, material_type: str):
        # override materials for objects
        # get material to override
        material = None
        if material_type == 'CLAY':
            material = cls.clay_material(scene_data=scene_data)
        elif material_type == 'UV_GRID':
            material = cls.uv_grid_material(scene_data=scene_data)
        elif material_type == 'CUSTOM':
            material = context.window_manager.eevee_materials_override_vars.custom_material
        if material:
            # first - only backup for all objects (or linked objects backups already override material)
            for obj in objects:
                if not obj.eevee_materials_override_mat_backup:     # if already has backup - no more backups
                    # backup current material by slots
                    for slot in obj.material_slots:
                        mat_backup = obj.eevee_materials_override_mat_backup.add()
                        mat_backup.material = slot.material
            # next - override
            for obj in objects:
                for slot in obj.material_slots:
                    # slot.link = 'OBJECT'    # 'DATA'  - don't override on linked objects - need to be backup and restore as materials
                    slot.material = material

    @classmethod
    def restore_objects(cls, objects):
        # restore override materials for objects
        for obj in objects:
            for i, material_backup in enumerate(obj.eevee_materials_override_mat_backup):
                obj.material_slots[i].material = obj.eevee_materials_override_mat_backup[0].material
                obj.eevee_materials_override_mat_backup.remove(0)

    @classmethod
    def change_mode(cls, scene_data, mode: bool):
        # change override mode (on - off)
        override_nodegroup = cls.override_nodegroup(node_groups=scene_data.node_groups)
        switcher = next((node for node in override_nodegroup.nodes if node.type == 'MIX_SHADER'), None)
        if switcher:
            switcher.inputs['Fac'].default_value = float(mode)

    @classmethod
    def change_material_exclude(cls, material):
        # change exclude from override property for current material
        if material.node_tree:
            override_node = next((node for node in material.node_tree.nodes if cls._overrider_id in node), None)
            if override_node:
                override_node.mute = float(material.eevee_materials_override_exclude)

    @staticmethod
    def set_override_material(override_nodetree, material_nodetree):
        # set material to override
        # remove current
        for node in override_nodetree.nodes:
            if node.type == 'GROUP':
                override_nodetree.nodes.remove(node)
        # set new
        material_node = override_nodetree.nodes.new(type='ShaderNodeGroup')
        material_node.location = (-200, -100)
        material_node.node_tree = material_nodetree
        if material_node.node_tree:
            # link to switcher
            switcher = next((node for node in override_nodetree.nodes if node.type == 'MIX_SHADER'), None)
            if switcher:
                override_nodetree.links.new(material_node.outputs[0], switcher.inputs[2])

    @classmethod
    def override_nodegroup(cls, node_groups: list):
        # create override node group
        nodegroup = next((nodegroup for nodegroup in node_groups if cls._overrider_id in nodegroup), None)
        if not nodegroup:
            nodegroup = node_groups.new(cls._overrider_name, 'ShaderNodeTree')
            nodegroup[cls._overrider_id] = True  # id marker
            # inputs
            nodegroup.inputs.new('NodeSocketShader', 'Surface')
            # outputs
            nodegroup.outputs.new('NodeSocketShader', 'BSDF')
            # nodes
            group_input_node = nodegroup.nodes.new('NodeGroupInput')
            group_input_node.location = (-200, 0)
            group_output_node = nodegroup.nodes.new('NodeGroupOutput')
            group_output_node.location = (200, 0)
            mix_shader_node = nodegroup.nodes.new('ShaderNodeMixShader')
            mix_shader_node.location = (0, 0)
            mix_shader_node.inputs['Fac'].default_value = 0
            # links
            nodegroup.links.new(group_input_node.outputs['Surface'], mix_shader_node.inputs[1])
            nodegroup.links.new(mix_shader_node.outputs[0], group_output_node.inputs['BSDF'])
        return nodegroup

    @classmethod
    def clay_material(cls, scene_data):
        # create "clay" material
        clay_material = next((material for material in scene_data.materials if cls._clay_id in material), None)
        if not clay_material:
            # create new
            clay_material = scene_data.materials.new(name=cls._clay_name)
            clay_material.use_nodes = True
            clay_material[cls._override_base] = True    # override base material
            clay_material[cls._clay_id] = True          # id marker
            output_node = next(
                (node for node in clay_material.node_tree.nodes if node.type == 'OUTPUT_MATERIAL'),
                None)
            for node in clay_material.node_tree.nodes:
                if node != output_node:
                    clay_material.node_tree.nodes.remove(node)
            # add material node group
            material_node = clay_material.node_tree.nodes.new(type='ShaderNodeGroup')
            material_node.location = (0, 0)
            material_node.node_tree = cls.clay_nodegroup(
                node_groups=scene_data.node_groups
            )
            # links
            clay_material.node_tree.links.new(material_node.outputs['BSDF'], output_node.inputs[0])
        return clay_material

    @classmethod
    def clay_nodegroup(cls, node_groups: list):
        # create clay node group
        nodegroup = next((nodegroup for nodegroup in node_groups if cls._clay_id in nodegroup), None)
        if not nodegroup:
            nodegroup = node_groups.new(cls._clay_name, 'ShaderNodeTree')
            nodegroup[cls._clay_id] = True  # id marker
            # outputs
            nodegroup.outputs.new('NodeSocketShader', 'BSDF')
            # group input/output nodes
            group_input_node = nodegroup.nodes.new('NodeGroupInput')
            group_input_node.location = (-800, 200)
            group_output_node = nodegroup.nodes.new('NodeGroupOutput')
            group_output_node.location = (300, 200)
            # nodes
            layer_weight = nodegroup.nodes.new('ShaderNodeLayerWeight')
            layer_weight.location = (-568.7, 211.2)
            layer_weight.inputs[0].default_value = 0.35
            diffuse_bsdf = nodegroup.nodes.new('ShaderNodeBsdfDiffuse')
            diffuse_bsdf.location = (-180.3, 257.4)
            fresnel = nodegroup.nodes.new('ShaderNodeFresnel')
            fresnel.location = (-175.7, 372.2)
            fresnel.inputs[0].default_value = 1.55
            glossy_bsdf = nodegroup.nodes.new('ShaderNodeBsdfGlossy')
            glossy_bsdf.location = (-180.6, 123.2)
            glossy_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
            glossy_bsdf.inputs[1].default_value = 0.45
            mix = nodegroup.nodes.new('ShaderNodeMixRGB')
            mix.location = (-371.1, 258.9)
            mix.inputs[1].default_value = (0.8, 0.258, 0.092, 1.0)
            mix.inputs[2].default_value = (0.533, 0.175, 0.064, 1.0)
            mix_shader = nodegroup.nodes.new('ShaderNodeMixShader')
            mix_shader.location = (99.1, 275.6)
            # links
            nodegroup.links.new(diffuse_bsdf.outputs[0], mix_shader.inputs[1])
            nodegroup.links.new(glossy_bsdf.outputs[0], mix_shader.inputs[2])
            nodegroup.links.new(layer_weight.outputs[1], mix.inputs[0])
            nodegroup.links.new(mix.outputs[0], diffuse_bsdf.inputs[0])
            nodegroup.links.new(fresnel.outputs[0], mix_shader.inputs[0])
            nodegroup.links.new(mix_shader.outputs[0], group_output_node.inputs[0])
        return nodegroup

    @classmethod
    def node_tree_from_material(cls, material):
        # create node tree from material node tree
        node_tree = None
        if material.node_tree:
            node_tree = material.node_tree.copy()
            # modify node tree to be compatible with node group
            # outputs
            node_tree.outputs.new('NodeSocketShader', 'Surface')
            node_tree.outputs.new('NodeSocketShader', 'Volume')
            node_tree.outputs.new('NodeSocketVector', 'Displacement')
            # input/output nodes
            group_input_node = node_tree.nodes.new('NodeGroupInput')
            group_input_node.location = (-800, 200)
            group_output_node = node_tree.nodes.new('NodeGroupOutput')
            group_output_node.location = (300, 200)
            # if recreation - remove overrider node group
            overrider_nodegroup = next((node for node in node_tree.nodes if cls._overrider_id in node), None)
            if overrider_nodegroup:
                link_to_surface = next(
                    (link for link in node_tree.links
                     if link.to_node == overrider_nodegroup
                     and link.to_socket == overrider_nodegroup.inputs['Surface']),
                    None)
                if link_to_surface:
                    node_tree.links.new(
                        link_to_surface.from_socket,
                        group_output_node.inputs['Surface']
                    )
                # remove overrider node group node
                node_tree.nodes.remove(overrider_nodegroup)
            # if first time
            material_output_node = next(
                (node for node in node_tree.nodes if node.type == 'OUTPUT_MATERIAL'),
                None)
            if material_output_node:
                link_to_surface = next(
                    (link for link in node_tree.links
                     if link.to_node == material_output_node
                     and link.to_socket == material_output_node.inputs['Surface']),
                    None)
                if link_to_surface:
                    node_tree.links.new(
                        link_to_surface.from_socket,
                        group_output_node.inputs['Surface']
                    )
                link_to_volume = next((link for link in node_tree.links
                                       if link.to_node == material_output_node and link.to_socket == material_output_node.inputs['Volume']), None)
                if link_to_volume:
                    node_tree.links.new(link_to_volume.from_socket, group_output_node.inputs['Volume'])
                link_to_displace = next((link for link in node_tree.links
                                         if link.to_node == material_output_node and link.to_socket == material_output_node.inputs['Displacement']), None)
                if link_to_displace:
                    node_tree.links.new(link_to_displace.from_socket, group_output_node.inputs['Displacement'])
                # remove material output node
                node_tree.nodes.remove(material_output_node)
        # this doesn't works to save created from material node tree to node groups
        # nodegroup_node_tree = bpy.data.node_groups.new(cls._custom_name, 'ShaderNodeTree')
        # nodegroup_node_tree = node_tree
        return node_tree

    @classmethod
    def uv_grid_material(cls, scene_data):
        # create "uv_grid" material
        uv_grid_material = next((material for material in scene_data.materials if cls._uv_grid_id in material), None)
        if not uv_grid_material:
            # create new
            uv_grid_material = scene_data.materials.new(name=cls._uv_grid_name)
            uv_grid_material.use_nodes = True
            uv_grid_material[cls._override_base] = True    # override base material
            uv_grid_material[cls._uv_grid_id] = True       # id marker
            output_node = next(
                (node for node in uv_grid_material.node_tree.nodes
                 if node.type == 'OUTPUT_MATERIAL'),
                None)
            for node in uv_grid_material.node_tree.nodes:
                if node != output_node:
                    uv_grid_material.node_tree.nodes.remove(node)
            # add material node group
            material_node = uv_grid_material.node_tree.nodes.new(type='ShaderNodeGroup')
            material_node.location = (0, 0)
            material_node.node_tree = cls.uv_grid_nodegroup(
                scene_data=scene_data
            )
            # links
            uv_grid_material.node_tree.links.new(material_node.outputs['BSDF'], output_node.inputs[0])
        return uv_grid_material

    @classmethod
    def uv_grid_nodegroup(cls, scene_data):
        # create uv grid node group
        nodegroup = next((nodegroup for nodegroup in scene_data.node_groups if cls._uv_grid_id in nodegroup), None)
        if not nodegroup:
            nodegroup = scene_data.node_groups.new(cls._uv_grid_name, 'ShaderNodeTree')
            nodegroup[cls._uv_grid_id] = True  # id marker
            # outputs
            nodegroup.outputs.new('NodeSocketShader', 'BSDF')
            # group input/output nodes
            group_input_node = nodegroup.nodes.new('NodeGroupInput')
            group_input_node.location = (-800, 200)
            group_output_node = nodegroup.nodes.new('NodeGroupOutput')
            group_output_node.location = (300, 200)
            # nodes
            diffuse_bsdf = nodegroup.nodes.new('ShaderNodeBsdfDiffuse')
            diffuse_bsdf.location = (50.0, 300.0)
            image_texture = nodegroup.nodes.new('ShaderNodeTexImage')
            image_texture.location = (-250.0, 300.0)
            uv_grid_image = cls.uv_grid_image(scene_images=scene_data.images)
            if uv_grid_image:
                image_texture.image = uv_grid_image
            mapping = nodegroup.nodes.new('ShaderNodeMapping')
            mapping.location = (-500.0, 300.0)
            mapping.inputs['Scale'].default_value = (0.5, 0.5, 0.5)
            texture_coordinate = nodegroup.nodes.new('ShaderNodeTexCoord')
            texture_coordinate.location = (-650.0, 300.0)
            # links
            nodegroup.links.new(image_texture.outputs[0], diffuse_bsdf.inputs[0])
            nodegroup.links.new(mapping.outputs[0], image_texture.inputs[0])
            nodegroup.links.new(texture_coordinate.outputs[2], mapping.inputs[0])
            nodegroup.links.new(diffuse_bsdf.outputs[0], group_output_node.inputs[0])
        return nodegroup

    @classmethod
    def uv_grid_image(cls, scene_images):
        # get uv grid image
        uv_grid_image = next((image for image in scene_images if cls._uv_grid_id in image), None)
        if not uv_grid_image:
            existing_images = set(scene_images)
            bpy.ops.image.new(name=cls._uv_grid_name, width=1024, height=1024, generated_type='UV_GRID')
            uv_grid_image = list(set(scene_images) - existing_images)[0]
            uv_grid_image[cls._uv_grid_id] = True  # id marker
        return uv_grid_image

    @classmethod
    def clean_materials(cls, scene_data):
        # remove all override node groups from all materials
        materials = (material for material in scene_data.materials
                     if material.node_tree and cls._override_base not in material)
        for material in materials:
            override_node = next((node for node in material.node_tree.nodes if cls._overrider_id in node), None)
            if override_node:
                link_to_override_node = next((link for link in material.node_tree.links
                                              if link.to_node == override_node), None)
                if link_to_override_node:
                    output_node = next(
                        (node for node in material.node_tree.nodes
                         if node.type == 'OUTPUT_MATERIAL' and node.is_active_output is True),
                        None)
                    material.node_tree.links.new(link_to_override_node.from_socket, output_node.inputs[0])
                material.node_tree.nodes.remove(override_node)

    @classmethod
    def remove_all_objects_backup(cls, scene_data):
        # remove all materials backup from all objects (without restoring)
        for obj in scene_data.objects:
            obj.eevee_materials_override_mat_backup.clear()

    @classmethod
    def _default_material_init(cls, scene_data):
        # init objects without material with the default material
        no_material_objects = (obj for obj in scene_data.objects if not obj.active_material and obj.type in ('MESH', 'CURVE'))
        if no_material_objects:
            # create default materials
            default_override_material = next((material for material in scene_data.materials if material.name == cls._default_override_material_name), None)
            if not default_override_material:
                default_override_material = scene_data.materials.new(name=cls._default_override_material_name)
                default_override_material.use_nodes = True
                default_override_material.use_fake_user = True
            if default_override_material:
                # assign default material to all objects without materials
                for obj in no_material_objects:
                    obj.active_material = default_override_material
