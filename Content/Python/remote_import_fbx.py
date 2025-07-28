

from pathlib import Path
import unreal

@unreal.uclass()
class RemoteImporter(unreal.Object):
    @unreal.ufunction(ret=bool,params=[str,str],meta=dict(Category = "Tech"))
    def import_fbx(self,source_path,ue_destination):
        static_mesh_import_data = unreal.FbxStaticMeshImportData()
        static_mesh_import_data.combine_meshes = True
        static_mesh_import_data.remove_degenerates = True


        options = unreal.FbxImportUI()
        options.import_mesh = True
        options.import_textures = False
        options.import_materials = True
        options.automated_import_should_detect_type = True
        options.static_mesh_import_data = static_mesh_import_data

        task = unreal.AssetImportTask()
        task.automated = True
        task.destination_name = Path(source_path).stem
        task.destination_path = ue_destination
        task.filename = source_path
        task.replace_existing = True
        task.save = False
        task.options = options

        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

        return True