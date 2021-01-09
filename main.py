# file dialog header
import tkinter as tk
from tkinter import filedialog
# excel header
# # import openpyxl
import pandas as pd
# gencoder
import json
import urllib.request as rq
# string split
import re


# shelving
# check the way of input in choose list
def check_way(way):
    if way == '1' or way == '2':
        return True
    return False

# choose a excel file
def get_file_dialog():
    return filedialog.askopenfilename()

# read an epidemiological survey timeline from excel
def read_excel():
    # one by dialog, mutli by code circle 
    file = get_file_dialog()
    # load sheet city
    df_city = pd.read_excel(file, 'city')
    city = df_city.iloc[0,0]
    # load sheet dict(of addr)
    # dict must be not empty, include home address at least
    df_dict = pd.read_excel(file, 'dict')
    dict_addr = {}
    for row in df_dict.itertuples():
        key = getattr(row, 'key')
        value = getattr(row, 'value')
        dict_addr[key] = value
    # load sheet timeline
    df_timeline = pd.read_excel(file, 'timeline')
    print(df_city)
    print(df_dict)
    print(df_timeline)
    print(city)
    print(dict_addr)
    return city, dict_addr, df_timeline

# just using the excel way and shelving terminal
# read timeline form bash
def read_terminal():
    print('Please input a point-in-time and the postion in a line and exit with a \"E\"')
    while True:
        input()

# find the postion from baidu map
def pos_baidu(city, addr):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = 'pRoqaGDWc11FYHs4o6ANx51lWAUTcsW8' # find in Internet
    rq_city = rq.quote(city)
    rq_addr = rq.quote(addr)
    url = url + '?' + 'address=' + rq_addr + '&city=' + rq_city + '&output=' + output + '&ak=' + ak + '&callback=showLocation'
    req = rq.urlopen(url)
    res = req.read().decode("utf-8")
    reslist = re.split(r'[()]', res)
    res = reslist[1]
    print(res)
    dict_res = json.loads(res)
    if dict_res['status'] == 0 and dict_res['result']['comprehension'] >= 60:
        return dict_res['result']['location']
    else:
        return None

# find the postion from google map
def pos_google(addr):
    pass

# duplicate removal
def get_addrs_by_one(df_timeline):
    addrs = df_timeline['address'].drop_duplicates().values.tolist()
    print(addrs)
    return addrs

# get all coordinate of addresses to a dict
def get_all_pos(city, dict_addr, df_timeline):
    addrs = get_addrs_by_one(df_timeline)
    pos  = 0
    dict_pos = {}
    for a in addrs:
        if dict_addr.get(a):
            full_a = city + dict_addr[a]
        else:
            full_a = city + a
        pos = pos_baidu(city, full_a)
        if pos != None:
            dict_pos[a] = pos
            continue
        pos = pos_google(full_a)
        if pos != None:
            dict_pos[a] = pos
            continue
        print(f"We can't find the postion(coordinate) of {a}.You can change it to a  broader one.")
    return dict_pos

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
        city, dict_addr, df_timeline = read_excel()
    elif way_read == "2":
        # shelving this way, just choose "1"
        city, dict_addr, df_timeline = read_terminal()
    else:
        print("error")

    dict_pos = get_all_pos(city, dict_addr, df_timeline)

    
