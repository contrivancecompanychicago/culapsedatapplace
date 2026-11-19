#Experiment A for Alcorn with R pixel channel
from replit import db

db['r_pixel_entry1'] = 'r_row1'
db['r_pixel_entry2'] = 'r_row2'
db['r_pixel_entry3'] = 'r_row3'

for key in db.keys():
  print(key)
  print(db[key])
db['alcorn_list1'] = [0.8, 0.80, 0.79]
db['alcorn_dict_entry1'] = {'r_pixel': 'columnA', 'g_pixel': 'columnB', 'b_pixel': 'columnC'}

print(db.prefix('alcorn_entry'))
