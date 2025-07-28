from dataclasses import dataclass
from typing import Union
import unreal
#用于单例控制
SLOW_TASK: Union[None,unreal.ScopedSlowTask] = None

@dataclass
class ProgressBarState:
    steps:int = 0
    current_step:int =0

PROGRESS_BAR_STATE = ProgressBarState()

@unreal.uclass()
class MyProgressBar(unreal.Object):
    @unreal.ufunction(ret=bool,params=[int,str],meta=dict(Category = "Tech"))
    def progress_bar_start(self,steps,label):
        global SLOW_TASK
        if SLOW_TASK:  # 检查是否已有进行中的进度条
            return False
        
        # 创建新的进度条任务
        SLOW_TASK = unreal.ScopedSlowTask(steps,label)
        global PROGRESS_BAR_STATE
        PROGRESS_BAR_STATE.steps = steps  # 记录总步骤数
        
        # 启动并显示进度条对话框 
        SLOW_TASK.__enter__()
        SLOW_TASK.make_dialog()
        
        return True  # 表示成功创建进度条

    @unreal.ufunction(ret=bool,meta=dict(Category = "Tech"))
    def progress_bar_increment(self):
        global SLOW_TASK
        if not SLOW_TASK:
            return False
        
        global PROGRESS_BAR_STATE
        if PROGRESS_BAR_STATE.current_step<= PROGRESS_BAR_STATE.steps:
            PROGRESS_BAR_STATE.current_step += 1
            SLOW_TASK.enter_progress_frame(1)
            return True
        
        return False
    
    @unreal.ufunction(ret=bool,meta=dict(Category = "Tech"))
    def progress_bar_finish(self):
            global SLOW_TASK
            if not SLOW_TASK:
                return False
            
            SLOW_TASK.__exit__()
            SLOW_TASK = None

            global PROGRESS_BAR_STATE
            PROGRESS_BAR_STATE = ProgressBarState()
        



