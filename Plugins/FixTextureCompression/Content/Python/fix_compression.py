import unreal
from typing import Union,List

EditorAssetLibrary = unreal.EditorAssetLibrary()
EditorUtilityLibrary = unreal.EditorUtilityLibrary()

#文件后缀类型对应的压缩设置
COMPRESSION_MAPPING = {
    "_N":unreal.TextureCompressionSettings.TC_NORMALMAP,
    "_D":unreal.TextureCompressionSettings.TC_DEFAULT,
    "_E":unreal.TextureCompressionSettings.TC_DEFAULT,
    "_M":unreal.TextureCompressionSettings.TC_DEFAULT,
    "_R":unreal.TextureCompressionSettings.TC_GRAYSCALE
}

#获取列表下的所有纹理资产并设置格式
def validate_compression_settings(assets:Union[List[unreal.Texture2D],unreal.Texture2D],apply_fix:bool =True):
   if not isinstance(assets,list):
    assets = [assets]
   
    for texture in assets:
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
            print(f"WRONG COMPRESSION SETTINGS :{texture.get_fname()} )")
            if apply_fix:
                print(f"{texture.get_fname()} was set to {str(correct_compression)}")
                texture.set_editor_property(name="compression_settings",value = correct_compression)
