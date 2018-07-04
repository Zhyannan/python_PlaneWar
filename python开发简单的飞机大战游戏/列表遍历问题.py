list1 = [10, 20, 30, 40, 50]
# 不能对同一个列表边遍历边增删元素
for element in list1:
    print(element)  # 没有遍历到40
    if element == 30 or element == 40:
        list1.remove(element)

# 解决办法:
# 1. 先遍历,然后将目标元素记录下来(没有增删,就可以让每个元素都参与遍历, 原列表索引没有变化)
# temp_list = []  # 定义临时列表, 记录目标元素
#
# for element in list1:
#     print(element)
#     if element == 30 or element == 40:
#         temp_list.append(element)
#
# # 2. 等遍历完再对目标元素进行处理
# for target_element in temp_list:
#     list1.remove(target_element)
#
print(list1)