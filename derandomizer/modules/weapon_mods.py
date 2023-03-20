# Function to Remove Weapon Mod Randomization from Riftbreaker
def modify(input_subdir,output_subdir,weapon_mods_file):

	# Import Python RegEx module
	import os
	import re

	# Move to the input directory and read the contents of the Weapon Mods file
	script_dir = os.getcwd()
	weapon_mods_file_location = script_dir + input_subdir + weapon_mods_file
	# print(weapon_mods_file_location)
	with open(weapon_mods_file_location, 'r') as f:
		weapon_mods_contents = f.read()

	# Make a working copy of the contents
	new_weapon_mods_contents = weapon_mods_contents

	# Start the change counter
	weapon_mod_change_count = 0

	# Bring all player weapons into a list of strings
	weapon_mods = re.findall(r'items/loot/weapon_mods/.*?(?:\n})', weapon_mods_contents, re.DOTALL)

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
				weapon_mod_change_count = weapon_mod_change_count + 1

			# Change the value type to value for Crit and Stun
			if 'DAMAGE_CRITICAL_CHANCE' or 'AMMO_STUN' in stat_def:
				new_moddesc = new_moddesc.replace('PERCENTAGE', 'VALUE')
				weapon_mod_change_count = weapon_mod_change_count + 1

			# Apply the change
			new_weapon_mod = new_weapon_mod.replace(moddesc, new_moddesc)

			# Delete the change
			del new_moddesc
		
		# Replace the original weapon with the updated one
		new_weapon_mods_contents = new_weapon_mods_contents.replace(weapon_mod, new_weapon_mod)

		# Delete the update to prepare for another
		del new_weapon_mod

	# Write the updated content to the output file
	new_weapon_mods_file_location = script_dir + output_subdir + weapon_mods_file
	with open(new_weapon_mods_file_location, 'w') as f:
		f.write(new_weapon_mods_contents)

	return weapon_mod_change_count
	