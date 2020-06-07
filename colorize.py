import re
import os
import sys
import glob
import json
import colorsys

hex_pattern = r'#([a-fA-F0-9]{6})([^a-fA-F0-9])'
hex_pattern_short = r'#([a-fA-F0-9]{3})([^a-fA-F0-9])'
rgba_pattern = r'rgba\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d(?:\.\d+)?)\)'
rgb_pattern = r'rgba\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)'

names = ["Red", "White", "Cyan", "Silver", "Blue", "Gray", "Grey", "DarkBlue", "Black", "LightBlue",
		"Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"]

files = {}
search = None

for arg in sys.argv:
	if arg.startswith("--src="):
		files["src"] = os.path.expanduser(arg.split("=")[1])
	if arg.startswith("--dest="):
		files["dest"] = os.path.expanduser(arg.split("=")[1])
	if arg.startswith("--config="):
		files["config"] = os.path.expanduser(arg.split("=")[1])
	if arg.startswith("--search"):
		search = arg.split("=")[1]

if "src" not in files:
	print("missing source")
	exit()
if not search:
	if "dest" not in files:
		print("missing destination")
		exit()
	if "config" not in files:
		print("missing config")
		exit()
	else:
		config = json.load(open(files["config"], "r"))



# returns an hsv with a scale of: hue [0, 1], saturation [0, 1], value [0, 1]
def to_hsv(color):
	# Source format: #HHHHHH
	match = re.match(r'#([a-fA-F0-9]{6})', color)

	if match:
		hex_source = match.group(0).strip('#')
		rgb_source = tuple(int(hex_source[i:i+2], 16) for i in (0, 2, 4))
		return colorsys.rgb_to_hsv(rgb_source[0]/255, rgb_source[1]/255, rgb_source[2]/255)
	
	# Source format: #HHH
	match = re.match(r'#([a-fA-F0-9]{3})', color)

	if match:
		hex_source = match.group(0).strip('#')
		rgb_source = tuple(int(hex_source[i] + hex_source[i], 16) for i in (0, 1, 2))
		return colorsys.rgb_to_hsv(rgb_source[0]/255, rgb_source[1]/255, rgb_source[2]/255)

	# Source format: rgba(int, int, int, float)
	match = re.match(rgba_pattern, color)

	if match:
		rgb_source = (int(match.group(1), 16), int(match.group(2), 16), int(match.group(3), 16))
		return colorsys.rgb_to_hsv(rgb_source[0]/255, rgb_source[1]/255, rgb_source[2]/255)

	# Source format: rgb(int, int, int)
	match = re.match(rgb_pattern, color)

	if match:
		rgb_source = (int(match.group(1), 16), int(match.group(2), 16), int(match.group(3), 16))
		return colorsys.rgb_to_hsv(rgb_source[0]/255, rgb_source[1]/255, rgb_source[2]/255)

	return None

# takes an rgb tuple with a range of [0,1] on all values
def rgb_to_hex(rgb):
	hex_destination = "#"

	for i in rgb:
		value = hex(round(i * 255)).split("x")[1]

		if len(value) == 1:
			value = "0" + value

		hex_destination += value

	return hex_destination

# takes an hsv with a scale of: hue [0,1], saturation [0, 1], value [0, 1]
def hsv_to_hex(hsv):
	return rgb_to_hex(colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]))

