# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_eevee_materials_override

# ToDo - override with uv


class EeveeMaterialsOverride:

    _overrider_id = 'eevee_materials_overrider'
    _overrider_name = 'EEVEE Materials Overrider'
    _clay_id = 'eevee_materials_clay'
    _clay_name = 'Clay'

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
                cls.set_override_material(override_nodetree=override_nodetree, material_nodetree=custom_nodetree)
                cls.extend_to_all_materials(scene_data=scene_data)

    @classmethod
    def override_uv_grid(cls, scene_data):
        # override with UV-grid material
        override_nodetree = cls.override_nodegroup(node_groups=scene_data.node_groups)
        # ToDo

    @classmethod
    def extend_to_all_materials(cls, scene_data):
        # extend override node group to all scene materials
        # create override node group
        override_nodegroup = cls.override_nodegroup(node_groups=scene_data.node_groups)
        if override_nodegroup:
            # extend to all materials
            materials = (material for material in scene_data.materials if material.node_tree)
            for material in materials:
                override_node = next((node for node in material.node_tree.nodes if cls._overrider_id in node), None)
                node_material_output = next((node for node in material.node_tree.nodes if node.name == 'Material Output'), None)
                if node_material_output:
                    if not override_node:
                        override_node = material.node_tree.nodes.new(type='ShaderNodeGroup')
                        override_node.node_tree = override_nodegroup
                        override_node[cls._overrider_id] = True  # id marker
                        override_node.name = cls._overrider_name
                        override_node.location = (node_material_output.location.x, node_material_output.location.y + override_node.height + 25)
                    linked = next((link for link in material.node_tree.links if link.to_node == node_material_output and link.from_node == override_node), None)
                    if not linked:
                        link_to_output_node = next((link for link in material.node_tree.links if link.to_node == node_material_output), None)
                        if link_to_output_node:
                            link_to_output_node_from_socket = link_to_output_node.from_socket
                            material.node_tree.links.remove(link_to_output_node)
                            material.node_tree.links.new(link_to_output_node_from_socket, override_node.inputs['Surface'])
                        material.node_tree.links.new(override_node.outputs['BSDF'], node_material_output.inputs['Surface'])

    @classmethod
    def change_mode(cls, scene_data, mode: bool):
        # change override mode (on - off)
        override_nodegroup = cls.override_nodegroup(node_groups=scene_data.node_groups)
        switcher = next((node for node in override_nodegroup.nodes if node.type == 'MIX_SHADER'), None)
        if switcher:
            switcher.inputs['Fac'].default_value = float(mode)

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
                link_to_surface = next((link for link in node_tree.links
                                        if link.to_node == overrider_nodegroup and link.to_socket == overrider_nodegroup.inputs['Surface']), None)
                if link_to_surface:
                    node_tree.links.new(link_to_surface.from_socket, group_output_node.inputs['Surface'])
                # remove overrider node group node
                node_tree.nodes.remove(overrider_nodegroup)
            # if first time
            material_output_node = next((node for node in node_tree.nodes if node.type == 'OUTPUT_MATERIAL'), None)
            if material_output_node:
                link_to_surface = next((link for link in node_tree.links
                                        if link.to_node == material_output_node and link.to_socket == material_output_node.inputs['Surface']), None)
                if link_to_surface:
                    node_tree.links.new(link_to_surface.from_socket, group_output_node.inputs['Surface'])
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
