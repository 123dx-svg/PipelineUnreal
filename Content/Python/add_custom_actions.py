import unreal


@unreal.uclass()
class MyScriptObject(unreal.ToolMenuEntryScript):
     @unreal.ufunction(override = True)
     def execute(self, context):
          print("Script Excuted")

def add_title_bar_button():
     menus = unreal.ToolMenus.get()
     #添加到顶部
     main_menu = menus.find_menu("LevelEditor.MainMenu")
     #添加自定义菜单名字叫Menu Label
     custom_menu = main_menu.add_sub_menu("Custom Menu","PyAutomation","Menu Name","Menu Label")
     #刷新菜单
     menus.refresh_all_widgets()


#按钮添加到EditMain下
def add_button_to_EditMain():
    menus = unreal.ToolMenus.get()
    edit_menu =menus.find_menu("LevelEditor.MainMenu.Edit")
    script_obj = MyScriptObject()
    script_obj.init_entry(
        owner_name=edit_menu.menu_name,
        menu=edit_menu.menu_name,
        section="EditMain",
        name="UE5 PyAutomation",
        label="UE5 PyAutomation",
        tool_tip="Custom Script Entry"

    )
    #添加到section中去
    script_obj.register_menu_entry()

    menus.refresh_all_widgets()



#按钮添加到右键静态网格体下
def add_button_to_staticmesh():
     menus = unreal.ToolMenus.get()
     asset_context_menu = menus.find_menu("ContentBrowser.AssetContextMenu.StaticMesh")
     script_obj = MyScriptObject()
     script_obj.init_entry(
        owner_name=asset_context_menu.menu_name,
        menu=asset_context_menu.menu_name,
        section="GetAssetActions",
        name="UE5 PyAutomation2",
        label="UE5 PyAutomation2",
        tool_tip="Custom Script Entry2"
     )
     script_obj.register_menu_entry()

    #添加图标 具体Style直接到UMGStyle.cpp文件下找，如果需要自定义图标就得CPP改了 此处用了个调色盘图标
     tool_menu_entry_script_data = script_obj.data
     script_icon = unreal.ScriptSlateIcon(style_set_name="UMGStyle",
                                          style_name="Palette.Icon",
                                          small_style_name="Palette.Icon.Small")
     tool_menu_entry_script_data.icon = script_icon


     #属性UI 如果初始化执行可能不需要刷新
     menus.refresh_all_widgets()