#Operate on a scale of: hue [0,360], saturation [0, 100], value [0, 100]
#If a conversion was found, it will return the new hsv
#If no conversion was found then it won't return anything
def convert(hsv):
	if hsv[1] == 0:
		hsv = (0, hsv[1], hsv[2])
	if hsv[2] == 0:
		hsv = (0, 0, 0)

	destination_hsv = hsv

	for color in sorted(config):
		match = (False, False, False)
		from_hue_value = None
		from_saturation_value = None
		from_value_value = None
		
		if "name" in config[color]["from"]:
			if config[color]["from"]["name"].lower() == "white" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#FFFFFF"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "black" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#000000"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "red" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#FF0000"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "dark orange" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#FF8000"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "orange" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#FFA500"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "yellow" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#FFFF00"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "lime" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#00FF00"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "green" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#008000"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "cyan" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#00FFFF"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "magenta" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#FF00FF"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "brown" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#A52A2A"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "Silver" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#C0C0C0"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "Gray" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#808080"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "Grey" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#808080"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "Maroon" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#800000"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "Olive" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#808000"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "DarkBlue" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#0000A0"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "LightBlue" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#ADD8E6"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "Purple" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#800080"):
				match = (True, True, True)
			if config[color]["from"]["name"].lower() == "brown" and (hsv_to_hex((round(hsv[0]/360), round(hsv[1]/100),round(hsv[2]/100))) == "#A52A2A"):
				match = (True, True, True)
		else:
			if "hue" in config[color]["from"]:
				from_hue_value = config[color]["from"]["hue"]["value"]
				from_hue_min = from_hue_value
				from_hue_max = from_hue_value
				if "min" in config[color]["from"]["hue"]: from_hue_min = config[color]["from"]["hue"]["min"]
				if "max" in config[color]["from"]["hue"]: from_hue_max = config[color]["from"]["hue"]["max"]
				
				if hsv[0] >= from_hue_min and hsv[0] <= from_hue_max:
					match = (True, match[1], match[2])
			else:
				match = (True, match[1], match[2])

			if "saturation" in config[color]["from"]:
				from_saturation_value = config[color]["from"]["saturation"]["value"]
				from_saturation_min = from_saturation_value
				from_saturation_max = from_saturation_value
				if "min" in config[color]["from"]["saturation"]: from_saturation_min = config[color]["from"]["saturation"]["min"]
				if "max" in config[color]["from"]["saturation"]: from_saturation_max = config[color]["from"]["saturation"]["max"]
				
				if hsv[1] >= from_saturation_min and hsv[1] <= from_saturation_max:
					match = (match[0], True, match[2])
			else:
				match = (match[0], True, match[2])

			if "value" in config[color]["from"]:
				from_value_value = config[color]["from"]["value"]["value"]
				from_value_min = from_value_value
				from_value_max = from_value_value
				if "min" in config[color]["from"]["value"]: from_value_min = config[color]["from"]["value"]["min"]
				if "max" in config[color]["from"]["value"]: from_value_max = config[color]["from"]["value"]["max"]
				
				if hsv[2] >= from_value_min and hsv[2] <= from_value_max:
					match = (match[0], match[1], True)
			else:
				match = (match[0], match[1], True)

		if match[0] and match[1] and match [2]:
			if "hue" in config[color]["to"]:
				to_hue_value = config[color]["to"]["hue"]["value"]
				to_hue_min = to_hue_value
				to_hue_max = to_hue_value
				if "min" in config[color]["to"]["hue"]: to_hue_min = config[color]["to"]["hue"]["min"]
				if "max" in config[color]["to"]["hue"]: to_hue_max = config[color]["to"]["hue"]["max"]
				
				if from_hue_value:
					hue_distance = hsv[0] - from_hue_value
					hue_bottom_scale = (from_hue_value - from_hue_min) / (to_hue_value - to_hue_min)
					hue_top_scale = (from_hue_max - from_hue_value) / (to_hue_max - to_hue_value)

					if hsv[0] <= to_hue_value: destination_hsv = (hue_distance * hue_bottom_scale, destination_hsv[1], destination_hsv[2])
					else: destination_hsv = (hue_distance * hue_top_scale, destination_hsv[1], destination_hsv[2])
				else:
					destination_hsv = (to_hue_value, destination_hsv[1], destination_hsv[2])

			if "saturation" in config[color]["to"]:
				to_saturation_value = config[color]["to"]["saturation"]["value"]
				to_saturation_min = to_saturation_value
				to_saturation_max = to_saturation_value
				if "min" in config[color]["to"]["saturation"]: to_saturation_min = config[color]["to"]["saturation"]["min"]
				if "max" in config[color]["to"]["saturation"]: to_saturation_max = config[color]["to"]["saturation"]["max"]
				
				if from_saturation_value:
					saturation_distance = hsv[0] - from_saturation_value
					saturation_bottom_scale = (from_saturation_value - from_saturation_min) / (to_saturation_value - to_saturation_min)
					saturation_top_scale = (from_saturation_max - from_saturation_value) / (to_saturation_max - to_saturation_value)

					if hsv[0] <= to_saturation_value: destination_hsv = (destination_hsv[0], saturation_distance * saturation_bottom_scale, destination_hsv[2])
					else: destination_hsv = (destination_hsv[0], saturation_distance * saturation_top_scale, destination_hsv[2])
				else:
					destination_hsv = (destination_hsv[0], to_saturation_value, destination_hsv[2])

			if "value" in config[color]["to"]:
				to_value_value = config[color]["to"]["value"]["value"]
				to_value_min = to_value_value
				to_value_max = to_value_value
				if "min" in config[color]["to"]["value"]: to_value_min = config[color]["to"]["value"]["min"]
				if "max" in config[color]["to"]["value"]: to_value_max = config[color]["to"]["value"]["max"]
				
				if from_value_value:
					value_distance = hsv[0] - from_value_value
					value_bottom_scale = (from_value_value - from_value_min) / (to_value_value - to_value_min)
					value_top_scale = (from_value_max - from_value_value) / (to_value_max - to_value_value)

					if hsv[0] <= to_value_value: destination_hsv = (value_distance * value_bottom_scale, destination_hsv[1], destination_hsv[2])
					else: destination_hsv = (value_distance * value_top_scale, destination_hsv[1], destination_hsv[2])
				else:
					destination_hsv = (to_value_value, destination_hsv[1], destination_hsv[2])
			return destination_hsv

