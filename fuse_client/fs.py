#!/usr/bin/env python

import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations
from Passthrough import Passthrough
import requests
import json

from variables import variables
import shutil
import crypt
import db


class dfs(Passthrough):
    def __init__(self, root, fallbackPath, username, secret):

        dbms = db.db_connect(username=username, password=secret)
        tokens = dbms.get_all_tokens()

        keys, paths = dbms.get_all_keys()
        if not keys:
            key = crypt.gen_sym_key_from_password(secret)
            print(key)
            print(key.decode())
            dbms.insert_key(key.decode(), '/')
            keys.append(key.decode())
            paths.append('/')

        self.root = root
        self.fallbackPath = fallbackPath
        self.token = tokens
        self.keys = keys
        self.paths = paths

        print('KEYS AND PATHS: ' + str(self.keys) + str(self.paths))

        url = variables['server'] + '/v1/listFolders'
        header = {'Authorization': 'Token ' + self.token}
        r = requests.get(url, headers=header).content
        req = json.loads(r.decode('utf-8'))
        print(req)
        for folders in req:
            os.makedirs('/tmp/.tmp_fuse/' + folders)

        ##############################################################
        url = variables['server'] + '/v1/listFiles'
        header = {'Authorization': 'Token ' + self.token}
        r = requests.get(url, headers=header).content
        req = json.loads(r.decode('utf-8'))
        print(req)
        for files in req:
            print('creating file: ' + root + files)
            try:
                f = open(root + files, "w+")
                f.close()
            except Exception as e:
                print(e)
        ###############################################################
            url = variables['server'] + '/v1/downloadFile'
            values = {'name': files}
            header = {'Authorization': 'Token ' + self.token}

            r = requests.get(url, headers=header, data=values)
            #print(str(r.content))
            decoded_string = crypt.decode_with_password(r.content.decode(), self.keys[0])  # ROOT KEY
            f = open(self.root + files, 'w')
            f.write(decoded_string.decode('utf-8') )  # (decode("utf-8"))
            f.close()

    # Helpers
    # =======
    def _full_path(self, partial, useFallBack=False):
        if partial.startswith("/"):
            partial = partial[1:]
        # Find out the real path. If has been requesetd for a fallback path,
        # use it
        path = primaryPath = os.path.join(
            self.fallbackPath if useFallBack else self.root, partial)
        # If the pah does not exists and we haven't been asked for the fallback path
        # try to look on the fallback filessytem
        if not os.path.exists(primaryPath) and not useFallBack:
            path = fallbackPath = os.path.join(self.fallbackPath, partial)
            # If the path does not exists neither in the fallback fielsysem
            # it's likely to be a write operation, so use the primary
            # filesystem... unless the path to get the file exists in the
            # fallbackFS!
            if not os.path.exists(fallbackPath):
                # This is probabily a write operation, so prefer to use the
                # primary path either if the directory of the path exists in the
                # primary FS or not exists in the fallback FS
                primaryDir = os.path.dirname(primaryPath)
                fallbackDir = os.path.dirname(fallbackPath)
                if os.path.exists(primaryDir) or not os.path.exists(fallbackDir):
                    path = primaryPath
        return path
      
    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                                                        'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid', 'st_blocks')) 

    def readdir(self, path, fh):
        dirents = ['.', '..']
        """
        full_path = self._full_path(path)
        # print("listing " + full_path)
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        if self.fallbackPath not in full_path:
            full_path = self._full_path(path, useFallBack=True)
            # print("listing_ext " + full_path)
            if os.path.isdir(full_path):
                dirents.extend(os.listdir(full_path))
        """
        print ("ls for " + str(path[1:]))
        url = variables['server'] + '/v1/listFiles'
        header = {'Authorization': 'Token ' + self.token}
        r = requests.get(url, headers=header).content
        req = json.loads(r.decode('utf-8'))
        print(req)

        for files in req:
            print ("path: " + str(path[1:]))
            print ('files: ' + files)
            if path[1:] == "":
                print ("ROOT")
                dirents.append(files)
            elif files.startswith(str(path[1:])):
                print ("NOT ROOT")
                dirents.append(files)
            else:
                print("NOT OK")

        url = variables['server'] + '/v1/listFolders'
        header = {'Authorization': 'Token ' + self.token}
        r = requests.get(url, headers=header).content
        req = json.loads(r.decode('utf-8'))
        print(req)

        for folders in req:
            if path[1:] == "":
                dirents.append(folders)
            elif folders.startswith(str(path[1:])):
                dirents.append(folders[1:])

        #for i in range(0,len(req['metadata']['contents'])):
        #    dirents.append(req['metadata']['contents'][i]['name'])
        #print("Dirents: " + str(dirents))

        print ("LS : " + str(list(set(dirents))))

        for r in list(set(dirents)):
            yield r

    def create(self, path, mode, fi=None):
        print("Create file:  -> " + path)
        f = open(self.root + path[1:], "w+")
        f.close()
        url = variables['server'] + '/v1/fileupload'
        print(url)
        ## ENCRYPT FILE
        f = open(self.root + path[1:], 'rb')
        encoded_file = crypt.encode_with_password(f.read(), self.keys[0])
        ###################
        files = {'upload_file': encoded_file}
        values = {'name': path[1:]}
        header = {'Authorization': 'Token ' + self.token}
        print('OK')
        r = requests.post(url, files=files, headers=header, data=values)
        print(r.content)
        super().create(path,mode, fi=None)


    def mkdir(self, path, mode):
        print("Create folder: " + path)
        url = variables['server'] + '/v1/uploadFolder'
        values = {'name': path}
        header = {'Authorization': 'Token ' + self.token}

        r = requests.post(url, headers=header, data=values)
        print(r.content)
        print('OK')
        super().mkdir(path, mode)

    def rmdir(self, path):
        print("Remove folder: " + path)
        url = variables['server'] + '/v1/deleteFolder'
        values = {'name': path}
        header = {'Authorization': 'Token ' + self.token}

        r = requests.post(url, headers=header, data=values)
        print(r.content)

        super().rmdir(path)

    def rename(self, old, new):
        print('Old name: ' + old)
        print('New name: ' + new)


        url = variables['server'] + '/v1/renameFolder'
        values = {'name': new, 'old_name': old}
        header = {'Authorization': 'Token ' + self.token}

        r = requests.post(url, headers=header, data=values)
        print(r.content)

        if r.status_code == 400:
            print("Rename file")
            url = variables['server'] + '/v1/renameFile'
            values = {'name': new[1:], 'old_name': old[1:]}
            header = {'Authorization': 'Token ' + self.token}

            r = requests.post(url, headers=header, data=values)
            print(r.content)

        super().rename(old,new)

    def release(self, path, fh):
        print ("Release/close file overwrite")

        url = variables['server'] + '/v1/deleteFile'
        values = {'name': path[1:]}
        header = {'Authorization': 'Token ' + self.token}

        r = requests.post(url, headers=header, data=values)
        print(r.content)


        url = variables['server'] + '/v1/fileupload'
        print(url)
        ## ENCRYPT FILE
        f = open(self.root + path[1:], 'rb')
        encoded_file = crypt.encode_with_password(f.read(), self.keys[0])
        ###################
        files = {'upload_file': encoded_file}
        values = {'name': path[1:]}
        header = {'Authorization': 'Token ' + self.token}
        r = requests.post(url, files=files, headers=header, data=values)
        print(r.content)

        return os.close(fh)

    def unlink(self, path):
        print("Unlink overwrite: " + self.root + path[1:])

        url = variables['server'] + '/v1/deleteFile'
        values = {'name': path[1:]}
        header = {'Authorization': 'Token ' + self.token}

        r = requests.post(url, headers=header, data=values)
        print(r.content)

        os.remove(self.root + path[1:])
        super().unlink(path)


"""
def main(mountpoint, token):
    FUSE(dfs(token), mountpoint, nothreads=True,
         foreground=True, **{'allow_other': True, 'nonempty': True})

"""
def main(mountpoint, username, secret):
    if not os.path.exists('/tmp/.tmp_fuse/'):
        print ('tmp_fuse not exist')
        os.makedirs('/tmp/.tmp_fuse/')
    else:
        print('tmp_fuse exists')
        for the_file in os.listdir('/tmp/.tmp_fuse/'):
            file_path = os.path.join('/tmp/.tmp_fuse/', the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    root = '/tmp/.tmp_fuse/'
    fallbackPath = '/tmp/.tmp_fuse/'

    FUSE(dfs(root, fallbackPath, username, secret), mountpoint, nothreads=True,
         foreground=True, **{'allow_other': True, 'nonempty': True})

"""
if __name__ == '__main__':
    mountpoint = sys.argv[3]
    root = sys.argv[1]
    fallbackPath = sys.argv[2]
    main(mountpoint, root, fallbackPath)
"""