import sys
import re
import os

# remove all ------ (single is fine) with space
# replace all double or more spaces with just one space
# remove underscores
# remove titles and chapters
# remove new lines 
#	-> controversial. Paragraph separation might be useful? 
#	-> spaCY doesn't seem to have anything for paragraphs though
# add lowercasing? but spaCy probably takes care of that

def is_chapter(line):
	if len(line) >= 2:
		if line[0].lower() == "chapter":
			return True
	return False

def is_volume(line):
	if len(line) == 2:
		if line[0].lower() == "volume":
			return True
	return False

def is_newline(line):
	if len(line) == 0:
		return True
	return False

def clean_novel(filename, subdir):
	with open(filename, 'r+') as openfile:
	# 	print(sys.argv[1])
		# s = openfile.read().replace('\n', ' ')
	# 	s_new = re.sub(' +', ' ', s)
	# 	openfile.seek(0)
	# 	openfile.write(s_new)

		# read in the string
		s = openfile.read()
		lines = s.split('\n')
		lines[:] = [line.split() for line in lines]

		# remove Chapter and Volume titles
		lines[:] = [line for line in lines if not is_chapter(line)]
		lines[:] = [line for line in lines if not is_volume(line)]
		
		# get rid of consecutive new lines
		for i, line in enumerate(lines):
			if is_newline(line):
				flag = True
				while flag:
					if i+1 < len(lines) and is_newline(lines[i+1]):
						lines.remove(lines[i+1])
					else:
						line.append('\n')
						flag = False

		# # rejoin everything 
		lines[:] = [' '.join(line) for line in lines]
		new = ' '.join(lines).strip()
		new = new.replace(' \n ', '\n')
		new = re.sub('[-]-+', ' ', new) 	# removes >= 2 -
		new = re.sub('[_*]', '', new)		# removes _
		new = re.sub(' +', ' ', new)		# condenses spaces

		# write to new file
		folder =  os.path.basename(subdir)
		fn = os.path.basename(filename)
		new_filename = "PROCESSED" + "/" + folder + "/" + fn
		out = open(new_filename, 'w')
		# out = open("output.txt", 'w')
		out.write(new)

		# write back to file
		# openfile.seek(0)
		# openfile.write(new)

# clean_novel()

rootdir = sys.argv[1]
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file[0] != '.':
			filename = os.path.join(subdir, file)
			clean_novel(filename, subdir)




