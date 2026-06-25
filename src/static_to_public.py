import os
import shutil


def static_to_public(src: str, target: str) -> None:
    if os.path.exists(target):
        shutil.rmtree(target)
        os.mkdir(target)
        print(f"SUCCESS: deleted contents of {target}")
        copied_file_paths = copy_src(src, target)
        print(copied_file_paths)
        for filepath in copied_file_paths:
            print(filepath.replace(src, target))

    else:
        print(f"INFO: \"{target}\" directory does not exist... Creating directory")
        os.mkdir(target)

def copy_src(src: str, target: str) -> list[str]:
    file_list: list[str] = []
    current_dir: list[str] = os.listdir(src)
    for i in range(len(current_dir)):
        file_key = os.path.join(src, current_dir[i])
        if os.path.isfile(file_key):
            file_list.append(file_key)
            _ = shutil.copy(file_key, target)
            continue
        os.mkdir(file_key.replace(src, target))
        file_list.extend(copy_src(file_key, target))
    return file_list
