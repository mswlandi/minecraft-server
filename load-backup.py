# -*- coding: utf-8 -*-

"""
    Upload folder to Google Drive
"""

# Import Google libraries
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFileList
import googleapiclient.errors

# Import general libraries
from sys import exit
import ast
import shutil
import os


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


def download_file(drive, folder_id, filename):
    """ 
		Downloads a specific file from Google Drive
	"""
    print(f'downloading {filename}')
    download_file_id = get_folder_file_id(drive, folder_id, filename)
    download_file = drive.CreateFile({'id': f'{download_file_id}'})
    download_file.GetContentFile(filename)


def main():
    world_name = "Bedrock level"
    dst_folder_name = f"server/worlds/{world_name}"
    # dst_folder_name = f"C:/Users/asst/Downloads/server/worlds/{world_name}"
    backup_folder_name = "minecraft-backups"

    # Authenticate to Google API
    drive = authenticate()
    backup_folder_id = get_folder_file_id(drive, 'root', backup_folder_name)

    # Create the folder if it doesn't exist
    if not backup_folder_id:
        print(f'{backup_folder_name} folder does not exist in drive')
        exit(1)
    
    download_file(drive, backup_folder_id, f"{world_name}.zip")
    shutil.unpack_archive(f"{world_name}.zip", dst_folder_name)
    os.remove(f"{world_name}.zip")


if __name__ == "__main__":
    main()