def convert_hex(match):
	hex_source = match.group(0).strip('#')
	rgb_source = tuple(int(hex_source[i:i+2], 16) for i in (0, 2, 4))
	hsv_source = colorsys.rgb_to_hsv(rgb_source[0]/255, rgb_source[1]/255, rgb_source[2]/255)

	hsv_destination = convert((hsv_source[0] * 360, hsv_source[1] * 100, hsv_source[2] * 100))
	
	if hsv_destination:
		hsv_destination = (hsv_destination[0] / 360, hsv_destination[1] / 100, hsv_destination[2] / 100)
		rgb_destination = colorsys.hsv_to_rgb(hsv_destination[0], hsv_destination[1], hsv_destination[2])

		hex_destination = "#"

		for i in rgb_destination:
			value = hex(round(i * 255)).split("x")[1]

			if len(value) == 1:
				value = "0" + value

			hex_destination += value

		return hex_destination + match.group(2)
	
	return match.group(0)

def convert_hex_short(match):
	hex_source = match.group(0).strip('#')
	rgb_source = tuple(int(hex_source[i] + hex_source[i], 16) for i in (0, 1, 2))
	hsv_source = colorsys.rgb_to_hsv(rgb_source[0]/255, rgb_source[1]/255, rgb_source[2]/255)

	hsv_destination = convert((hsv_source[0] * 360, hsv_source[1] * 100, hsv_source[2] * 100))

	if hsv_destination:
		hsv_destination = (hsv_destination[0] / 360, hsv_destination[1] / 100, hsv_destination[2] / 100)
		rgb_destination = colorsys.hsv_to_rgb(hsv_destination[0], hsv_destination[1], hsv_destination[2])

		hex_destination = "#"

		for i in rgb_destination:
			value = hex(round(i * 255)).split("x")[1]

			if len(value) == 1:
				value = "0" + value

			hex_destination += value
		
		return hex_destination + match.group(2)

	return match.group(0)

def convert_rgba(match):
	rgb_source = (int(match.group(1), 16), int(match.group(2), 16), int(match.group(3), 16))
	hsv_source = colorsys.rgb_to_hsv(rgb_source[0]/255, rgb_source[1]/255, rgb_source[2]/255)

	hsv_destination = convert((hsv_source[0] * 360, hsv_source[1] * 100, hsv_source[2] * 100))

	if hsv_destination:
		hsv_destination = (hsv_destination[0] / 360, hsv_destination[1] / 100, hsv_destination[2] / 100)
		rgb_destination = colorsys.hsv_to_rgb(hsv_destination[0], hsv_destination[1], hsv_destination[2])

		return "rgba(" + str(round(rgb_destination[0] * 255)) + ", " + str(round(rgb_destination[1] * 255)) + ", " + str(round(rgb_destination[2] * 255)) + ", " + match.group(4) + ")"
	
	match.group(0)

