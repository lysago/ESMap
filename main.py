# file dialog header
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
    if way == '1' or way == '2' or way == '3':
        return True
    return False

# choose a excel file
def get_file_dialog():
    return filedialog.askopenfilename()

# read an epidemiological survey timeline from excel
def read_excel(file):
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

# find the location from baidu map
def gencode_baidu(city, addr):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = 'pRoqaGDWc11FYHs4o6ANx51lWAUTcsW8' # find in Internet
    rq_city = rq.quote(city)
    rq_addr = rq.quote(addr)
    url = url + '?' + 'address=' + rq_addr + '&city=' + rq_city + '&output=' + output + '&ak=' + ak + '&callback=showLocation'
    req = rq.urlopen(url)
    res = req.read().decode('utf-8')
    reslist = re.split(r'[()]', res)
    res = reslist[1]
    print(res)
    dict_res = json.loads(res)
    if dict_res['status'] == 0 and dict_res['result']['comprehension'] >= 60:
        loc_dict = dict_res['result']['location']
        location = []
        location.append(loc_dict['lng'])
        location.append(loc_dict['lat'])
        return location
    else:
        return None

# find the location from google map
def gencode_google(addr):
    pass

# find the location from Amap
def gencode_Amap(city, addr):
    url = 'https://restapi.amap.com/v3/geocode/geo'
    output = 'json'
    ak = '759c9d4904eadceb66c9aafdfb8bf161' # find in Internet
    rq_city = rq.quote(city)
    rq_addr = rq.quote(addr)
    url = url + '?' + 'address=' + rq_addr + '&city=' + rq_city + '&output=' + output + '&key=' + ak
    req = rq.urlopen(url)
    res = req.read().decode('utf-8')
    print(res)
    dict_res = json.loads(res)
    if dict_res['status'] == '1' and int(dict_res['count']) >= 1:
        loc_str = dict_res['geocodes'][0]['location']
        loc_strlist = re.split(r',', loc_str)
        location = [float(l) for l in loc_strlist ]
        return location
    else:
        return None

# duplicate removal
def get_addrs_by_one(df_timeline):
    addrs = df_timeline['address'].drop_duplicates().values.tolist()
    print(addrs)
    return addrs

# get all coordinate of addresses to a dict
def get_all_loc(city, dict_addr, df_timeline):
    addrs = get_addrs_by_one(df_timeline)
    loc  = 0
    dict_loc = {}
    for a in addrs:
        if dict_addr.get(a):
            full_a = city + dict_addr[a]
        else:
            full_a = city + a
        loc = gencode_baidu(city, full_a)
        if loc != None:
            dict_loc[a] = loc
            continue
        loc = gencode_Amap(city, full_a)
        if loc != None:
            dict_loc[a] = loc
            continue
        print(f"We can't find the location(coordinate) of {a}.You can change it to a  broader one.")
    print(dict_loc)
    return dict_loc

def get_scale(dict_loc):
    # l, r, u, l
    # cause China in 73.66-135.05,3.86-53.55
    bound = [180.0, 90.0, 0.0, 0.0]
    for k, v in dict_loc.items():
        bound[0] = min(v[0], bound[0])
        bound[1] = min(v[1], bound[1])
        bound[2] = max(v[0], bound[2])
        bound[3] = max(v[1], bound[3])
    # center = [(bound[0] + bound[2]) / 2, (bound[1] + bound[3]) / 2]
    return bound

# draw the map
def draw(timeline, dict_loc):
    url = 'http://api.map.baidu.com/staticimage/v2'
    ak = 'pRoqaGDWc11FYHs4o6ANx51lWAUTcsW8' # find in Internet
    bound = get_scale(dict_loc)
    loc_strlist = []
    for k in dict_loc:
        loc_str = str(dict_loc[k][0]) + ',' + str(dict_loc[k][1])
        loc_strlist.append(loc_str)
    marker_str = '|'.join(loc_strlist)
    url = url + '?' + 'bbox=' + str(bound[0]) + ',' + str(bound[1]) + ';' + str(bound[2]) + ',' + str(bound[3]) + '&markers=' + marker_str + '&ak=' + ak
    print(url)


if __name__ == '__main__':
    print('Please choose the way you input: \\\
        1. excel    2.terminal  3.test')
    '''    
    way_read = input()
    while check_way(way_read) == False:
        print('Please choose again. You should input correct number.')
        way_read = input()
    '''
    way_read = '3'
    
    if way_read == '1':
        # one by dialog, mutli by code circle 
        file = get_file_dialog()
    elif way_read == '2':
        file = input('Please input the excel path.\n')
    elif way_read == '3':
        file = './test.xlsx'
    else:
        print('error')
        exit()
    city, dict_addr, df_timeline = read_excel(file)

    dict_loc = get_all_loc(city, dict_addr, df_timeline)
    draw(df_timeline, dict_loc)

    
