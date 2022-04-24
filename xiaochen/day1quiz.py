# BMI低于18.5：过轻
# 18.5-25：正常
# 25-28：过重
# 28-32：肥胖
# 高于32：严重肥胖
weight = 76
height = 1.73
bmi = weight / (height ** 2)
print(bmi)

height = 1.6
expected_weight = 25 * height**2
print(expected_weight)

if __name__ == '__main__':
    chen = {"name": "小辰", "gender": "女"}
    print(chen.get("name"))

