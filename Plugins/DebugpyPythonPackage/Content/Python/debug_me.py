import unreal

EditorUtilityLibrary = unreal.EditorUtilityLibrary()
def new_func(EditorUtilityLibrary):
    assets = EditorUtilityLibrary.get_selected_assets()
    return assets

assets = new_func(EditorUtilityLibrary)
for asset in assets:
    print(f"Asset Name: {asset.get_name()} | Asset Path: {asset.get_path_name()}")



 

def inner():
    print("Inner function called")
    count = 1
    for i in range(5):
        count = count *i
    return count
def outer():
    print("Outer function called")
    result = inner()
    print(f"Result from inner function: {result}")

print("Starting the script...")
outer()