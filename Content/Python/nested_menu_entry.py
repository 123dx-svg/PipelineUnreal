import unreal


@unreal.uclass()
class MyCustomScriptObject(unreal.ToolMenuEntryScript):
     @unreal.ufunction(override = True)
     def execute(self, context):
          print("Script Excuted")

@unreal.uclass()
class AnotherCustomScriptObject(unreal.ToolMenuEntryScript):
     @unreal.ufunction(override = True)
     def execute(self, context):
          print("Another Custom Script Excuted")

def main():
     menus = unreal.ToolMenus.get()
     asset_context_menu = menus.find_menu("ContentBrowser.AssetContextMenu.StaticMesh")
     custom_menu = asset_context_menu.add_sub_menu("Custom Menu","PyAutomation","Label","We add this sub menu")
     #添加分隔符
     separator_entry = unreal.ToolMenuEntry(name=unreal.Name("Separator Entry"),type=unreal.MultiBlockType.SEPARATOR)
     custom_menu.add_menu_entry("",separator_entry) 

     #菜单入口
     script_obj = MyCustomScriptObject()
     script_obj.init_entry(
        owner_name=custom_menu.menu_name,
        menu=custom_menu.menu_name,
        section="",
        name="UE5 PyAutomation",
        label="UE5 PyAutomation",
        tool_tip="Custom Script Entry"
     )
     script_obj.register_menu_entry()

    #添加图标 具体Style直接到UMGStyle.cpp文件下找，如果需要自定义图标就得CPP改了 此处用了个调色盘图标
     tool_menu_entry_script_data = script_obj.data
     script_icon = unreal.ScriptSlateIcon(style_set_name="UMGStyle",
                                          style_name="Palette.Icon",
                                          small_style_name="Palette.Icon.Small")
     tool_menu_entry_script_data.icon = script_icon

     #另一个按钮绑定 此时不用再注册了，unreal.ToolMenuEntry会自动执行一遍注册
     script_object1=AnotherCustomScriptObject()
     script_object1.init_entry(
        owner_name=custom_menu.menu_name,
        menu=custom_menu.menu_name,
        section="",
        name="Py",
        label="Py",
        tool_tip="Entry"

     )
     another_menu_entry = unreal.ToolMenuEntry(
          name=unreal.Name("Anthor Menu Entry"),
          type=unreal.MultiBlockType.MENU_ENTRY,
          script_object=script_object1
          
     )
     another_menu_entry.set_label("Test_Label")
     custom_menu.add_menu_entry("",another_menu_entry)

     menus.refresh_all_widgets()

if __name__ == "__main__":
     main()
