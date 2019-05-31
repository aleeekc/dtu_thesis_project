import pyminizip

def create_zip(srcfile, path, password):
	pyminizip.compress("/srcfile/path.txt", "file_path_prefix", "file.zip", "1233", 4)
	#pyminizip.compress("/srcfile/path.txt", "file_path_prefix", "/distfile/path.zip", "password", int(compress_level))

if __name__ == "__main__":
    main()