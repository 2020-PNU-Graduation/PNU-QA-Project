import os
from bs4 import BeautifulSoup


def print_files_in_dir(root_dir, prefix):
    files = os.listdir(root_dir)
    for file in files:
        if str(file) == '.DS_Store': continue
        path = os.path.join(root_dir, file)
        if os.path.isdir(path):
            print_files_in_dir(path, prefix + "")
        else:
            temp_file = open(str(path), 'r', encoding='utf-8')

            soup = BeautifulSoup(temp_file, 'html.parser')
            res = soup.select_one("table")

            if str(res) != 'None':
                print(file)
                new_file = open(str(file) + '_table.txt', 'w', encoding='utf-8')
                new_file.write(str(res))
                new_file.close()

            temp_file.close()


if __name__ == "__main__":
    root_dir = "./ko/articles"
    print_files_in_dir(root_dir, "")