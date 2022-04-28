import os
import calendar


# 月度日报模拟测试， 整和所有日报写入一个月度报告汇总中，如果没有当日的跳过
# 跳过所有非工作日 chinescalendar库
# 迭代预测，先月度，再搞年度双层目录和年报
# 文档类型变为word类型，文本加入列表格式
# 接收用户自定义路径
# GUI加入，生成exe


def generateMonthFiles(n):
    os.makedirs(str(n) + "月工作报告")
    max_index = calendar.mdays[n]
    for i in range(1, max_index+1):
        day_folder_name = str(i) + "日"
        file_path = str(n) + "月工作报告\\" + day_folder_name
        os.makedirs(file_path, exist_ok=True)
        file_name = day_folder_name + "日报.txt"
        with open(os.path.join(file_path, file_name), "w", encoding='utf-8') as f:
            f.write(str(i) + "日日报")


def calendarAPI():
    print(calendar.mdays)
    print(calendar.isleap(2020))  # 闰年判断


if __name__ == '__main__':
    generateMonthFiles(2)
    # print(sum(range(1, 101, 2)))
