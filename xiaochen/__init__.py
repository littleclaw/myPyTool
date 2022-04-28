# from:a  by:b  to:c
import os


# n 表示有几层塔， a 为起始点名，b为中间点名，c为目标点名
def hanno(n, a, b, c):
    if n == 1:
        print(a + "-->" + c)
    else:
        hanno(n - 1, a, c, b)
        print(a + "-->" + c)
        hanno(n - 1, b, a, c)


if __name__ == '__main__':
    # hanno(5, "A", "B", "C")
    for f_name in os.listdir("D:\\WeChat"):
        print(f_name)

