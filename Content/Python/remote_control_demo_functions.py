import json
import unreal
#需要安装requests 包

# 无参请求
# PUT http://localhost:30010/remote/object/call
# {
# 	"objectPath":"/Engine/PythonTypes.Default__RemoteControlDemo",
# 	"functionName":"ping_unreal"
# }

# 带参请求
# PUT http://localhost:30010/remote/object/call
# {
# 	"objectPath":"/Engine/PythonTypes.Default__RemoteControlDemo",
# 	"functionName":"return_params",
# 	"parameters":{
# 		"integer":12345,
# 		"string":"dingxiao hello"
# 	}
# }


@unreal.uclass()
class RemoteControlDemo(unreal.Object):
    #无参的请求
    @unreal.ufunction(ret=bool,meta=dict(Category = "Tech"))
    def ping_unreal(self):
        return True
    #带参请求
    @unreal.ufunction(ret=str,params=[int,str],meta=dict(Category = "Tech"))
    def return_params(self,integer,string):
        return json.dumps({"integer":integer,"string":string})