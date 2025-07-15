import os.path
import unreal

import uuid

def say_hi():
    unreal.log('Hi Engine hello scrip')

print('hi i am imported')

random_name = str(uuid.uuid4())
path = os.path.join(r"D:\\CPPUE4\\PipelineUnreal\\Content\\Python",random_name)

with open(path,"w") as f:
    pass

print(f"Created {random_name}")

