import unreal

EditorAssetLibrary = unreal.EditorAssetLibrary()

#文件后缀类型对应的压缩设置
COMPRESSION_MAPPING = {
    "_N":unreal.TextureCompressionSettings.TC_NORMALMAP,
    "_D":unreal.TextureCompressionSettings.TC_DEFAULT,
    "_E":unreal.TextureCompressionSettings.TC_DEFAULT,
    "_M":unreal.TextureCompressionSettings.TC_DEFAULT,
    "_R":unreal.TextureCompressionSettings.TC_GRAYSCALE
}



#获取列表下的所有纹理资产并设置格式
def validate_compression_settings(directory:str,apply_fix:bool =True):
    asset_path_list = EditorAssetLibrary.list_assets(directory)
    for asset_path in asset_path_list:
        texture = EditorAssetLibrary.load_asset(asset_path)

        if not isinstance(texture,unreal.Texture2D):
            continue
        
        name = str(texture.get_fname())
        name_match = False
        correct_compression = None
        for suffix in COMPRESSION_MAPPING.keys():
            if name.endswith(suffix):
                name_match = True
                correct_compression = COMPRESSION_MAPPING[suffix]
                break
        if not name_match:
            continue

        current_compression = texture.get_editor_property("compression_settings")
        if current_compression != correct_compression:
            print(f"WRONG COMPRESSION SETTINGS :{asset_path} )")
            if apply_fix:
                print(f"{asset_path} was set to {str(correct_compression)}")
                texture.set_editor_property(name="compression_settings",value = correct_compression)

if __name__ == "__main__":
    validate_compression_settings(directory="/Game/StarterContent/Textures/")