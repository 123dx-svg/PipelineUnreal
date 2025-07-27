import unreal

# 列出所有注册的菜单 如果在控制台cmd输入ToolMenus.Edit就会直接显示所有的菜单，就不要每次去猜了
def list_menu(num =1000):
    menu_list = set()
    for i in range(num):
        # 该路径获取命令
        # edit_menus = unreal.ToolMenus.get().find_menu("LevelEditor.MainMenu.Edit")
        obj = unreal.find_object(None,"/Engine/Transient.ToolMenus_0:RegisteredMenu_%s" % i)
        if not obj:
            continue
        menu_name = str(obj.menu_name)
        if menu_name !="None":
            menu_list.add(menu_name)
    return list(menu_list)

print(list_menu())