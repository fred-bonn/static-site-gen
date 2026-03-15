import os, shutil

def static_copy(src, dst):
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory '{src}' does not exist.")
    if os.path.exists(dst):
        shutil.rmtree(dst)

    recursive_copy(src, dst)

def recursive_copy(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
    
    for file in os.listdir(src):
        src_file = os.path.join(src, file)
        dest_file = os.path.join(dest, file)

        print(f"Copying '{src_file}' to '{dest_file}'")

        if os.path.isdir(src_file):
            recursive_copy(src_file, dest_file)
        else:
            shutil.copy(src_file, dest_file)