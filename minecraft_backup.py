# Backup Minecraft saves
import time
import os
import shutil as sh

saves_folder = "C:\\Users\\Ant\\AppData\\Roaming\\.minecraft\\saves"

# def compare_files(file_old, file_new):


def copy_folder(src, dst):
    try:
        sh.copytree(src, dst)
    except sh.Error as err:
        # Directories are the same
        print("Directory was not copied. Error: %s" % err)
    except OSError as err:
        # Any error saying that the directory doesn't exist
        print("Directory was not copied. Error: %s" % err)


def mode_active():
    saves = os.listdir(saves_folder)

    print("Type number of folder, that you want to backup:")
    c = 0
    for i in saves:
        print(c + 1, i)
        c += 1


def mode_passive():
    print("Backup the most important save.")
    copy_folder(saves_folder + "Main World", "")

print("To start active mode press any key.")
for i in reversed(range(1, 6)):
    print(i)
    # if () any key pressed
    #   mode_active()
    time.sleep(1)
os.system("cls")

mode_passive()
