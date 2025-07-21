import unreal
from unreal import DataValidationResult,Object

@unreal.uclass()
class AssetPrefixValidator(unreal.EditorValidatorBase):
    def __init__(self,*arg,**kwargs):
        super().__init__(*arg, **kwargs)

    @unreal.ufunction(override=True)
    def can_validate_asset(self, asset):
         return isinstance(asset,(unreal.Texture2D, unreal.Blueprint,unreal.Material,unreal.MaterialInstanceConstant))

    @unreal.ufunction(override=True)
    def validate_loaded_asset(self, asset:Object,validation_errors) -> DataValidationResult:

        name = str(asset.get_fname())
        message = "Name should start with"

        if asset.__class__ == unreal.Texture2D:
            if name.startswith("T_"):
                return (unreal.DataValidationResult.VALID,validation_errors)
            message += " T_"
        elif asset.__class__ == unreal.Blueprint:
            if name.startswith("BP_"):
                return (unreal.DataValidationResult.VALID,validation_errors)
            message += " BP_"          
        elif asset.__class__ == unreal.Material:
            if name.startswith("M_"):
                return (unreal.DataValidationResult.VALID,validation_errors)
            message += " M_"
        elif asset.__class__ == unreal.MaterialInstanceConstant:
            if name.startswith("MI_"):
                return (unreal.DataValidationResult.VALID,validation_errors)
            message += " MI_"


        self.asset_warning(asset,unreal.Text(message)) 
        return (unreal.DataValidationResult.INVALID, validation_errors)

def register_asset_prefix_validator():
    editor_validator_subsystem = unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem)
    validator = AssetPrefixValidator()
    editor_validator_subsystem.add_validator(validator)

