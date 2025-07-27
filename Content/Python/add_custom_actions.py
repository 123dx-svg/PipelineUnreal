import unreal


def add_title_bar_button():
     menus = unreal.ToolMenus.get()
     #添加到顶部
     main_menu = menus.find_menu("LevelEditor.MainMenu")
     #添加自定义菜单名字叫Menu Label
     custom_menu = main_menu.add_sub_menu("Custom Menu","PyAutomation","Menu Name","Menu Label")
     #刷新菜单
     menus.refresh_all_widgets()

@unreal.uclass()
class MyScriptObject(unreal.ToolMenuEntryScript):
     @unreal.ufunction(override = True)
     def execute(self, context):
          print("Script Excuted")

          
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

#按钮添加到右键静态网格体下
def add_button_to_staticmesh():
     menus = unreal.ToolMenus.get()
     asset_context_menu = menus.find_menu("ContentBrowser.AssetContextMenu.StaticMesh")
     script_obj2 = MyScriptObject()
     script_obj2.init_entry(
        owner_name=asset_context_menu.menu_name,
        menu=asset_context_menu.menu_name,
        section="GetAssetActions",
        name="UE5 PyAutomation2",
        label="UE5 PyAutomation2",
        tool_tip="Custom Script Entry2"
     )
     script_obj2.register_menu_entry()