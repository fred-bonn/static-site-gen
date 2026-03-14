import os, shutil

def cp_replace_dir(src, dst):
    # Ensure both source and destination directories exist
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory '{src}' does not exist.")
    if not os.path.exists(dst):
        raise FileNotFoundError(f"Destination directory '{dst}' does not exist.")
    
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    # Remove the destination directory and its contents
    shutil.rmtree(dst)
    # Copy the source directory to the destination
    shutil.copytree(src, dst)