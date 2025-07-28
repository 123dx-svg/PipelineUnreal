#该代码给Blender脚本
import bpy

API_URL = "http://localhost:30010/remote/object/call"

class TechArtCorner_OT(bpy.types.Operator):
    bl_idname = "tutorial.export"
    bl_label = "Example Export"

    def send_to_unreal(self,filepath):
        import requests
        payload = {
            	"objectPath":"/Engine/PythonTypes.Default__RemoteImporter",
	            "functionName":"import_fbx",
                "parameters":{
                    "source_path":filepath,
                    "ue_destination":"/Game/Envior"
                }
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "insomnia/11.3.0"
        }
        try:
            response = requests.request("PUT",API_URL,json=payload,headers=headers)
            response.raise_for_status()
        except Exception as e:
            print(f"Exception happend Lets Handle it {str(e)}")
    
    def excute(self,context):
        filepath = r"D:\CPPUE4\PipelineUnreal\FBX\Cone2.fbx"
        bpy.ops.export_scene.fbx(filepath=filepath,mesh_smooth_type = "FACE",object_types = {'MESH'},use_custom_props = True)
        self.send_to_unreal(filepath)
        return {'FINISHED'}

class PythonAutomationCourse_pannel(bpy.types.Panel):
    bl_idname = "EXAMPLE_PY"
    bl_label = "EXAMPLE EXPORT"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Python Automation Course"
    def draw(self,context):
        layout = self.layout
        layout.operator(TechArtCorner_OT.bl_idname,text="Example Export")

def register():
    bpy.utils.register_class(TechArtCorner_OT)
    bpy.utils.register_class(PythonAutomationCourse_pannel)

def unregister():
    bpy.utils.unregister_class(TechArtCorner_OT)
    bpy.utils.unregister_class(PythonAutomationCourse_pannel)

if __name__ == "__main__":
    register()