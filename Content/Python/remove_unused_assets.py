import unreal

EditorUtilityLibrary = unreal.EditorUtilityLibrary()
EditorAssetLibrary = unreal.EditorAssetLibrary()

def get_selected_asset_paths():
    selected_assets = EditorUtilityLibrary.get_selected_assets()  
    for asset in selected_assets:
        yield EditorAssetLibrary.get_path_name_for_loaded_asset(asset)
    

def remove_unused_assets(asset_path:str):
    references = EditorAssetLibrary.find_package_referencers_for_asset(asset_path)

    if len(references) == 0:
        if EditorAssetLibrary.delete_asset(asset_path):
            unreal.log(f"Removed unused asset: {asset_path}")
        else:
            unreal.log_warning(f"Failed to remove asset: {asset_path}")

# 以下是选中文件夹对文件夹进行递归搜索
# AssetRegistry = unreal.AssetRegistryHelpers.get_asset_registry()
# asset_list = AssetRegistry.get_assets_by_path("/Game/StarterContent", recursive=True)


if __name__ == "__main__":
    for path in get_selected_asset_paths():
        remove_unused_assets(path)