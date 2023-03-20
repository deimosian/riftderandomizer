# Script to Remove Weapon Mod Randomization from Riftbreaker

# Define the locations of the input and output files relative to the script
input_file = './gamedata/scripts/blueprint_tables/weapon_mods.dat'
output_file = './moddata/scripts/blueprint_tables/weapon_mods.dat'

# Import Python RegEx module
import re

# Read the contents of the input file
with open(input_file, 'r') as f:
	content = f.read()

# Bring all player weapons into a list of strings
weapon_mods = re.findall(r'items/loot/weapon_mods/.*?(?:\n})', content, re.DOTALL)

# Work on each weapon string
for weapon_mod in weapon_mods:

	#Make a working copy of the weapon
	new_weapon_mod = weapon_mod

	# Bring all weapon stats into a list of strings
	moddescs = re.findall(r'WeaponModDesc.*?(?:\t})', weapon_mod, re.DOTALL)

	for moddesc in moddescs:

		# Get the maximum value
		max_value = re.search(r'(?<=max_value \")\d*.\d*', moddesc)

		# Get the minimum value
		min_value = re.search(r'(?<=min_value \")\d*.\d*', moddesc)

		#Make a working copy of the moddesc
		new_moddesc = moddesc

		# Check if a change is needed
		if max_value is not None and max_value.group() != min_value.group():

			# Create the change
			new_moddesc = re.sub(r'(?<=min_value \")\d*.\d*', max_value.group(), new_moddesc)

		if 'DAMAGE_CRITICAL_CHANCE' or 'AMMO_STUN' in stat_def:
			# Change the stat feature to minmax
			new_moddesc = new_moddesc.replace('PERCENTAGE', 'VALUE')

		# Apply the change
		new_weapon_mod = new_weapon_mod.replace(moddesc, new_moddesc)

		# Delete the change
		del new_moddesc
	
	# Replace the original weapon with the updated one
	content = content.replace(weapon_mod, new_weapon_mod)

	# Delete the update to prepare for another
	del new_weapon_mod

# Write the updated content to the output file
with open(output_file, 'w') as f:
	f.write(content)
