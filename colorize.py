import re
import os
import sys
import glob
import json
import colorsys

hex_pattern = r'#([a-fA-F0-9]{6})([^a-fA-F0-9])'
hex_pattern_short = r'#([a-fA-F0-9]{3})([^a-fA-F0-9])'
rgba_pattern = r'rgba\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d(?:\.\d+)?)\)'
finder = re.compile(hex_pattern)

config = json.load(open(sys.argv[2], "r"))

#Operate on a scale of: hue [0,360], saturation [0, 100], value [0, 100]
def convert(hsv):
	destination_hsv = hsv

	for color in sorted(config):
		match = (False, False, False)
		from_hue_value = None
		from_saturation_value = None
		from_value_value = None

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
	# print("hex_source", hex_source)
	rgb_source = tuple(int(hex_source[i:i+2], 16) for i in (0, 2, 4))
	# print("rgb_source", rgb_source)
	hsv_source = colorsys.rgb_to_hsv(rgb_source[0]/255, rgb_source[1]/255, rgb_source[2]/255)
	# print("hsv_source", hsv_source)

	hsv_destination = convert((hsv_source[0] * 360, hsv_source[1] * 100, hsv_source[2] * 100))
	
	if hsv_destination:
		hsv_destination = (hsv_destination[0] / 360, hsv_destination[1] / 100, hsv_destination[2] / 100)

		# hsv_destination = (30/360, hsv_source[1], hsv_source[2])
		# print("hsv_destination", hsv_destination)
		rgb_destination = colorsys.hsv_to_rgb(hsv_destination[0], hsv_destination[1], hsv_destination[2])
		# print("rgb_destination", rgb_destination)
		hex_destination = "#"
		for i in rgb_destination:
			value = hex(round(i * 255)).split("x")[1]
			if len(value) == 1:
				value = "0" + value
			hex_destination += value
		# print("hex_destination", hex_destination)
		return hex_destination + match.group(2)
	
	return match.group(0)

def convert_hex_short(match):
	hex_source = match.group(0).strip('#')
	# print("hex_source", hex_source)
	rgb_source = tuple(int(hex_source[i] + hex_source[i], 16) for i in (0, 1, 2))
	# print("rgb_source", rgb_source)
	hsv_source = colorsys.rgb_to_hsv(rgb_source[0]/255, rgb_source[1]/255, rgb_source[2]/255)
	# print("hsv_source", hsv_source)

	hsv_destination = convert((hsv_source[0] * 360, hsv_source[1] * 100, hsv_source[2] * 100))

	if hsv_destination:
		hsv_destination = (hsv_destination[0] / 360, hsv_destination[1] / 100, hsv_destination[2] / 100)

		# hsv_destination = (30/360, hsv_source[1], hsv_source[2])
		# print("hsv_destination", hsv_destination)
		rgb_destination = colorsys.hsv_to_rgb(hsv_destination[0], hsv_destination[1], hsv_destination[2])
		# print("rgb_destination", rgb_destination)
		hex_destination = "#"
		for i in rgb_destination:
			value = hex(round(i * 255)).split("x")[1]
			if len(value) == 1:
				value = "0" + value
			hex_destination += value
		# print("hex_destination", hex_destination)
		return hex_destination + match.group(2)

	return match.group(0)

def convert_rgb(match):
	rgb_source = (int(match.group(1), 16), int(match.group(2), 16), int(match.group(3), 16))
	hsv_source = colorsys.rgb_to_hsv(rgb_source[0]/255, rgb_source[1]/255, rgb_source[2]/255)

	hsv_destination = convert((hsv_source[0] * 360, hsv_source[1] * 100, hsv_source[2] * 100))

	if hsv_destination:
		hsv_destination = (hsv_destination[0] / 360, hsv_destination[1] / 100, hsv_destination[2] / 100)

		# hsv_destination = (30/360, hsv_source[1], hsv_source[2])
		rgb_destination = colorsys.hsv_to_rgb(hsv_destination[0], hsv_destination[1], hsv_destination[2])
		return "rgba(" + str(round(rgb_destination[0] * 255)) + ", " + str(round(rgb_destination[1] * 255)) + ", " + str(round(rgb_destination[2] * 255)) + ", " + match.group(4) + ")"
	
	match.group(0)

# for color in colors:
# 	print(color + colors.get(color))
for file in glob.glob(sys.argv[1] + "/**/*", recursive=True):
	if os.path.isfile(file) and file not in sys.argv:
		try:
			output = ""
			print("File: " + file)
			for index, line in enumerate(open(file, "r").readlines()):
				text = re.sub(hex_pattern, convert_hex, line)
				text = re.sub(hex_pattern_short, convert_hex_short, text)
				text = re.sub(rgba_pattern, convert_rgb, text)
				if re.search(hex_pattern, line) or re.search(rgba_pattern, line):
					print("Line " + str(index) + ": ")
					print(line)
					print(text)
				output += text
			# text = 
			# for color in colors:
			# 	text = text.replace(color, colors.get(color))
			# 	print(text.find(color))
			open(file, "w").write(output)
		except UnicodeDecodeError:
			pass
