#!/bin/sh
cd ~/RADC/
python3 copy_untar.py && python3 auto_dcm2bids.py -d ~/RADC/Data/ -o ~/RADC/BIDS/ -c ~/RADC/config_uc.json && python3 clear_data.py;
# python3 copy_untar.py && python3 auto_dcm2bids.py -d ~/RADC/Data/ -o ~/RADC/BIDS/ -c ~/RADC/config_uc.json;