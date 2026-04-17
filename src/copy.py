import os, shutil

def get_public_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    public_dir = os.path.join(current_dir, "..", "public")
    return os.path.abspath(public_dir)

def del_dir(path):
    if os.path.exists:
        shutil.rmtree(path)
        print(f"Deleting all of {os.path.basename(path)} directory.")
    else:
        print(f"No dir found at {path}")

def copy_recursive(src, dst):
    if not os.path.exists(src):
        raise Exception(f"Filepath not found: {src}")
    if not os.path.exists(dst):
        os.mkdir(dst)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            os.mkdir(dst_path)
            copy_recursive(src_path, dst_path)

def copy(path):
    public_dir = get_public_dir()
    if os.path.basename(public_dir) != "public":
        raise Exception("Issue with locating public directory")
    del_dir(public_dir)
    print(f"{os.path.basename(public_dir)} directory has been deleted. Recreating directory.")
    os.mkdir(public_dir)
    print(f"{os.path.basename(public_dir)} directory has been recreated. Copying files from {os.path.basename(path)} directory.")
    copy_recursive(path, public_dir)
    print(f"All files copied from {os.path.basename(path)} directory.")
