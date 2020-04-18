# Code Based on <python forensic : A workbench of ....>
import time
import os
import sys
import argparse
# ============================= Some Utils ==============================================
global gl_args
MIN_WORD = 5
MAX_WORD = 15
PREDECESSOR_SIZE = 32
WINDOW_SIZE = 128

def ValidateFileRead(theFile):
	if not os.path.exists(theFile):
		raise argparse.ArgumentTypeError('File Does not Exist')

	if os.access(theFile, os.R_OK):
		return theFile
	else:
		raise argparse.ArgumentTypeError('File is not readable')

def DisplayMessage(msg):
	if gl_args.verbose:
		print(msg)

	return

def PrintHeading():
	print("Offset    00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F        			ASCII")
	print("--------------------------------------------------------------------------")

	return

def PrintBuffer(word,direct_offset,buff,offset, hexSize):
	print("Found: " + word + " At address: ")
	print("%08x      " %(direct_offset), end='')

	PrintHeading()
	# display column
	column = 16
	buff_len = len(buff)
	remain_len = buff_len - direct_offset

	if remain_len < hexSize:
		display_size = remain_len
	else:
		display_size = hexSize

	new_buff = []
	for ele in buff:
		new_buff.append(ele)
	
	need_pad = remain_len % 16
	for i in range(need_pad):
		new_buff.append(0x00)
	

	for i in range(direct_offset, direct_offset + display_size, column):
		#Raw Part
		for j in range(0,column):
			if(j == 0):
				byte_value = new_buff[i + j]
				print("%08x 		%02X " %(i, byte_value), end='')
			else:
				byte_value = new_buff[i + j]
				print("%02x " %byte_value, end='')
		print("		", end='')

		# ASCII part
		for j in range(0,column):
			byte_value = new_buff[i + j]
			if(byte_value >= 0x20 and byte_value <= 0x7f):
				print("%c" %byte_value,end='')
			else:
				print(".",end='')

		print("")
	return

def PrintAllWordsFound(wordList):
	print("Index of All Words")
	print("----------------------")

	wordList.sort()

	for entry in wordList:
		print(entry)
	print("----------------------")
	print("")
	return

class class_Matrix:
	weighted_matrix = set()

	def __init__(self):
		try:
			fileTheMatrix = open(gl_args.matrix,'rb')
			for line in fileTheMatrix:
				value = line.strip()
				self.weighted_matrix.add(int(value,16))
		except:
			print("Matrix File Error:" + gl_args.theMatrix)
			sys.exit()
		finally:
			fileTheMatrix.close()

		return

	def isWordProbable(self,theWord):
		if(len(theWord) < MIN_WORD):
			return False
		else:
			BASE = 96
			word_weight = 0

			# calculate weight
			for i in range(4,0,-1):
				char_value = (ord(theWord[i]) - BASE)
				shift_value = (i-1) * 8
				char_weight = char_value << shift_value
				word_weight = (word_weight | char_weight)

			if(word_weight in self.weighted_matrix):
				return True
			else:
				return False



# ========================= Search ==================================================
def SearchWords():
	black_words_set=set()
	cmd_args = gl_args

	# get blacklist keywords to search 
	try:
		fileWords = open(cmd_args.keyWords)
		for line in fileWords:
			black_words_set.add(line.strip())
	except:
		print('Keywords File Failure:' + cmd_args.keyWords)
		sys.exit()
	finally:
		fileWords.close()


	# get target file for search
	try:
		targetFile = open(cmd_args.srchTarget,'rb')
		target_bytes_array = bytearray(targetFile.read())
	except:
		sys.exit()
	finally:
		targetFile.close()
	target_size = len(target_bytes_array)


	#prepare for next step
	target_bytes_array_copy = target_bytes_array
	if cmd_args.matrix:
		word_check_matrix = class_Matrix()


	#--------Search main body--------------

	# search loop
	# replace non chars with zero's
	for i in range(0,target_size):
		character = chr(target_bytes_array[i])
		if not character.isalpha():
			target_bytes_array[i] = 0

	# 1.create an empty list of probable not found items' index
	# extract possible words from bytearray
	# then inspect search word list
	# 
	
	index_of_words = []
	
	cnt = 0
	print("Target-size " + str(target_size))
	for i in range(0,target_size):
		character = chr(target_bytes_array[i])
		if character.isalpha():
			cnt += 1
		else:
			if(cnt >= MIN_WORD and cnt <= MAX_WORD):
				cur_word = ""
				for z in range(i - cnt, i):
					cur_word = cur_word + chr(target_bytes_array[z])
				cur_word = cur_word.lower()

				if(cur_word in black_words_set):
					PrintBuffer(cur_word,i - cnt,target_bytes_array_copy,
						i - PREDECESSOR_SIZE, WINDOW_SIZE)
					index_of_words.append([cur_word,i - cnt])
					cnt = 0
					print("")
				else:
					if cmd_args.matrix and word_check_matrix.isWordProbable(cur_word):
						index_of_words.append([cur_word,i - cnt])
					cnt = 0
			else:
				cnt = 0

	PrintAllWordsFound(index_of_words)
	return

# ========================= CMD ===============================
def ParseCommandLine():
	parser = argparse.ArgumentParser('Python Search')

	parser.add_argument('-v','--verbose',help='enable printing addtional infos',
		action='store_true')
	parser.add_argument('-k','--keyWords',type=ValidateFileRead,
		required=True,help='Specify keywords to search')
	parser.add_argument('-t','--srchTarget',type=ValidateFileRead,
		required=True,help='Specify target file to search')
	parser.add_argument('-m','--matrix',type=ValidateFileRead,
		required=False,help="Specify the weighted matrix file--support similar word search")

	gl_args = parser.parse_args()

	DisplayMessage('Command Line Processed : Successfully')
	return


if __name__ == '__main__':
    PSEARCH_VERSION = '1.0'
    ParseCommandLine()
    start_time = time.time()
    SearchWords()
    
    end_time = time.time()
    duration = end_time - start_time
    print("Search Time : {}".format(duration))
