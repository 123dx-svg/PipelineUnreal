from post_import_callbacks import register_import_callback
from validate_asset_prefix import register_asset_prefix_validator
from add_custom_actions import add_title_bar_button,add_button_to_EditMain,add_button_to_staticmesh


print("===EXECUTING Content/Python init unreal")
#初始文件记录导入规则 暂时回合其他导入规则冲突，他会根据元数据导入模型时自动匹配文件夹自动执行无需进行项目设置
#register_import_callback()
#验证前缀
#register_asset_prefix_validator()

# 注册界面按键
 #标题栏 每次重启会被刷掉
add_title_bar_button()
 #在EditMain中再添加一个可以执行脚本的按钮
add_button_to_EditMain()
 #在静态网格体下添加按钮
add_button_to_staticmesh()