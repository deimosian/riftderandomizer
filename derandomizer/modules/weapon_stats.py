# Function to Remove Weapon Stat Randomization from Riftbreaker
def modify(input_subdir,output_subdir,weapon_stats_file):

	# Import Python RegEx module
	import os
	import re

	# Move to the input directory and read the contents of the Weapon Stats file
	script_dir = os.getcwd()
	weapon_stats_file_location = script_dir + input_subdir + weapon_stats_file
	with open(weapon_stats_file_location, 'r') as f:
		weapon_stats_contents = f.read()
	
	# Make a working copy of the contents
	new_weapon_stats_contents = weapon_stats_contents

	# Start the change counter
	weapon_stat_change_count = 0

	# Bring all player weapons into a list of strings
	weapons = re.findall(r'items/weapons/.*?(?:\n})', weapon_stats_contents, re.DOTALL)

	# Work on each weapon string
	for weapon in weapons:

		#Make a working copy of the weapon
		new_weapon = weapon

		# Bring all weapon stats into a list of strings
		stat_defs = re.findall(r'WeaponStatDef.*?(?:\t})', weapon, re.DOTALL)

		# Work on each weapon stat
		for stat_def in stat_defs:

			# Get the maximum value
			default_value = re.search(r'(?<=default_value \")\d*.\d*', stat_def)

			# Get the maximum value
			max_value = re.search(r'(?<=max_value \")\d*.\d*', stat_def)

			# Get the minimum value
			min_value = re.search(r'(?<=min_value \")\d*.\d*', stat_def)
			
			# Check if change is needed
			if max_value is not None:
			
				# Make a working copy of the stat
				new_stat_def = stat_def

				# Remove the randomizable stat feature
				if '|INITIAL_RANDOMIZABLE' in stat_def:
					new_stat_def = new_stat_def.replace('|INITIAL_RANDOMIZABLE', '')
					weapon_stat_change_count = weapon_stat_change_count + 1

				# Convert stats which have a default value
				if default_value is not None:

					# Change the stat feature to minmax
					new_stat_def = new_stat_def.replace('BASE_DEFAULT', 'BASE_MINMAX')
					weapon_stat_change_count = weapon_stat_change_count + 1

					# Remove the default value line
					new_stat_def = re.sub(r'.*default_value.*\n','',new_stat_def)
					weapon_stat_change_count = weapon_stat_change_count + 1

				# Work on the ammo consumption
				if 'AMMO_COST' in stat_def:

					# Check if a change is needed
					if max_value is not None and max_value.group() != min_value.group():

						# Create the change
						new_stat_def = re.sub(r'(?<=max_value \")\d*.\d*', min_value.group(), new_stat_def)
						weapon_stat_change_count = weapon_stat_change_count + 1

				# Work on other relevant stats
				elif 'AMMO_SPEED' and 'WEAPON_SCALE' and 'BEAM_RANGE' not in stat_def:

					# Check if a change is needed
					if max_value is not None and max_value.group() != min_value.group():

						# Create the change
						new_stat_def = re.sub(r'(?<=min_value \")\d*.\d*', max_value.group(), new_stat_def)
						weapon_stat_change_count = weapon_stat_change_count + 1

				# Apply the change
				new_weapon = new_weapon.replace(stat_def, new_stat_def)

				# Delete the change
				del new_stat_def

		# Replace the original weapon with the updated one
		new_weapon_stats_contents = new_weapon_stats_contents.replace(weapon, new_weapon)

		# Delete the update to prepare for another
		del new_weapon

	# Write the updated content to the output file
	new_weapon_stats_file_location = script_dir + output_subdir + weapon_stats_file
	with open(new_weapon_stats_file_location, 'w') as f:
		f.write(new_weapon_stats_contents)

	return weapon_stat_change_count
