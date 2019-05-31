from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from .views import *

app_name = 'backend'

urlpatterns = [
    path('login', login),
    path('register', register),
    path('logout',logout),
    path('ping', ping),
    path('userinfo', userinfo),
    path('login_anon', login_anon),
    path('fileupload', fileupload),
    path('setKey', setKey),
    re_path(r'^downloadKey/(?P<key>\w{1,100})/$', downloadKey),
    path('renameFolder', renameFolder),
    path('deleteFolder', deleteFolder),
    path('uploadFolder', uploadFolder),
    path('downloadLink', downloadLink),
    path('deleteFile', deleteFile),
    path('renameFile', renameFile),
    path('listFiles', listFiles),
    path('listFolders', listFolders),
    # path('getlinkfiles', getlinkfiles),
    path('downloadFile', downloadFile),
    re_path(r'^downloadLink/(?P<key>\w{1,100})/$', downloadLinkFile),
    path('shareFolder', shareFolder),
    path('createGroup', createGroup),
    path('joinGroup', joinGroup),
    path('listUsersInGroup', listUsersInGroup),
]
