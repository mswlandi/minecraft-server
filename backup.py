# -*- coding: utf-8 -*-

"""
    Upload folder to Google Drive
"""

# Enable Python3 compatibility
from __future__ import (unicode_literals, absolute_import, print_function,
                        division)
from turtle import back

# Import Google libraries
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFileList
import googleapiclient.errors

# Import general libraries
from os import chdir, listdir, stat, remove
from sys import exit
import ast
import shutil
from datetime import datetime
from functools import reduce


def authenticate():
    """ 
		Authenticate to Google API
	"""

    gauth = GoogleAuth()

    return GoogleDrive(gauth)


def get_folder_file_id(drive, parent_folder_id, folder_name):
    """ 
		Check if destination folder exists and return it's ID
	"""

    # Auto-iterate through all files in the parent folder.
    file_list = GoogleDriveFileList()
    try:
        file_list = drive.ListFile({'q': "'{0}' in parents and trashed=false".format(parent_folder_id)}).GetList()
	# Exit if the parent folder doesn't exist
    except googleapiclient.errors.HttpError as err:
		# Parse error message
        message = ast.literal_eval(err.content)['error']['message']
        if message == 'File not found: ':
            print(message + folder_name)
            exit(1)
		# Exit with stacktrace in case of other error
        else:
            raise

	# Find the the destination folder in the parent folder's files
    for file1 in file_list:
        if file1['title'] == folder_name:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
            return file1['id']


def create_folder(drive, folder_name, parent_folder_id):
    """ 
		Create folder on Google Drive
	"""
    
    folder_metadata = {
        'title': folder_name,
        # Define the file type as folder
        'mimeType': 'application/vnd.google-apps.folder',
        # ID of the parent folder        
        'parents': [{"kind": "drive#fileLink", "id": parent_folder_id}]
    }

    folder = drive.CreateFile(folder_metadata)
    folder.Upload()

    # Return folder informations
    print(f"title: {folder['title']}, id: {folder['id']}")
    return folder['id']


def upload_files(drive, folder_id, src_folder_name):
    """ 
		Upload files in the local folder to Google Drive 
	"""

	# Enter the source folder
    try:
        chdir(src_folder_name)
	# Print error if source folder doesn't exist
    except OSError:
        print(src_folder_name + 'is missing')
	# Auto-iterate through all files in the folder.
    for file1 in listdir('.'):
		# Check the file's size
        statinfo = stat(file1)
        if statinfo.st_size > 0:
            print('uploading ' + file1)
            # Upload file to folder.
            f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}]})
            f.SetContentFile(file1)
            f.Upload()
		# Skip the file if it's empty
        else:
            print('file {0} is empty'.format(file1))


def upload_file(drive, folder_id, filename):
    """ 
		Upload a specific file to Google Drive
	"""

    # Check the file's size
    statinfo = stat(filename)
    if statinfo.st_size > 0:
        print('uploading ' + filename)
        # Upload file to folder.
        f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}]})
        f.SetContentFile(filename)
        f.Upload()
    # Skip the file if it's empty
    else:
        print(f'file {filename} is empty')


def delete_file(drive, folder_id, filename):
    """ 
		Deletes a specific file from Google Drive
	"""
    print(f'deleting {filename}')
    delete_file_id = get_folder_file_id(drive, folder_id, filename)
    delete_file = drive.CreateFile({'id': f'{delete_file_id}'})
    delete_file.Delete()


def get_file_list(drive, folder_id):
    """ 
		Returns the list of file names in a certain folder in Google Drive
	"""
    # Auto-iterate through all files in the parent folder.
    file_list = GoogleDriveFileList()
    file_list = drive.ListFile({'q': "'{0}' in parents and trashed=false".format(folder_id)}).GetList()

    file_name_list = [file['title'] for file in file_list]
    return file_name_list


def main():
    world_name = "Bedrock level"
    src_folder_name = f"~/server/worlds/{world_name}"
    # src_folder_name = "C:/Users/asst/Downloads/server/worlds/test"
    backup_folder_name = "minecraft-backups"
    zip_file_name = f"world_backup_{datetime.now().strftime('%Y%m%d')}"

    # compresses the world to upload
    shutil.make_archive(zip_file_name, 'zip', src_folder_name)

    # Authenticate to Google API
    drive = authenticate()
    backup_folder_id = get_folder_file_id(drive, 'root', backup_folder_name)

    # Create the folder if it doesn't exist
    if not backup_folder_id:
        print(f'{backup_folder_name} folder does not exist in drive')
        exit(1)

    # get the list of backup file names
    backups_filenames = []
    for filename in get_file_list(drive, backup_folder_id):
        if filename.startswith("world_backup_"):
            backups_filenames.append(filename)
    
    # deletes the oldest backup if exceedes the number of saved backups
    if len(backups_filenames) > 5:
        backups_filenames.sort()
        file_to_delete = backups_filenames[0]
        delete_file(drive, backup_folder_id, file_to_delete)

    # Upload the backup
    upload_file(drive, backup_folder_id, f'{zip_file_name}.zip')
    remove(f'{zip_file_name}.zip')


if __name__ == "__main__":
    main()