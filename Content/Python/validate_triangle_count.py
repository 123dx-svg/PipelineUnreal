import unreal
from unreal import DataValidationResult
from typing import Tuple
from unreal import Array

TRIS_COUNT_MAX =2500

@unreal.uclass()
class TriangleCountValidator(unreal.EditorValidatorBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @unreal.ufunction(override=True)
    def can_validate_asset(self, asset):
        return isinstance(asset, (unreal.StaticMesh, unreal.SkeletalMesh))

    @unreal.ufunction(override=True)
    def validate_loaded_asset(self, asset: unreal.Object, validation_errors: Array[unreal.Text]):
        #相当于 /Game/StarterContent/Props/SM_Statue
        correct_path = "".join(asset.get_path_name().split('.')[:-1])
        #资产Tag标签值
        tag_values = unreal.EditorAssetLibrary.get_tag_values(correct_path)
        triangles_key = unreal.Name("Triangles")
        if triangles_key not in tag_values:
            self.asset_warning(asset, unreal.Text("Triangle count not specified in tags"))
            return (unreal.DataValidationResult.INVALID, validation_errors)
        
        triangle_count = int(tag_values[unreal.Name('Triangles')])
        if triangle_count > TRIS_COUNT_MAX:
            fails = self.asset_fails(asset, unreal.Text(f"Triangle count exceeds maximum of {TRIS_COUNT_MAX}: {triangle_count}"),validation_errors)
            return (unreal.DataValidationResult.INVALID, fails)
        
        self.asset_passes(asset)
        return (unreal.DataValidationResult.VALID, validation_errors)
    
    pass
    
def register_triangle_count_validator():
    editor_validator_subsystem = unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem)
    triangle_count_validator = TriangleCountValidator()
    editor_validator_subsystem.add_validator(triangle_count_validator)