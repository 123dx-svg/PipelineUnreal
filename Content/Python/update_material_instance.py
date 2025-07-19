import unreal

EditorAssetLibrary = unreal.EditorAssetLibrary()
MaterialEditingLibrary = unreal.MaterialEditingLibrary()

def set_material_vector(material_instace:unreal.MaterialInstanceConstant,parameter_name:unreal.Name,value)->bool:
    #异常处理
    assert parameter_name in MaterialEditingLibrary.get_vector_parameter_names(material_instace)
    return MaterialEditingLibrary.set_material_instance_vector_parameter_value(instance = material_instace,parameter_name=parameter_name,value=value)

instance:unreal.MaterialInstanceConstant = EditorAssetLibrary.load_asset(
    "/Game/StarterContent/Materials/MI_Example")

MaterialEditingLibrary.clear_all_material_instance_parameters(instance)

set_material_vector(material_instace=instance,parameter_name="Emissive color 01",value=[0.1,0.2,0.3,0.4])
set_material_vector(material_instace=instance,parameter_name="Emissive color 02",value=[0.1,0.2,0.3,0.4])

#重新更新Shader
MaterialEditingLibrary.update_material_instance(instance)