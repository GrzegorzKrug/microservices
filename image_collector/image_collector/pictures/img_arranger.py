import os
import sys
from threading import Thread
from glob import glob


def move_pics(file_list, directory):
    for file in file_list:
        name = os.path.basename(file)
        destination = os.path.join(directory, name)
        file = os.path.abspath(file)
        os.rename(file, destination)
    print(f"Moved {len(file_list)} files to {directory}")


def remove_duplicates():
    for cur_dir in os.listdir():
        good_files = set()
        bad_files = []

        if cur_dir not in ['big', 'medium', 'small', 'tiny']:
            continue

        directories = []

        for num_dir in os.listdir(cur_dir):
            path = os.path.join(cur_dir, num_dir)
            if os.path.isdir(path):
                directories.append(num_dir)

        directories.sort()

        for num_dir in directories:
            path = os.path.join(cur_dir, num_dir)
            for file in os.listdir(path):
                if file in good_files:
                    file_path = os.path.join(path, file)
                    bad_files.append(file_path)
                else:
                    good_files.add(file)

        for file in os.listdir(cur_dir):
            if file in good_files:
                file_path = os.path.join(cur_dir, file)
                bad_files.append(file_path)
            else:
                good_files.add(file)

        for file in bad_files:
            print(f"Removing {file}")
            os.remove(file)


def move_new_files():
    CAP = 100
    for cur_dir in os.listdir():
        if cur_dir not in ['big', 'medium', 'small', 'tiny']:
            continue

        pics = glob(os.path.join(cur_dir, "*.jpg"))
        print(f"{len(pics)} pictures in main {cur_dir}")

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
                amount = len(files)
                if amount < CAP:
                    chunk = chunk - amount
                elif amount > CAP:
                    too_much = amount - CAP
                    print(f"Too much files in {dest_path} by {too_much}")
                    files = files[:too_much]
                    files = [os.path.abspath(os.path.join(dest_path, file)) for file in files]
                    pics = files[:too_much] + pics
                    continue
                else:
                    continue
            finally:
                # print(f"Num: {num:>3}, images: {len(pics)}")
                num += 1

            if chunk > 0:
                fil_list = pics[:chunk]
                th = Thread(target=move_pics, args=(fil_list, dest_path))
                th.start()
                try:
                    pics = pics[chunk:]
                except IndexError as err:
                    print(f"{err}")
                    print(pics)
                    pics = []


if __name__ == "__main__":
    remove_duplicates()
    move_new_files()