def convert_rgb(match):
	rgb_source = (int(match.group(1), 16), int(match.group(2), 16), int(match.group(3), 16))
	hsv_source = colorsys.rgb_to_hsv(rgb_source[0]/255, rgb_source[1]/255, rgb_source[2]/255)

	hsv_destination = convert((hsv_source[0] * 360, hsv_source[1] * 100, hsv_source[2] * 100))

	if hsv_destination:
		hsv_destination = (hsv_destination[0] / 360, hsv_destination[1] / 100, hsv_destination[2] / 100)
		rgb_destination = colorsys.hsv_to_rgb(hsv_destination[0], hsv_destination[1], hsv_destination[2])
		
		return "rgb(" + str(round(rgb_destination[0] * 255)) + ", " + str(round(rgb_destination[1] * 255)) + ", " + str(round(rgb_destination[2] * 255)) + ")"
	
	match.group(0)

def convert_name(match):
	print(match.group(0))
	if match.group(0).lower() == "white":
		hsv_source = (0, 0, 1)
	if match.group(0).lower() == "red":
		hsv_source = (0, 1, 1)
	if match.group(0).lower() == "grey" or match.group(0).lower() == "gray":
		hsv_source = (0, 0, 0.52)

	hsv_destination = convert((hsv_source[0] * 360, hsv_source[1] * 100, hsv_source[2] * 100))

	if hsv_destination:
		hsv_destination = (hsv_destination[0] / 360, hsv_destination[1] / 100, hsv_destination[2] / 100)
		rgb_destination = colorsys.hsv_to_rgb(hsv_destination[0], hsv_destination[1], hsv_destination[2])
		
		return "rgb(" + str(round(rgb_destination[0] * 255)) + ", " + str(round(rgb_destination[1] * 255)) + ", " + str(round(rgb_destination[2] * 255)) + ")"
	
	match.group(0)

recursive = "-r" in sys.argv

if search:
	search = search.replace("'", "")

	if not search.startswith("rgb") and not search.startswith("#"):
		search = "#" + search
		
	search_hex = hsv_to_hex(to_hsv(search))

	for src_file in glob.glob(files["src"] + "/**/*", recursive=recursive):
		if os.path.isfile(src_file) and src_file not in files:
			try:
				show = False
				output = ""
				for index, line in enumerate(open(src_file, "r").readlines()):
					colors = []
					colors += [match[0] for match in re.findall(hex_pattern, line) if match]
					colors += [match[0] for match in re.findall(hex_pattern_short, line) if match]
					colors += ["rgba" + str(match) for match in re.findall(rgba_pattern, line) if match]
					colors += ["rgb" + str(match) for match in re.findall(rgb_pattern, line) if match]
					
					for color in colors:
						color = color.replace("'", "")

						if not color.startswith("rgb"):
							color = "#" + color

						color_hex = hsv_to_hex(to_hsv(color))

						if color_hex == search_hex:
							show = True
							output += "Line " + str(index) + ":\n" + str(line)
							break
				
				if show:
					print("File: " + src_file)
					print(output)
			except UnicodeDecodeError:
				pass
else:
	for src_file in glob.glob(files["src"] + "/**/*", recursive=recursive):
		dest_file = src_file.replace(files["src"], files["dest"])

		if os.path.isdir(src_file) and not os.path.exists(dest_file):
			os.makedirs(dest_file)
		
		if os.path.isfile(src_file) and src_file not in files:
			try:
				output = ""
				print("File: " + src_file)
				for index, line in enumerate(open(src_file, "r").readlines()):
					text = re.sub(hex_pattern, convert_hex, line)
					text = re.sub(hex_pattern_short, convert_hex_short, text)
					text = re.sub(rgba_pattern, convert_rgba, text)
					
					for name in [name.lower() for name in names]:
						text = re.sub(name, convert_name, text)

					if "--verbose" in sys.argv and (re.search(hex_pattern, line) or re.search(rgba_pattern, line)):
						print("Line " + str(index) + ": ")
						print(line + text)
					output += text

				open(dest_file, "w").write(output)
			except UnicodeDecodeError:
				pass
