import unreal
from unreal import DataValidationResult

@unreal.uclass()
class SquareTextureValidator(unreal.EditorValidatorBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

    @unreal.ufunction(override=True)
    def can_validate_asset(self, asset):
        return isinstance(asset, unreal.Texture2D)


    @unreal.ufunction(override=True)
    def validate_loaded_asset(self, asset:unreal.Texture2D, validation_errors)-> DataValidationResult:
        if not asset.blueprint_get_size_x() == asset.blueprint_get_size_y():
            #self.asset_fails(asset, unreal.Text("Texture is not square."),validation_errors)
            self.asset_warning(asset, unreal.Text("Texture is not square."))
            return (unreal.DataValidationResult.INVALID,validation_errors)
        return (unreal.DataValidationResult.VALID, validation_errors)


@unreal.uclass()
class PowerOfTwoTextureValidator(unreal.EditorValidatorBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

    @unreal.ufunction(override=True)
    def can_validate_asset(self, asset):
        return isinstance(asset, unreal.Texture2D)


    @unreal.ufunction(override=True)
    def validate_loaded_asset(self, asset:unreal.Texture2D,validation_errors):
        #省略每次的计算，直接使用预定义的有效尺寸
        valid_sizes = (2,4,8,16,32,64,128,256,512,1024,2048,4096,8192)
        if asset.blueprint_get_size_x() not in valid_sizes or asset.blueprint_get_size_y() not in valid_sizes:
            self.asset_warning(asset, unreal.Text(f"Texture size is not one of the valid sizes: {valid_sizes}"))
            return (unreal.DataValidationResult.INVALID,validation_errors)
        return (unreal.DataValidationResult.VALID,validation_errors)
    
    
def register_texture_validator():
    editor_validator_subsystem = unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem)
    square_validator = SquareTextureValidator()
    power_of_two_validator = PowerOfTwoTextureValidator()
    editor_validator_subsystem.add_validator(square_validator)
    editor_validator_subsystem.add_validator(power_of_two_validator)