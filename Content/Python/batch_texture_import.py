import unreal
from pathlib import Path
from typing import Set

def batch_import_textures(destination_path: str, source_paths: str) ->Set[unreal.Object]:

    asserts_to_import = Path(source_paths).glob("*.png")
    #转换路径
    asserts_to_import = list(map(lambda path: str(path), asserts_to_import))

    asserts_import_data = unreal.AutomatedAssetImportData()
    asserts_import_data.destination_path = destination_path
    asserts_import_data.filenames = asserts_to_import
    asserts_import_data.replace_existing = True
    imported = set(unreal.AssetToolsHelpers.get_asset_tools().import_assets_automated(asserts_import_data))

    return imported

if __name__ == "__main__":
    imported_textures = batch_import_textures("/Game/Enviro", r"D:\CPPUE4\PipelineUnreal\Tex")
