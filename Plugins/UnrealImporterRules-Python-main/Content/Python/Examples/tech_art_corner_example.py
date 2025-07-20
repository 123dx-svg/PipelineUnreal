import unreal
from ImporterRules.Queries import QueryBase
from ImporterRules.Actions import ImportActionBase
from ImporterRules import importer_rules_manager, Rule



#字典用于存储不同类型的文件夹路径
mesh_type_to_directory_mapping = {

    "environment": "Enviro",
    "weapons": "Weapons",
    "decal" : "Decal"
}


class ContainsMeshTypeProperty(QueryBase):
    def test(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:
        EditorAssetSubsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
        if not EditorAssetSubsystem:
            return False
        #资产的元数据类型 提前已经在建模工具中定义
        value = EditorAssetSubsystem.get_metadata_tag(created_object, unreal.Name("FBX.mesh_type"))
        #查找值类型
        if value not in mesh_type_to_directory_mapping:
            print(f"Mesh type '{value}' not found in mapping.")
            return False
        return True
    
class MoveMeshBaseOnType(ImportActionBase):
   def apply(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:
       print("Moving mesh based on type...")
       if created_object is None:
           return False
       
       EditorAssetSubsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
       EditorAssetLibrary = unreal.EditorAssetLibrary()
       value = EditorAssetSubsystem.get_metadata_tag(created_object, unreal.Name("FBX.mesh_type"))

       destination_path = f"/Game/{mesh_type_to_directory_mapping.get(value)}/{created_object.get_name()}"
       EditorAssetLibrary.rename_asset(created_object.get_path_name(), destination_path)

       return True


importer_rules_manager.register_rules(
    class_type=unreal.StaticMesh,
    rules=[
        Rule(
            queries=[
                ContainsMeshTypeProperty(),
            ],
            actions=[
                MoveMeshBaseOnType(),
            ],
            requires_all=True,
            apply_on_reimport=True,  # This rule will apply on reimport as well

        )
    ]

)