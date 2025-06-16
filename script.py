import os


for f in os.listdir("uploads/tiles"):
    path = os.path.join("uploads/tiles", f)
    print(path)
    os.remove(path)