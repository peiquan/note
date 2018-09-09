# -*- coding: utf-8 -*-

# 冒泡排序


def bubbleSort(array):
    count = len(array)
    for i in range(0, count):
        for j in range(0, count - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array

array = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
print('bubbleSort:', bubbleSort(array))

# 选择排序


def selectSort(array):
    count = len(array)
    for i in range(0, count):
        min_index = i
        for j in range(i + 1, count):
            if array[j] < array[min_index]:
                min_index = j
        if min_index != i:
            array[min_index], array[i] = array[i], array[min_index]
    return array

array = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
print('selectSort:', selectSort(array))

'''
插入排序
'''


def insertSort(array):
    count = len(array)
    for i in range(1, count):
        temp = array[i]
        j = i - 1
        while j >= 0 and array[j] > temp:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = temp
    return array

array = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
print('insertSort:', insertSort(array))


'''
归并排序
'''


def merge(leftArray, rightArray):
    i, j = 0, 0
    result = []
    while i < len(leftArray) and j < len(rightArray):
        if leftArray[i] < rightArray[j]:
            result.append(leftArray[i])
            i += 1
        else:
            result.append(rightArray[j])
            j += 1
    result += leftArray[i:]
    result += rightArray[j:]
    return result


def mergeSort(array):
    if len(array) <= 1:
        return array
    num = int(len(array) / 2)
    left = mergeSort(array[:num])
    right = mergeSort(array[num:])
    return merge(left, right)

array = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
print('mergeSort:', mergeSort(array))


'''
快速排序
'''


def quickSort(array):
    if len(array) < 2:
        return array
    pivot = array[0]
    less = [i for i in array[1:] if i < pivot]
    greater = [i for i in array[1:] if i >= pivot]
    return quickSort(less) + [pivot] + quickSort(greater)

array = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
print('quickSort:', quickSort(array))
