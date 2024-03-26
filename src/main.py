from genericpath import isdir, isfile
from logging import root
import os
import shutil

from templating import generate_page, generate_pages_recursive


def copy_dir_contents(root_path, source_dir, target_dir):
    print(f"Copying data from {source_dir} to {target_dir}")
    dir_contents = os.listdir(root_path + source_dir)

    for f in dir_contents:
        if os.path.isfile(root_path + source_dir + "/" + f):
            if not os.path.exists(root_path + target_dir + "/" + f):
                shutil.copy(
                    root_path + source_dir + "/" + f, root_path + target_dir + "/" + f
                )
        elif os.path.isdir(root_path + source_dir + "/" + f):
            if not os.path.exists(root_path + target_dir + "/" + f):
                os.mkdir(root_path + target_dir + "/" + f)
                copy_dir_contents(root_path, source_dir + "/" + f, target_dir + "/" + f)


def _base_dir_setup(root_path):
    if not os.path.exists("static"):
        os.mkdir(root_path + "/static")

    if os.path.exists(root_path + "/public"):
        shutil.rmtree(root_path + "/public")

    os.mkdir(root_path + "/public")


def main():
    pth = os.getcwd()
    _base_dir_setup(pth)
    copy_dir_contents(pth, "/static", "/public")
    from_path, template_path, dest_path = (
        pth + "/content/",
        pth + "/template.html",
        pth + "/public/",
    )
    generate_pages_recursive(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
