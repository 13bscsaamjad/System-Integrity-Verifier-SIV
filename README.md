# System-Integrity-Verifier-SIV

1 INTRODUCTION
System Integrity Verifier (SIV) enables to verify the integrity of the specified directory tree. The goal of the SIV is to detect file system modifications occurring within a directory tree. The SIV outputs statistics and warnings about changes to a report file specified by the user. The primary usage of the SIV includes the ability to verify the integrity of the specified directory tree. Moreover, it tracks other proprietary changes within the files that can enable wide monitoring too. For example, it shows the statistics regarding the files that have been removed and all those files that have been added too. This can allow to track if any vital file have been removed. Or the files that have been added are supposed to be added at the specific tree point or not. It also detects the size changes and the specified digests. Another feature is that it also portrays the owner user and the owner group. This can enable the authorization monitoring to see if the specific file is under control of the valid user or group in the system. The access rights to the files are also tracked using the SIV and that is also an extension of ensuring authorization. Lastly it also keeps track of the last modified time of specific files. That could enable to track what users could be using the system and have potentially made a change at the time when the modification is made to the file.

2 DESIGN AND IMPLEMENTATION
The program is implemented in Python3. The reason for choosing Python3 is that under its standard installation, it comes with very usable libraries to manipulate and implement different requirements and specifications of the desired SIV. To run the program, we only need Python3 installed and configured. 

When the program runs it checks if the monitored directory exists or not. If it doesn’t exist, the program displays the error and terminates. Similarly, it checks that if the verification and report file supplied exists within the directory tree of the given monitored directory using parents method under the pathlib library. If they do exist, the program displays the error and quits. It also checks if the hash function is supported or not and if it is not it displays the error and quits. Lastly it checks if the verification file also exists and then if it does, it asks if the user wants to overwrite the existing verification file. If user type yes, the program will continue otherwise it will end.
2.1 Command Line Arguments
The command line arguments are handled using Python3 library argparse. The mutually exclusive groups required for the implementation of the program are handled through this library. For example, you can only specify hash function using (–H) flag when you are running the program in initialization mode using flag (–i). Similarly, you cannot provide hash function (–H) in the verification mode.
2.2 Iterative Directory Search
For iterative directory search to list all files and directories within the specified directory, the newly python3 module pathlib is used. Using glob method within pathlib, iterative search is performed on the monitored directory provided which lists all the files and directories that exists in the directory tree.

2.2.1 Size. The size of the file/directory is obtained using stat method’s st_size property on the path.
2.2.2 Owner. The owner of the file/directory is obtained using owner method within the pathlib module on the path.
2.2.3 Group.  The group of the file/directory is obtained using group method within the pathlib module on the path.
2.2.4 Permissions. The permissions of the file/directory are obtained using stat method’s st_mode property under pathlib module on the path.
2.2.5 Last Modification Time. The last modification time of the file/directory is obtained using stat method’s st_mtime property on the path.
2.2.6 Hash. The hash is calculated using hashlib module under Python3. The file is opened in the binary mode and the stream is passed to calculate the digest in the specified function “md5” or “sha1”. This is only calculated for files and skipped for directories.
2.3 Verification File Format
The data is stored in the verification file in JSON format. The path to the file converted into string is stored as the key whereas the all other five parameters are yet stored as key value pairs within the dictionary object as a value to the file-path key.

The keys within the dictionary object are owner, group, perm (permissions), mtime (last modified time) and hashfunc (md5 or sha1). The values to these keys are actual values obtained as explained in 2.2.
2.4 Change Detection
The initialization mode iteratively searches the files/directories and compute the required parameters as explained and store them in the JSON format as explained earlier. The verification mode gets the JSON data from the verification file and store it internally. It then starts to parse iteratively the monitored directory and find the changes as follows.
ALGORITHM: Verification
start_time  now
scan_path  path_to_monitored_directory if exist
verification_data  path_to_verification_file if exist and not in scan_path tree
hash_function  get from verification_data
report_file  path_to_report_file if exist and not in scan_path tree
directories  0
files  0
warnings  0
initialize 
files_added
files_removed
files_different_size
files_different_hash
files_different_owner
files_different_group
files_different_rights
files_different_date
to empty lists




for each path in scan_path, do
	if path is a file
		increase files by one
		find owner, group, size, rights, last modification and hash
	end
	if path is a directory
		increase directories by one
		find owner, group, size, rights and last modification	
	end
if path in verification_data
	compare owner, group, size, rights, last modification and hash
	add path to respective list if not same
	delete path from verification_data
end
if path not in verification_data
	add path in files_added list
end
for each path in verification_data, do
	add path in files_removed
end

end

3 USAGE
The program can be run in initialization mode, verification mode or help mode. For running the program in help mode specify the help flag (-h) as follows:

python3 siv.py -h 
3.1 Initialization Mode
The command format to run the program in initialization mode is as follows:

python3 siv.py –i –D monitored_directory –V verification_data –R report_file –H sha1

The hash functions supported are sha1 and md5 so you can only provide sha1 or md5 after –H flag.
3.2 Verification Mode
The command format to run the program in verification mode is as follows:

python3 siv.py –v –D monitored_directory –V verification_data –R report_file


4 LIMITATIONS
The program reads the files in the binary mode. For files, it finds all the required parameters and store or compare them. But for directories, it skips the hash but not the other parameters. The hash functions supported are only md5 and sha1.
