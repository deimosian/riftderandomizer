# Script to run the derandomizer and package the output as a zip file

# Import modules
import os
import re
import shutil
import subprocess
from modules import entity_mods
from modules import weapon_mods
from modules import weapon_stats

# Set directory and file name variables
input_subdir = '/derandomizer/game_data'
output_subdir = '/derandomizer/mod_data'
entity_mods_file = '/scripts/blueprint_tables/entity_mods.dat'
weapon_mods_file = '/scripts/blueprint_tables/weapon_mods.dat'
weapon_stats_file = '/scripts/blueprint_tables/weapon_stats.dat'
readme_file_location = 'README.md'

# Modify the Entity Mods
entity_mod_change_count = entity_mods.modify(input_subdir,output_subdir,entity_mods_file)

# Modify the Weapon Mods
weapon_mod_change_count = weapon_mods.modify(input_subdir,output_subdir,weapon_mods_file)

# Modify the Weapon Stats
weapon_stats_change_count = weapon_stats.modify(input_subdir,output_subdir,weapon_stats_file)

print("Made " + str(entity_mod_change_count) + " Entity Mod Changes.")
print("Made " + str(weapon_mod_change_count) + " Weapon Mod Changes.")
print("Made " + str(weapon_stats_change_count) + " Weapon Stats Changes.")

# Update statistics in README
with open(readme_file_location, 'r') as f:
	readme_contents = f.read()

re.sub(r'(?<=Made )\d*(?= Entity Mod Changes)', str(entity_mod_change_count), readme_contents)
re.sub(r'(?<=Made )\d*(?= Weapon Mod Changes)', str(entity_mod_change_count), readme_contents)
re.sub(r'(?<=Made )\d*(?= Weapon Stats Changes)', str(entity_mod_change_count), readme_contents)

with open(readme_file_location, 'w') as f:
	f.write(readme_contents)

shutil.make_archive('derandomizer', 'zip', "./" + output_subdir)

