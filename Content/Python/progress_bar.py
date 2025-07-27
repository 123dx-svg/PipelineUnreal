import unreal 
import time

def main():
    total_steps = 100
    dialog_name = "Slow task in progress"
    with unreal.ScopedSlowTask(total_steps,dialog_name) as slow_task:
        slow_task.make_dialog(can_cancel=True)

        for i in range(total_steps):
            if slow_task.should_cancel():
                break
            time.sleep(0.1)
            slow_task.enter_progress_frame(1)


if __name__ == "__main__":
    main()