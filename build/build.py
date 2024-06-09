import json
import os

appdata_path = os.getenv('APPDATA')
directory_path = os.path.join(appdata_path, 'AutoCry', 'AutoTangQua')
file_path = os.path.join(directory_path, 'config.txt')
count_path = os.path.join(directory_path, 'count.txt')
with open(file_path, "r") as file:
    data = file.readlines()
    print(data)


def sleep_plus():
    if str(data[3].strip()) == "Fast":
        pass
    elif str(data[3].strip()) == "Medium":
        sleep(1)
    else:
        sleep(2)


switcher = {
    1: [-177, 82],
    2: [-8, 79],
    3: [162, 71],
    4: [-175, 207],
    5: [-16, 211],
    6: [163, 209],
    7: [-177, 342],
    8: [-8, 346],
    9: [155, 358]
}


def select_item(select):
    item = switcher.get(select)
    click(Pattern("1717896267952.png").targetOffset(item[0], item[1]))


def gift(name, count, item):
    for i in range(count):
        select_item(item)
        click(Pattern("1717896267952.png").targetOffset(202, 470))
        sleep_plus()
        type(name)
        type(Key.ENTER)
        sleep_plus()
        click(Pattern("1717896267952.png").targetOffset(-18, 239))

        with open(count_path, "w") as f:
            f.write(str(i + 1))


gift(name=data[2].strip(),
     count=int(data[1].strip()),
     item=int(data[0].strip()))
sleep(1)
