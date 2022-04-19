import pandas as pd
import glob
import re
import os


map_dict = {
    0: 'T-64BM "Bulat"',
    1: 'T-64BV',
    2: 'T-72AV',
    3: 'T-72B1',
    4: 'T-72B3',
    5: 'T-72BA',
    6: 'T-80BV',
    7: 'T-80BVM',
    8: 'T-80U',
    9: 'T-90'
}

def extract_number(f):
    s = re.findall("\d+$",f)
    return (int(s[0]) if s else -1, f)

def get_prediction(image_name):
    #     weights = "v13_10tanks_x.pt"
    weights = "v1.0_l.pt"
    os.system(f'py yolov5/detect.py --weights processed_weights/{weights} --img 640 --conf-thres 0.4 --source raw_images/{image_name}.jpg --save-txt --save-conf')

def get_txtpath():
    list_of_folders = [f.path for f in os.scandir('yolov5/runs/detect/') if f.is_dir()]
    letest = max(list_of_folders, key=extract_number)
    txtpath = glob.glob(letest + "/*/*.txt")
    try:
        return txtpath[0]
    except:
        return 404

def yolo2classname(txtpath):
  df = pd.read_csv(txtpath, sep = ' ', header=None)
  df.sort_values(by=5, ascending=False, inplace=True)
  df.reset_index(inplace=True)
  index = df[0][0]
  return map_dict[index]

def classname2info(classname):
    df = pd.read_csv('vehicles.csv')
    return df[df['name_en'] == classname].values.tolist()

  
def getinfo():
    txt_path = get_txtpath()
    if txt_path == 404:
        return 404
    print(txt_path)
    result = classname2info(yolo2classname(txt_path))
    name_en = result[0][1]
    name_ua = result[0][2]
    vehicle_type = result[0][3]
    operator = result[0][4]
    info_link = result[0][5]
    return name_en, name_ua, vehicle_type, operator, info_link
#    return 0, 1, 2, 3, 4, 5


