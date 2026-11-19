#Experiment B for Alcorn with R pixel channel
from replit import db

db['r_pixel_entry4'] = 'r_row4'
db['r_pixel_entry5'] = 'r_row5'
db['r_pixel_entry6'] = 'r_row6'

for key in db.keys():
  print(key)
  print(db[key])
db['alcorn_list2'] = [0.212, 0.220, 0.220]
db['alcorn_dict_entry1'] = {'r_pixel': 'columnA', 'g_pixel': 'columnB', 'b_pixel': 'columnC'}

print(db.prefix('alcorn_entry'))
