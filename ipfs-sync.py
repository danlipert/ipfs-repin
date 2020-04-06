import json
import os
import sys

import wget


THIS_SERVER = os.getenv("THIS_SERVER")
OTHER_SERVER = os.getenv("OTHER_SERVER")
IPFS_PIN_LS_URI_FMT = "{}/api/v0/pin/ls"

other_pins_url = IPFS_PIN_LS_URI_FMT.format(OTHER_SERVER)
this_pins_url = IPFS_PIN_LS_URI_FMT.format(THIS_SERVER)

this_pins_filename = wget.download(this_pins_url, out="this-pins.json")

if len(sys.argv) == 0:
    other_pins_filename = wget.download(other_pins_url, out="other-pins.json")
else:
    other_pins_filename = sys.argv[0]

with open(other_pins_filename) as other_pins_file:
    other_pins = json.load(other_pins_file)

with open(this_pins_filename) as this_pins_file:
    this_pins = json.load(this_pins_file)

delta_pins = [k for k in other_pins['Keys'] if k not in this_pins['Keys']]

with open("delta-pins.keys", 'w') as delta_pins_file:
    delta_pins_file.write("\n".join(delta_pins))
    delta_pins_file.close()

print('Other pins count:{}'.format(len(other_pins['Keys'])))
print('This pins count:{}'.format(len(this_pins['Keys'])))
print('Delta pins count:{}'.format(len(delta_pins)))

print('delta_pins:')
for p in delta_pins:
    print(p)

os.system('cat delta-pins.keys | tee /dev/stderr | xargs -n 1 ipfs pin add --recursive')
