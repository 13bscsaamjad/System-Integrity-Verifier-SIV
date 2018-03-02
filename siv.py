import os
import pathlib
import hashlib
import sys
import os
import pwd
import datetime
import json
import time
import argparse


def initialize(mdir, vfile, rfile, hfunc):
	starttime = time.time()
	mondir = pathlib.Path(mdir)
	verfile = pathlib.Path(vfile)
	repfile = pathlib.Path(rfile)
	hashfunc = str(hfunc)
	dircount = 0
	filecount = 0
	
	if not mondir.is_dir():
		print("Monitored directory does not exists!")
		sys.exit()

	if mondir in verfile.parents or mondir in repfile.parents:
		print ("The Verification file or Report File is in the Monitored directory! Exiting!")
		sys.exit()

	if hashfunc != "sha1" and hashfunc != "md5":
		print ("Hash function not supported! Exiting!")
		sys.exit()

	if verfile.exists():
		opt = input("Verification File already exists! Do you want to overwrite? (yes/no): ")
		if opt != "yes" and opt != "no":
			print ("Option not correct! Exiting!")
		elif opt == "no":
			sys.exit()
	
	data = {}
	
	for x in mondir.glob('**/*'):
		if not x.is_dir():
			filecount = filecount + 1
			if hashfunc == "md5":
				mhash = hashlib.md5(x.open("rb").read()).hexdigest()
			else:
				mhash = hashlib.sha1(x.open("rb").read()).hexdigest()
			
			data[str(x)] = {"owner" : x.owner(), "group" :  x.group(), "size" : x.stat().st_size, "perm" : x.stat().st_mode, "mtime" : x.stat().st_mtime, hashfunc : mhash}
		
		else:
			data[str(x)] = {"owner" : x.owner(), "group" :  x.group(), "size" : x.stat().st_size, "perm" : x.stat().st_mode, "mtime" : x.stat().st_mtime, hashfunc : "N/A"}
			dircount = dircount + 1
	
	with verfile.open("w") as jsonfile:
		json.dump(data, jsonfile)

	fwriter = repfile.open("w")
	fwriter.write("Path to Monitored Directory: " + str(mondir) + "\n")
	fwriter.write("Path to Verification File: " + str(verfile) + "\n")
	fwriter.write("Number of directories parsed: " + str(dircount) + "\n")
	fwriter.write("Number of files parsed: " + str(filecount) + "\n")
	fwriter.write("Time to complete the initialization mode: " + str(time.time()-starttime) + " seconds.")

