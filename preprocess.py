from config import *
from glob import glob
from skimage import io
import plotly.express as px
import pandas as pd
import xml.etree.ElementTree as xet


# Parse data from XML and convert into CSV
path = glob(f'{ANNOTATIONS_DIR}/*.xml')
labels_dict = dict(filepath=[], xmin=[], xmax=[], ymin=[], ymax=[])

for filename in path:
    info = xet.parse(filename)
    root = info.getroot()
    member_object = root.find('object')
    
    labels_info = member_object.find('bndbox')
    xmin = int(labels_info.find('xmin').text)
    xmax = int(labels_info.find('xmax').text)
    ymin = int(labels_info.find('ymin').text)
    ymax = int(labels_info.find('ymax').text)
    # Since the used dataset is aggregated from two different sources, 
    # there are two image formats: png and jpeg, 
    # images are named as "Cars<INDEX>.png" or "N<INDEX>.jpeg"
    postfix = 'png' if 'Cars' in filename else 'jpeg'
    filename = filename.replace('annotations', 'images').replace('xml', postfix)
    
    labels_dict['xmin'].append(xmin)
    labels_dict['xmax'].append(xmax)
    labels_dict['ymin'].append(ymin)
    labels_dict['ymax'].append(ymax)
    labels_dict['filepath'].append(filename)

df = pd.DataFrame(labels_dict)
df.to_csv(LABELS_CSV, index=False)
img_path = list(df['filepath'])

# Verify data
idx   = 20
xmin  = df['xmin'][idx]
xmax  = df['xmax'][idx]
ymin  = df['ymin'][idx]
ymax  = df['ymax'][idx]
fpath = img_path[idx]

img = io.imread(fpath)
fig = px.imshow(img)
fig.update_layout(width=600, height=500, margin=dict(l=10, r=10, b=10, t=10))
fig.add_shape(type='rect', x0=xmin, x1=xmax, y0=ymin, y1=ymax, xref='x', yref='y', line_color='cyan')
fig.show()