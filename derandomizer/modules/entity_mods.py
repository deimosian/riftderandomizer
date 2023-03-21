# Function to Remove Entity Mod Randomization from Riftbreaker

def modify(input_subdir,output_subdir,entity_mods_file):

	# Import Python RegEx module
	import os
	import re

	# Move to the input directory and read the contents of the Weapon Mods file
	script_dir = os.getcwd()
	entity_mods_file_location = script_dir + input_subdir + entity_mods_file
	# print(entity_mods_file_location)
	with open(entity_mods_file_location, 'r') as f:
		entity_mods_contents = f.read()

	# Make a working copy of the contents
	new_entity_mods_contents = entity_mods_contents

	# Start the change counter
	entity_mod_change_count = 0

	# Bring all player weapons into a list of strings
	entity_mods = re.findall(r'items/upgrades/.*?(?:\n})', entity_mods_contents, re.DOTALL)

	# Work on each weapon string
	for entity_mod in entity_mods:

		#Make a working copy of the weapon
		new_entity_mod = entity_mod

		# Bring all weapon stats into a list of strings
		moddescs = re.findall(r'EntityModDesc.*?(?:\n\t})', entity_mod, re.DOTALL)

		for moddesc in moddescs:

			#Make a working copy of the moddesc
			new_moddesc = moddesc

			random_flags = re.findall(r'.*random.*', new_moddesc)
			for random_flag in random_flags:
				# Remove the default value line
				new_moddesc = re.sub(r'.*random.*\n','', new_moddesc)
				entity_mod_change_count = entity_mod_change_count + 1

			# Apply the change
			new_entity_mod = new_entity_mod.replace(moddesc, new_moddesc)

			# Delete the change
			del new_moddesc
		
		# Replace the original weapon with the updated one
		new_entity_mods_contents = new_entity_mods_contents.replace(entity_mod, new_entity_mod)

		# Delete the update to prepare for another
		del new_entity_mod

	# Write the updated content to the output file
	new_entity_mods_file_location = script_dir + output_subdir + entity_mods_file
	with open(new_entity_mods_file_location, 'w') as f:
		f.write(new_entity_mods_contents)

	return entity_mod_change_count
	