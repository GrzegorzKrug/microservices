import os
import sys
from threading import Thread
from glob import glob


def move_pics(file_list, directory):
    for file in file_list:
        name = os.path.basename(file)
        destination = os.path.join(directory, name)
        os.rename(file, destination)
    print(f"Moved {len(file_list)} files to {directory}")


CAP = 500
for cur_dir in os.listdir():
    if cur_dir not in ['big', 'medium', 'small', 'tiny']:
        continue

    pics = glob(os.path.join(cur_dir, "*.jpg"))

    print(f"{len(pics)} pictures to move in {cur_dir}")

    num = 0
    while len(pics) > 0:
        dest_path = os.path.abspath(os.path.join(cur_dir, f"{num:>03}"))
        chunk = CAP

        try:
            os.mkdir(dest_path)
            print(f"Created {cur_dir} {num:>03}")

        except FileExistsError as fee:
            # print(f"This dir exists: {num}")
            files = os.listdir(dest_path)
            files = len(files)
            if files < CAP:
                chunk = chunk - files
            else:
                continue
        finally:
            num += 1

        if chunk > 0:            
            fil_list = pics[:chunk]
            th = Thread(target=move_pics, args=(fil_list, dest_path))
            th.start()
            try:
                pics = pics[chunk:]
            except IndexError:
                print(pics)
                pics = []

        # pics = glob(os.path.join(cur_dir, "*.jpg"))
