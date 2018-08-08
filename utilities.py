from shutil import make_archive

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
from google.colab import files

# Authentication
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)


def upload_folder(folder_id, folder):
    """Zips and uploads folder to the specified folder-id
       
       inputs:
           folder_id: folder in drive to which upload folder
           folder: folder to zip and upload
    """
    make_archive(f'{folder}_zip', 'zip', folder)
    upload_file(folder_id, f'{folder}_zip.zip')
    
def upload_file(folder_id, content_file):
    """Uploads file to the specified folder Id
       
       inputs: 
           folder_id: Id of folder to which upload file (string)
           content_file: Path of file to upload (string)
    """
    
    file = drive.CreateFile({'parents':[{'kind': 'drive#fileLink', 'id': folder_id}]})
    file.SetContentFile(content_file)
    file.Upload()
    print('File succesfully uploaded')
    
def list_files(folder_id):
    """List files in folder
       
       inputs:
           folder_id: folder to list files
    """
  
    file_list = drive.ListFile({'q': f" {folder_id} in parents and trashed=false"}).GetList()
    for file in file_list:
        print(f"name: {file['title']}, Id: {file['id']}")

def download_file(file, folder=False):
    """Downloads specified file
       
       inputs:
           file: path of file to download
           folder: if True zips and downloads folder
    """
    if folder:
        filename = f'{file}_zip.zip'
        make_archive(filename, 'zip', file)
        files.download(filename)
    else:
        files.download(file)

def get_file(file_id, filename):
    """Import file from drive
       
       inputs:
           file_id: Id of file to import
           filename: name given to imported file, whole name with suffix
    """
    
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(filename)
