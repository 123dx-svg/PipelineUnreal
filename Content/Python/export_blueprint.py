import os
import zipfile
import unreal
import tkinter as tk
from tkinter import filedialog

#打开文件夹
def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory(title="请选择导出目录")

    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    if not selected_assets:
        raise Exception("请先选中一个资产")

    # 拼接资产名称
    asset_name = selected_assets[0].get_name()
    return file_path  # 修改返回路径


#合并蓝图并导出
def merge_blueprint_to_local():
    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    blueprint_asset = selected_assets[0]
    asset_name = blueprint_asset.get_name()
    file_path = open_file_dialog()

    #获取蓝图内的所有Export标记组件
    ExportBPBlueprintFunctionLibrary = unreal.ExportBPBlueprintFunctionLibrary
    components =  ExportBPBlueprintFunctionLibrary.get_components_from_blueprint_asset(blueprint_asset)
    if components:
        mesh_path = "/Game/ExportBPMesh/"+blueprint_asset.get_name()
        #合并模型
        static_mesh_assets = ExportBPBlueprintFunctionLibrary.merge_actor_to_static_mesh(mesh_path,components)
        #导出模型
        if static_mesh_assets:
            task = unreal.AssetExportTask()
            task.object = static_mesh_assets[0]
            #创建一个以该文件命名的文件夹
            task.filename = f"{file_path}/{asset_name}/{asset_name}.glb"
            task.automated = True
            task.replace_identical = True
            task.exporter = unreal.GLTFStaticMeshExporter()
            task.options = unreal.GLTFExportOptions()
            res = unreal.Exporter.run_asset_export_task(task)
            if not res:
                print("导出失败")
            else:
                #删除临时模型
                EditorActorSubsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
                actors = EditorActorSubsystem.get_all_level_actors()
                for actor in actors:
                    if actor.actor_has_tag(unreal.Name("PythonTemp")):
                        EditorActorSubsystem.destroy_actor(actor)
                
                # 合并压缩包
                    zip_path = os.path.join(file_path, asset_name)
                    zip_name = os.path.join(zip_path, f"{asset_name}.zip")
                    
                    # 确保目录存在
                    os.makedirs(zip_path, exist_ok=True)
                    
                    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        glb_path = task.filename
                        #经过os.path.basename处理后，压缩包内的文件名为资产名称
                        zipf.write(glb_path, os.path.basename(glb_path))
                        print(f"成功创建压缩包：{os.path.basename(glb_path)}")



#执行脚本
@unreal.uclass()
class ExportBlueprint(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self, context):
        merge_blueprint_to_local()

#初始化UI
def export_blueprint_ui():
    tool_menus = unreal.ToolMenus.get()
    asset_context_menu = tool_menus.find_menu("ContentBrowser.AssetContextMenu.Blueprint")
    if not asset_context_menu:
        unreal.log_error("未找到蓝图上下文菜单")
        return
    
    export_blueprint = ExportBlueprint()

    export_blueprint.init_entry(
        owner_name=asset_context_menu.menu_name,
        menu= asset_context_menu.menu_name,
        section="",
        name= "导出蓝图为GLTF",
        label="导出蓝图导出为GLTF",
        tool_tip="导出选中的蓝图中Tag=Export的组件为GLTF格式"
        
    )

    export_blueprint.register_menu_entry()
    script_icon = unreal.ScriptSlateIcon(
        style_set_name="EditorStyle",
        style_name="FontEditor.ExportAllPages",
        small_style_name="FontEditor.ExportAllPages"
    )

    export_blueprint.data.icon = script_icon

    tool_menus.refresh_all_widgets()




if __name__ == "__main__":
    export_blueprint_ui()