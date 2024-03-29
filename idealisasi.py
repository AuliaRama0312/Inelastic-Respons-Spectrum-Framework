import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# area_Epp, input point 1 2 3
# point 1 = [0, 0] (start point)
# point 2 = yield point
# point 3 = end point 
def area_3p(point1, point2, point3):
    x = 0
    y = 1
    area1 = point2[x]*point2[y]/2
    area2 = point2[y]*(point3[x]-point2[x])
    area3 = (point3[y]-point2[y])*(point3[x]-point2[x])/2
    return (area1+area2+area3)  

# area_Po, input data_loc, id_max
# data_loc = group of point data base on pushover capacity
# id_max = max point on y axis index
def area_Po(data_loc,id_max):
    x = 0
    y = 1
    area = 0
    for i in range(1, id_max+1):
        triangle = (data_loc.iloc[i, x]-data_loc.iloc[i-1, x])*(data_loc.iloc[i, y]-data_loc.iloc[i-1, y])/2
        square = (data_loc.iloc[i, x]-data_loc.iloc[i-1, x])*(data_loc.iloc[i-1, y])
        area = area + (triangle + square)  
    
    return area

# input  x to find y value base on data
def get_point2(data,x):
    if (data.iloc[:, 0] == x).any():
        index = (data.iloc[:, 0] == x).idxmax()
        point2 = [x, data.iloc[index, 1]]
        return point2
    else:
        index = (data.iloc[:, 0] > x).idxmax()-1
        x1 = data.iloc[index, 0]
        x2 = data.iloc[index+1, 0]
        y1 = data.iloc[index, 1]
        y2 = data.iloc[index+1, 1]
        y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
        point2 = [x, y]
        return point2

# Idealisasi metode EPP
def EPP(data, test_converge):
    id_max = data.iloc[:, 1].idxmax()
    max = data.iloc[id_max] 
    max = [max[0],max[1]]

    Po_area = area_Po(data, id_max)
    x = 0
    area = 0

    while (abs(Po_area-area)/Po_area) >= test_converge:
        x = x + 0.00001
        point1 = [0, 0]
        point2 = [x, max[1]]
        point3 = max
        area = area_3p(point1, point2, point3)
    
    return(point1, point2, point3)
