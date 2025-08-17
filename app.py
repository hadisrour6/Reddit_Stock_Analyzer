import main
from main import *
from change_algorithm import *
from big_movement import *
from git_commit import *

import time
if __name__ == '__main__':
    # exec()
    # time.sleep(6)
    # main()
    x = find_big_movements(threshold_1d=5.0, threshold_7d=5.0)

    if x == 1:
        git_push("big_movement.json", "Auto-update big_movement.json")

