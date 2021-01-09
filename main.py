# file dialog header
import tkinter as tk
from tkinter import filedialog
# excel header
# # import openpyxl
import pandas as pd


# shelving
# check the way of input in choose list
def check_way(way):
    if way == "1" or way == "2":
        return True
    return False

# choose a excel file
def get_file_dialog():
    return filedialog.askopenfilename()

# read an epidemiological survey timeline from excel
def read_excel():
    file = get_file_dialog()
    # load sheet city
    pd_city = pd.read_excel(file, 'city')
    # load sheet dict(of addr)
    pd_dict = pd.read_excel(file, 'dict')
    # load sheet timeline
    pd_timeline = pd.read_excel(file, 'timeline')
    print(pd_city)
    print(pd_dict)
    print(pd_timeline)

# just using the excel way and shelving terminal
# read timeline form bash
def read_terminal():
    print("Please input a point-in-time and the postion in a line and exit with a \"E\"")
    while True:
        input()

# find the postion from baidu map
def pos_baidu(addr):
    pass

# find the postion from google map
def pos_google(addr):
    pass

# get all coordinate of addresses to a dict
def get_all_pos(addrs, dict_pos):
    for a in addrs:
        pos = pos_baidu(a)
        if pos != None:
            dict_pos[a] = pos
            continue
        pos = pos_google(a)
        if pos != None:
            dict_pos[a] = pos
            continue
        print(f"We can't find the postion(coordinate) of {a}.\\\
            \nYou can change it to a  broader one.")

# draw the map
def draw(timeline, dict_pos):
    # aaa
    pass

if __name__ == "__main__":
    print("Please choose the way you input: \\\
        1. excel    2.terminal")
    way_read = input()
    while check_way(way_read) == False:
        print("Please choose again. You should input correct number.")
        way_read = input()
    
    if way_read == "1":
        timeline = read_excel()
    elif way_read == "2":
        # shelving this way, just choose "1"
        timeline = read_terminal()
    else:
        print("error")
