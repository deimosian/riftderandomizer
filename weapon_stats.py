# Script to Remove Weapon Stat Randomization from Riftbreaker

# Define the locations of the input and output files relative to the script
input_file = './gamedata/scripts/blueprint_tables/weapon_stats.dat'
output_file = './moddata/scripts/blueprint_tables/weapon_stats.dat'

# Import Python RegEx module
import re

# Read the contents of the input file
with open(input_file, 'r') as f:
	content = f.read()

# Bring all player weapons into a list of strings
weapons = re.findall(r'items/weapons/.*?(?:\n})', content, re.DOTALL)

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

			# Convert stats which have a default value
			if default_value is not None:

				# Change the stat feature to minmax
				new_stat_def = new_stat_def.replace('BASE_DEFAULT', 'BASE_MINMAX')

				# Remove the default value line
				new_stat_def = re.sub(r'.*default_value.*\n','',new_stat_def)

				# Work on the ammo consumption
				if 'AMMO_COST' in stat_def:

					# Check if a change is needed
					if max_value is not None and max_value.group() != min_value.group():

						# Create the change
						new_stat_def = re.sub(r'(?<=max_value \")\d*.\d*', min_value.group(), new_stat_def)
						
				# Work on other stats besides ammo speed

				elif 'AMMO_SPEED' and 'WEAPON_SCALE' and 'BEAM_RANGE' not in stat_def:

					# Check if a change is needed
					if max_value is not None and max_value.group() != min_value.group():

						# Create the change
						new_stat_def = re.sub(r'(?<=min_value \")\d*.\d*', max_value.group(), new_stat_def)

			# Work on stats without a default value
			else:

				# Work on the ammo consumption
				if 'AMMO_COST' in stat_def:

					# Check if a change is needed
					if max_value is not None and max_value.group() != min_value.group():

						# Create the change
						new_stat_def = re.sub(r'(?<=max_value \")\d*.\d*', min_value.group(), new_stat_def)
						
				# Work on other stats besides ammo speed

				elif 'AMMO_SPEED' and 'WEAPON_SCALE' and 'BEAM_RANGE' not in stat_def:

					# Check if a change is needed
					if max_value is not None and max_value.group() != min_value.group():

						# Create the change
						new_stat_def = re.sub(r'(?<=min_value \")\d*.\d*', max_value.group(), new_stat_def)

			# Apply the change
			new_weapon = new_weapon.replace(stat_def, new_stat_def)

			# Delete the change
			del new_stat_def

	# Replace the original weapon with the updated one
	content = content.replace(weapon, new_weapon)

	# Delete the update to prepare for another
	del new_weapon

# Write the updated content to the output file
with open(output_file, 'w') as f:
	f.write(content)