def verify(mdir, vfile, rfile):
	starttime = time.time()
	mondir = pathlib.Path(mdir)
	verfile = pathlib.Path(vfile)
	repfile = pathlib.Path(rfile)
	dircount = 0
	filecount = 0
	warncount = 0
	new = []
	removed = []
	sizediff = []
	hashdiff = []
	userdiff = []
	groupdiff = []
	accrightdiff = []
	moddatediff = []
	
	
	if not verfile.exists():
		print ("Verification File does not exists! Exiting!")
		sys.exit()
	
	if not mondir.is_dir():
		print("Monitored directory does not exists! Exiting!")
		sys.exit()

	if mondir in verfile.parents or mondir in repfile.parents:
		print ("The Verification file or Report File is in the Monitored directory! Exiting!")
		sys.exit()
	
	data = json.load(verfile.open())
	hashfunc = ""
	
	for entry in data:
		desc = data.get(entry)
		break

	for entry in desc:
		if entry == "md5":
			hashfunc = "md5"
			break
		if entry == "sha1":
			hashfunc = "sha1"
			break
	
	for x in mondir.glob('**/*'):
		if not x.is_dir():
			filecount = filecount + 1
			if hashfunc == "md5":
				mhash = hashlib.md5(x.open("rb").read()).hexdigest()
			else:
				mhash = hashlib.sha1(x.open("rb").read()).hexdigest()
			if str(x) in data:
				if data[str(x)]["owner"] != x.owner():
					warncount = warncount + 1
					userdiff.append(str(x))
				if data[str(x)]["group"] != x.group():
					warncount = warncount + 1
					groupdiff.append(str(x))
				if data[str(x)]["size"] != x.stat().st_size:
					warncount = warncount + 1
					sizediff.append(str(x))
				if data[str(x)]["perm"] != x.stat().st_mode:
					warncount = warncount + 1
					accrightdiff.append(str(x))
				if data[str(x)]["mtime"] != x.stat().st_mtime:
					warncount = warncount + 1
					moddatediff.append(str(x))
				if data[str(x)][hashfunc] != mhash:
					warncount = warncount + 1
					hashdiff.append(str(x))
				del data[str(x)]
			else:
				warncount = warncount + 1
				new.append(str(x))

		else:
			dircount = dircount + 1
			if str(x) in data:
				if data[str(x)]["owner"] != x.owner():
					warncount = warncount + 1
					userdiff.append(str(x))
				if data[str(x)]["group"] != x.group():
					warncount = warncount + 1
					groupdiff.append(str(x))
				if data[str(x)]["size"] != x.stat().st_size:
					warncount = warncount + 1
					sizediff.append(str(x))
				if data[str(x)]["perm"] != x.stat().st_mode:
					warncount = warncount + 1
					accrightdiff.append(str(x))
				if data[str(x)]["mtime"] != x.stat().st_mtime:
					warncount = warncount + 1
					moddatediff.append(str(x))
				del data[str(x)]
			else:
				warncount = warncount + 1
				new.append(str(x))
	for item in data:
		warncount = warncount + 1
		removed.append(item)


	fwriter = repfile.open("w")
	fwriter.write("Path to Monitored Directory: " + str(mondir) + "\n")
	fwriter.write("Path to Verification File: " + str(verfile) + "\n")
	fwriter.write("Path to Report File: " + str(repfile) + "\n")
	fwriter.write("Number of directories parsed: " + str(dircount) + "\n")
	fwriter.write("Number of files parsed: " + str(filecount) + "\n")
	fwriter.write("Number of warnings issued: " + str(warncount) + "\n")
	fwriter.write("Time to complete the verification mode: " + str(time.time()-starttime) + " seconds\n")
	fwriter.write("**************************************************************************\n")
	fwriter.write("New Files/Directories:\n")
	if len(new) > 0:
		for item in new:
			fwriter.write(item + "\n")
	else:
		fwriter.write("None\n")
	fwriter.write("Removed Files/Directories:\n")
	if len(removed) > 0:
		for item in removed:
			fwriter.write(item + "\n")
	else:
		fwriter.write("None\n")
	fwriter.write("Files/Directories with different size:\n")
	if len(sizediff) > 0:
		for item in sizediff:
			fwriter.write(item + "\n")
	else:
		fwriter.write("None\n")
	fwriter.write("Files with different hash:\n")
	if len(hashdiff) > 0:
		for item in hashdiff:
			fwriter.write(item + "\n")
	else:
		fwriter.write("None\n")
	fwriter.write("Files/Directories with different user:\n")
	if len(userdiff) > 0:
		for item in userdiff:
			fwriter.write(item + "\n")
	else:
		fwriter.write("None\n")
	fwriter.write("Files/Directories with different group:\n")
	if len(groupdiff) > 0:
		for item in groupdiff:
			fwriter.write(item + "\n")
	else:
		fwriter.write("None\n")
	fwriter.write("Files/Directories with different access rights:\n")
	if len(accrightdiff) > 0:
		for item in accrightdiff:
			fwriter.write(item + "\n")
	else:
		fwriter.write("None\n")
	fwriter.write("Files/Directories with different modification date:\n")
	if len(moddatediff) > 0:
		for item in moddatediff:
			fwriter.write(item + "\n")
	else:
		fwriter.write("None\n")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(conflict_handler="resolve")
	group1 = parser.add_mutually_exclusive_group()
	group1.add_argument("-i", help="initialization mode", action="store_true")
	group1.add_argument("-v", help="verification mode", action="store_true")
	parser.add_argument("-D", help="path to monitored directory", required=True)
	parser.add_argument("-V", help="path to verification file", required=True)
	parser.add_argument("-R", help="path to report file", required=True)
	parser.add_argument("-H", help="hash function; accepted values are md5 or sha1")
	args = parser.parse_args()
	if args.v and args.H:
		parser.error("-H hash function can only be provided in the initialization mode")
	if args.i and not args.H:
		parser.error("-i initialization mode requires -H hash function")
	if args.i and args.D and args.V and args.R and args.H:
		initialize(args.D, args. V, args.R, args.H)
	if args.v and args.D and args.V and args.R:
		verify(args.D, args.V, args.R)
