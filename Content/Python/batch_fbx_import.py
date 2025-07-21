import unreal

from pathlib import Path
from typing import List


destination_path = "/Game/Enviro"
source_paths = r"D:\\CPPUE4\\PipelineUnreal\\FBX"
#assert_to_import = list(Path(source_paths).rglob("*.fbx")) 递归搜索
assert_to_import = list(Path(source_paths).glob("*.fbx"))

# 合并导入的网格
static_mesh_import_data = unreal.FbxStaticMeshImportData()
static_mesh_import_data.combine_meshes = True
static_mesh_import_data.remove_degenerates = True

# 设置导入选项
options = unreal.FbxImportUI()
options.import_mesh = True
options.import_textures = False
options.import_materials = True
options.automated_import_should_detect_type = True
options.static_mesh_import_data = static_mesh_import_data


tasks:List[unreal.AssetImportTask] = []

for input_file_path in assert_to_import:
    task = unreal.AssetImportTask()
    task.automated = True
    task.destination_path = destination_path
    task.destination_name = input_file_path.stem
    task.filename = str(input_file_path)
    task.replace_existing = True
    task.save = True
    task.options = options

    tasks.append(task)

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

for task in tasks:
    for path in task.imported_object_paths:
        unreal.log(f"Imported: {path}")