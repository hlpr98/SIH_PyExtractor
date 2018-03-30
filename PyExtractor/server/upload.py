from server import models
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os.path

from utilities.zip_extract import zip_extract
from utilities.location import getGPS
from server.models import DEPARTMENTS, Account
from server.forms import UploadForm
from server.views import parse_session
from server import views


# GET request to load template
def upload(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None:
        return authentication_result
    template_data = parse_session(
        request,
        {'form_button':'Upload'}
    )
    if request.method == 'POST' and request.FILES['zip']:
        # TODO : Wrap everything in a new process

            zip = request.FILES['zip']
            fs = FileSystemStorage()

            # To make a subfolder of same name
            foldername = zip.name.split(".")[0]

            # a.zip will be stored in media/a/a.zip
            file = fs.save(os.path.join(foldername,zip.name), zip)
            path = os.path.join("media",file)
            print(file + " stored in " + path)

            # TODO : Extract images from uploaded zip
            dest_path = os.path.join("media",foldername)
            print("Extracted images in " + dest_path)
            zip_extract(path, dest_path)

            # Stores list of metadata for uploaded images 
            # TODO : extend to include other metadata
            metadata = []

            # TODO : Extract Metadata from images
            for file in os.listdir(dest_path):            
                # TODO : Change for other file types
              if(file.find('.jpg')):  
                  gps = getGPS(os.path.join(dest_path,file))
                  metadata.append(gps)
            
            print(metadata)
            form = UploadForm()
            template_data['form'] = form
            template_data['alert_success'] = "Successfully uploaded"
            return render(request, 'upload.html', template_data)
    else:
        form = UploadForm()
    template_data['form'] = form
    return render(request, 'upload.html', template_data) #without context info

#POST request to send zip to server
# def upload(request):
    	
#     # Check if a file is sent
#     if request.method == 'POST' and request.FILES['zip']:
        
#         # TODO : Wrap everything in a new process

#         zip = request.FILES['zip']
#         fs = FileSystemStorage()

#         # To make a subfolder of same name
#         foldername = zip.name.split(".")[0]

#         # a.zip will be stored in media/a/a.zip
#         file = fs.save(os.path.join(foldername,zip.name), zip)
#         path = os.path.join("media",file)
#         print(file + " stored in " + path)

#         # TODO : Extract images from uploaded zip
#         dest_path = os.path.join("media",foldername)
#         print("Extracted images in " + dest_path)
#         zip_extract(path, dest_path)

#         # Stores list of metadata for uploaded images 
#         # TODO : extend to include other metadata
#         metadata = []

#         # TODO : Extract Metadata from images
#         for file in os.listdir(dest_path):            
#             # TODO : Change for other file types
#         	if(file.find('.jpg')):  
#         		gps = getGPS(os.path.join(dest_path,file))
#         		metadata.append(gps)
        
#         print(metadata)

#         return render(request, 'upload.html', {
#             'uploaded_file_url': path
#         })

#     return render(request, 'upload.html')