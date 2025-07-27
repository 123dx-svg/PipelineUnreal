import unreal
from fix_compression import validate_compression_settings

EditorUtilityLibrary = unreal.EditorUtilityLibrary()


@unreal.uclass()
class MyScriptObject(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self,context):
        selected_assets = EditorUtilityLibrary.get_selected_assets()
        total_steps = len(selected_assets)

        with unreal.ScopedSlowTask(total_steps,"修复纹理压缩类型中...") as slow_task:
            slow_task.make_dialog(can_cancel=True)

            for texture in selected_assets:
                if slow_task.should_cancel():
                    break
                validate_compression_settings(texture)
                slow_task.enter_progress_frame(1)

def setup_ui():
    menus = unreal.ToolMenus.get()
    asset_context_menu = menus.find_menu("ContentBrowser.AssetContextMenu.Texture")
    script_object = MyScriptObject()
    script_object.init_entry(
        owner_name=asset_context_menu.menu_name,
        menu=asset_context_menu.menu_name,
        section="GetAssetActions",
        name = "修复纹理压缩类型",
        label="修复纹理压缩类型",
        tool_tip="基于文件后缀进行纹理压缩设置修复"
      
    )
    script_object.register_menu_entry()

    #设置图标 该图标在SlateEditorStyle.cpp下
    tool_menu_entry_script_data = script_object.data
    script_icon = unreal.ScriptSlateIcon(style_set_name="EditorStyle",
                                         style_name="Checker",
                                         small_style_name="Checker")
    tool_menu_entry_script_data.icon = script_icon

    menus.refresh_all_widgets()




        
       