import os
# 月度日报模拟测试， 整和所有日报写入一个月度报告汇总中，
# 迭代预测，先月度，再搞年度双层目录和年报


def generateDirWithFiles():
    os.makedirs("5月工作报告")
    for i in range(0, 31):
        day_folder_name = str(i)+"日"
        os.makedirs("5月工作报告\\"+day_folder_name, exist_ok=True)
        file_name = day_folder_name+"日报.txt"
        open(os.path.join("testFiles\\"+str(i), file_name), "w")


if __name__ == '__main__':
    generateDirWithFiles()
