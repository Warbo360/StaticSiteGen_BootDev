import os
import shutil


def static_to_public(src: str, target: str) -> None:
    if os.path.exists(target):
        shutil.rmtree(target)
        os.mkdir(target)
        print(f"\nSUCCESS: deleted contents of \"{target}\"")
        try:
            copy_src(src, target)
            print(f"\nSUCCESS: Files copied from \"{src}\" to \"{target}\"")
        except Exception as e:
            print(f"An error occured {e}")
    else:
        print(f"\nERROR: \"{target}\" directory does not exist... Creating directory")

def copy_src(src: str, target: str) -> None:
    current_dir: list[str] = os.listdir(src)
    for i in range(len(current_dir)):
        if os.path.isfile(src + "/" + current_dir[i]):
            copy = shutil.copy(src + "/" + current_dir[i], target)
            print(f"COPIED: \"{copy}\" into \"{target}\"")
            continue
        os.mkdir(target + "/" + current_dir[i])
        copy_src(src + "/" + current_dir[i], target + "/" + current_dir[i])

