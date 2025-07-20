import unreal

import_subsystem = None
registered_once = False

mesh_type_to_directory_mapping = {

    "environment": "Enviro",
    "weapons": "Weapons",
    "decal" : "Decal"
}

def my_post_import_callback(factory:unreal.Factory, created_object:unreal.Object):
    unreal.log(f"Post Import :Factory: {factory}")
    unreal.log(f"Post Import :Created Object: {created_object}")

    if not isinstance(created_object, unreal.StaticMesh):
        return
    
    EditorAssetSubsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    if not EditorAssetSubsystem:
        return
    # 通过Tag判断是否第一次导入
    is_reimport = "True" == EditorAssetSubsystem.get_metadata_tag(created_object, unreal.Name("importer_rules_applied"))
    print(f"{'Reimport' if is_reimport else 'First Import'}")

    EditorAssetSubsystem.set_metadata_tag(created_object, unreal.Name("importer_rules_applied"), "True")
    

    EditorAssetLibrary = unreal.EditorAssetLibrary()
    value = EditorAssetSubsystem.get_metadata_tag(created_object, unreal.Name("FBX.mesh_type"))
    destination_path = f"/Game/{mesh_type_to_directory_mapping.get(value)}/{created_object.get_name()}"
    EditorAssetLibrary.rename_asset(created_object.get_path_name(), destination_path)



def register_import_callback():
    global import_subsystem,registered_once

#防止重复注册
    if registered_once:
        return
    registered_once = True

    import_subsystem = unreal.get_editor_subsystem(unreal.ImportSubsystem)
    import_subsystem.on_asset_post_import.add_callable(my_post_import_callback)