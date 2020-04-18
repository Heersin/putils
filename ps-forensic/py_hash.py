# Code Based on <python forensic : A workbench of ....>
import time
import sys
import os
import stat
import hashlib
import argparse
import csv

def ParseCommandLine():
	parser = argparse.ArgumentParser('Python file system hashing ..p-fish')

	parser.add_argument('-v','--verbose',help='allows progress messages to be displayed',
		action='store_true')

	# select hash algorithm -- required
	# for multy choices, set a group to order them
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('--md5', help='specifies MD5 algorithm',
		action='store_true')
	group.add_argument('--sha256',help='specifies SHA256 algorithm',
		action='store_true')
	group.add_argument('--sha512',help='specifies SHA512 algorithm',
		action='store_true')

	# select root(source) path -- required
	parser.add_argument('-s','--rootPath', type=ValidateDirectory, required=True,
		help='specify the source path to start traverse')

	# select report(destination) path -- required
	parser.add_argument('-d','--reportPath', type=ValidateDirectory, required=True,
		help='specify the destination path for reporting results')

	# create a global object to hold the valid args
	# which will be available then
	# gl_args -- args pass to this program
	# gl_hashtypes -- hash algorithm type
	
	global gl_args
	global gl_hashtype

	gl_args = parser.parse_args()

	if gl_args.md5:
		gl_hashtype = 'MD5'
	elif gl_args.sha256:
		gl_hashtype = 'SHA256'
	elif gl_args.sha512:
		gl_hashtype = 'SHA512'
	else:
		gl_hashtype = 'Unknown'
		print('Unknown Hash Type Specified')

	DisplayMessage("Command line processed : Successfully")
	return

def WalkPath():

	processCount = 0
	errorCount = 0

	oCSV = _CSVWriter(gl_args.reportPath + 'fileSystemReport.csv',
		gl_hashtype)


	for root, dirs, files in os.walk(gl_args.rootPath):
		for file in files:
			fname = os.path.join(root,file)
			result = HashFile(fname, file, oCSV)

			if result is True:
				processCount += 1
			else:
				errorCount += 1

	oCSV.writerClose()
	return(processCount)

def HashFile(theFile, simpleName, o_result):
	# First 3 if...
	# 	1.Varify the path valid or not
	# 	2.Varify the file is not a symbolic link
	# 	3.Varify the file is really a file
	# 
	# 2 operations need to catch exception
	# 	1.open file as 'rb'
	# 	2.read the file
	# 
	if os.path.exists(theFile):
		if not os.path.islink(theFile):
			if os.path.isfile(theFile):
				try:
					f = open(theFile, 'rb')
				except IOError:
					print('Open Failed:' + theFile)
					return
				else:
					try:
						rd = f.read()
					except IOError:
						f.close()
						print('Read Failed Catched : ' + theFile)
						return
					else:
						theFileStats = os.stat(theFile)
						(mode,ino,dev,nlink,uid,gid,size,atime,mtime,ctime) = os.stat(theFile)

						#process meta data
						DisplayMessage("Processing File: " + theFile)
						filesize = str(size)
						modify_time = time.ctime(mtime)
						access_time = time.ctime(atime)
						create_time = time.ctime(ctime)

						ownerID = str(uid)
						groupID = str(gid)
						fileMode = str(mode)

						#hashing file
						if gl_args.md5:
							hash_alg = hashlib.md5()
						elif gl_args.sha256:
							hash_alg = hashlib.sha256()
						elif gl_args.sha512:
							hash_alg = hashlib.sha512()
						else:
							print('Hash not selected')
							print('===========================')
							f.close()

						hash_alg.update(rd)
						hex_digest = hash_alg.hexdigest()
						hash_value = hex_digest.upper()

						#generate reports
						one_row = (simpleName, theFile,
							filesize,modify_time,access_time,create_time,
							hash_value,ownerID,groupID,fileMode)

						o_result.writeCSVRow(one_row)
						return True
			else:
				print('['+ repr(simpleName) + ', Skipped for not a file]')
				return False
		else:
			print('['+ repr(simpleName) + ", Skipped for it's a link]")
			return False
	else:
		print('['+ repr(simpleName) + ', Skipped for not exsiting]')
		return False

def ValidateDirectory(theDir):
	if not os.path.isdir(theDir):
		raise argparse.ArgumentTypeError('Directory does not exsit')

	if os.access(theDir, os.R_OK):
		return theDir
	else:
		raise argparse.ArgumentTypeError('Directory is not readable')

def ValidateDirectoryWritable(theDir):
	if not os.path.isdir(theDir):
		raise argparse.ArgumentTypeError('Directory does not exsit')

	if os.access(theDir, os.W_OK):
		return theDir
	else:
		raise argparse.ArgumentTypeError('Directory is not writable')

def DisplayMessage(msg):
	if gl_args.verbose:
		print(msg)
	return

class _CSVWriter:
	def __init__(self, filename, hashType):
		try:
			#in python3 csv takes text mode
			self.csvfile = open(filename,'w')
			self.writer = csv.writer(self.csvfile,delimiter=',',quoting=csv.QUOTE_ALL)
			self.head = ('File','Path','Size','Modified Time','Access Time','Created Time',
				'hashType','Owner','Group','Mode')
			self.writer.writerow(self.head)
		except:
			print('CSV File Failure')

	def writeCSVRow(self,single_row):
		self.writer.writerow(single_row)

	def writerClose(self):
		self.csvfile.close()

if __name__ == '__main__':
	PFISH_VER = '1.0'
	#Process Line args
	ParseCommandLine()

	#Record Starting time
	startTime = time.time()

	#Traverse File System
	filesProcessed = WalkPath()


	#Record End time
	endTime = time.time()
	duration = endTime - startTime

	DisplayMessage('Pfish Scan End, Scan Time {} '.format(duration))
	