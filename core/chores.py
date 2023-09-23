"""
Things like fighting with windows backslash \\ are here
"""
import os
import shutil

def win_split(paths):
    """
    Example:
    ```
    raw = r'''
        paste any windows paths
    '''
    for maker in win_split(raw):
        print(maker)
    ```
    """
    outputs = []
    for line in paths.strip().split("\n"):
        line = line.strip()
        if not line.startswith("C"):
            raise ValueError("Windows file assumed under C drive")
        parts = line.split("\\")[1:]
        env_maker = f"{repr(parts)}".replace("[", "").replace("]", "")
        env_maker = f"BaseEnv({env_maker})"
        outputs.append(env_maker)
    return outputs

def collect_files(root):
    os.makedirs(root, exist_ok=True)
    result = []
    # 支持的文字和圖片檔案副檔名
    text_extensions = ['.txt', '.md', '.csv']
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            extension = os.path.splitext(filename)[1].lower()

            if extension in text_extensions or extension in image_extensions:
                result.append(filepath)

    return result


def flatten_files(root, file_list, tag=""):
    """
    Example:
    root = <PATH>
    collected_files = collect_files(root)
    flatten_files(root, collected_files)
    """
    counts = 0

    for file_path in file_list:
        base_name, ext = os.path.splitext(os.path.basename(file_path))
        new_name = f"{tag}{base_name}{ext}"
        counter = 0

        # check dup
        while os.path.exists(os.path.join(root, new_name)):
            counter += 1
            new_name = f"{tag}{base_name}_{counter}{ext}"
        shutil.move(file_path, os.path.join(root, new_name))
        counts += 1

    return counts
