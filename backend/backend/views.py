from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.http import FileResponse
from uuid import uuid4
from .models import *


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_anon(request):
    username = request.data.get("username")
    if username is None:
        return Response({'error': 'Please provide a username'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.create_user(username=uuid4().__str__().replace("-",''), password=username)
        user.is_anonymous = True
    except Exception as e:
        print(e)
    user.set_unusable_password()
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
    except Exception as e:
        user = False
        pass

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        if email is None:
            email = ""
        details = UserDetails(uid=user.id)
        details.save()
        return Response({'token': token.key}, status=HTTP_200_OK)
    else:
        if email is None:
            email = ""
        user = User.objects.create_user(username=username, password=password, email=email)
        details = UserDetails(uid=user.id)
        details.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def logout(request):
    try:
        request.user.auth_token.delete()
    except Exception as e:
        Response("The token doesn't exist", status=HTTP_400_BAD_REQUEST)
    return Response("Logout successful", status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def ping(request):
    data = {'pong'}
    return Response(data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def userinfo(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        user = request.user
        userDetails = UserDetails(uid=user.id)
        data = {'username': user.username, 'email': user.email, 'quota': "unlimited", 'registered': user.date_joined.strftime("%Y-%m-%d %H:%M:%S"), "token": user.auth_token.key, "friends": userDetails.friends, "alias": userDetails.userAlias }
    return Response(data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def fileupload(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        name = request.data.get("name")
        if name is None or request.FILES['upload_file'] is None:
            return Response({'error': 'Please provide a file name and a file'},
                            status=HTTP_400_BAD_REQUEST)
        user = request.user
        try:
            file = File(owner=user.username, name=name, file=request.FILES['upload_file'])
            file.save()
        except Exception as e:
            print(e)
            return Response("Internal server error!", status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("The file was uploaded", status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def setKey(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        key = request.data.get("key")
        meant_for = request.data.get("meant_for")
        if key is None or meant_for is None:
            return Response({'error': 'Please provide a key, owner and intended recipient'},
                            status=HTTP_400_BAD_REQUEST)
        user = request.user
        try:
            key = Key(key=key, owner=user.username, meant_for=meant_for)
            key.save()
        except Exception as e:
            print(e)
            return Response("Internal server error!", status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'The key was saved', 'key': key.id}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def downloadLink(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        file = request.data.get("file")
        if file is None:
            return Response({'error': 'Please provide a file name!'},
                            status=HTTP_400_BAD_REQUEST)
        user = request.user
        try:
            for files in File.objects.all().filter(name=file, owner= user.username).iterator():
                fileObj = files
            if fileObj is None:
                Response({'error': 'Please provide a file name that is in the mounted directory!'},
                         status=HTTP_400_BAD_REQUEST)
            link = Link(owner=user.username, file=fileObj)
            link.save()
            uid = link.uid
        except Exception as e:
            print(e)
            return Response("Internal server error!", status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'The link was saved', 'key': uid}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def getlinks(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        user = request.user
        links = []
        try:
            for l in Link.objects.all().iterator():
                links.append(l.uid)
        except Exception as e:
            print(e)
            return Response("Internal server error!", status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(links, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def getlinkfiles(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        linkuid = request.data.get("link")
        link = Link.objects.all().filter(uid=linkuid)
        return Response(link.files, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def uploadFolder(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        name = request.data.get("name")
        if name is None:
            return Response({'error': 'Please provide a folder name'},
                            status=HTTP_400_BAD_REQUEST)
        user = request.user
        try:
            folder = Folder(name=name, owner=user.username)
            folder.save()
        except Exception as e:
            print(e)
            return Response("Internal server error!", status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("The folder was saved", status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def deleteFolder(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        name = request.data.get("name")
        if name is None:
            return Response({'error': 'Please provide a folder name'},
                            status=HTTP_400_BAD_REQUEST)
        try:
            folder = Folder.objects.get(name=name)
            folder.delete()
        except Exception as e:
            print(e)
            return Response("Internal server error!", status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("The folder was deleted", status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def renameFolder(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        name = request.data.get("name")
        old_name = request.data.get("old_name")
        if name is None:
            return Response({'error': 'Please provide a folder name'},
                            status=HTTP_400_BAD_REQUEST)
        try:
            folder = Folder.objects.get(name=old_name)
            folder.name = name
            folder.save()
        except Exception as e:
            print(e)
            return Response("Internal server error!", status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("The folder was renamed", status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def renameFile(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        name = request.data.get("name")
        old_name = request.data.get("old_name")
        if name is None:
            return Response({'error': 'Please provide a file name'},
                            status=HTTP_400_BAD_REQUEST)
        try:
            file = File.objects.get(name=old_name)
            file.name = name
            file.save()
        except Exception as e:
            print(e)
            return Response("Internal server error!", status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("The file was renamed", status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def deleteFile(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        name = request.data.get("name")
        if name is None:
            return Response({'error': 'Please provide a file name'},
                            status=HTTP_400_BAD_REQUEST)
        try:
            file = File.objects.get(name=name)
            file.delete()
        except Exception as e:
            print(e)
            return Response("Internal server error!", status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("The file was deleted", status=HTTP_200_OK)


@csrf_exempt
@api_view(["Get"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def listFiles(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        files = []
        for f in File.objects.all().filter(owner=request.user.username).iterator():
            files.append(f.name)

        return Response(files, status=HTTP_200_OK)


@csrf_exempt
@api_view(["Get"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def listFolders(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        folders = []
        for f in Folder.objects.all().filter(owner=request.user.username).iterator():
            folders.append(f.name)

        return Response(folders, status=HTTP_200_OK)


@csrf_exempt
@api_view(["Get"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def downloadFile(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        name = request.data.get("name")
        for f in File.objects.all().filter(owner=request.user.username, name=name).iterator():
            return FileResponse(f.file, status=HTTP_200_OK)


@csrf_exempt
@api_view(["Get"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def downloadLinkFile(request, key):
    for l in Link.objects.all().filter(uid=key).iterator():
        file = l.file
    if file is None:
        return Response("Link doesn't exist!", status=HTTP_200_OK)
    else:
        return FileResponse(file.file, status=HTTP_200_OK)


@csrf_exempt
@api_view(["Get"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def downloadKey(request, key):
    for k in Key.objects.all().filter(uid=key).iterator():
        savedKey = k.key
    if savedKey is None:
        return Response("Key doesn't exist!", status=HTTP_200_OK)
    else:
        return FileResponse(savedKey, status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def shareFolder(request):
    if request.user.is_anonymous == True:
        return Response('{This is an AnonymousUser!}', status=HTTP_200_OK)
    else:
        name = request.data.get("name")
        user = request.data.get("user")
        if user is None or name is None:
            return Response('{Please provide a user and a folder name!}', status=HTTP_400_BAD_REQUEST)
        else:

            username = None
            for u in User.objects.all().filter(username=user):
                username = u
            if username is None:
                return Response('{Please provide a valid user!}', status=HTTP_400_BAD_REQUEST)

            folder = None
            for f in Folder.objects.all().filter(name=name, owner=request.user.username):
                folder = f
            if folder is None:
                return Response('{Please provide a valid folder!}', status=HTTP_400_BAD_REQUEST)

            ### CREATE SHARE FOLDER ON RECIPIENT ACCOUNT
            fol = None
            for f in Folder.objects.all().filter(owner=username, name='/shares'):
                fol = f

            if fol is None:
                f = Folder(owner=username, name='/shares')
                f.save()

            folRecipient = None
            for f in Folder.objects.all().filter(owner=username, name='/shares/' + request.user.username):
                folRecipient = f

            if folRecipient is None:
                f = Folder(owner=username, name='/shares/' + request.user.username)
                f.save()

            folShare = None
            for f in Folder.objects.all().filter(owner=username, name='/shares/' + request.user.username + "/" + name):
                folShare = f

            if folShare is None:
                f = Folder(owner=username, name='/shares/' + request.user.username + "/" + name)
                f.save()

            ### COPY ALL FILES IN THE SHARED FOLDER TO THE RECIPENTS ACCOUNT

            for f in File.objects.all().filter(owner=request.user.username):
                if f.name.startswith(name):
                    file = File(owner=user, name='/shares/' + request.user.username + "/" + f.name, file=f.file)
                    file.save()

        return Response("Folder was shared!", status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def createGroup(request):
    if request.user.is_anonymous == True:
        return Response({'message': 'This is an AnonymousUser!'}, status=HTTP_200_OK)
    else:
        name = request.data.get("name")

        if name is None:
            return Response({'message': 'Please provide a group name!'}, status=HTTP_400_BAD_REQUEST)
        else:
            new_group, created = Group.objects.get_or_create(name=name)

            if created is None:
                return Response({'message': 'Group already exist!'}, status=HTTP_200_OK)

            #permission = Permission.objects.create(codename='can_add_users', name='Can add users to the group')
            #new_group.permissions.add(permission)
            new_group.user_set.add(request.user)
            new_group.save()

            return Response({'message': 'Group was created!'}, status=HTTP_200_OK)


##################################################################################
###############    THIS IS NOT READY; NEEDS TESTING   ############################
##################################################################################

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def joinGroup(request):
    if request.user.is_anonymous == True:
        return Response({'message': 'This is an AnonymousUser!'}, status=HTTP_200_OK)
    else:
        name = request.data.get("name")
        username = request.data.get("user")

        if name is None:
            return Response({'message': 'Please provide a group name!'}, status=HTTP_400_BAD_REQUEST)
        else:
            new_group, created = Group.objects.get_or_create(name=name)

            if created is None:
                return Response({'message': 'Group does not exist!'}, status=HTTP_200_OK)

            try:
                user = User.objects.get(username=username)
                group = Group.objects.get(name=name)
                user.groups.add(group)
            except Exception as e :
                print(e)

            return Response({'message': 'User was added to the group!'}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def listUsersInGroup(request):
    if request.user.is_anonymous == True:
        return Response({'message': 'This is an AnonymousUser!'}, status=HTTP_200_OK)
    else:
        name = request.data.get("name")

        if name is None:
            return Response({'message': 'Please provide a group name!'}, status=HTTP_400_BAD_REQUEST)
        else:


            list = []
            for u in User.objects.filter(groups__name=name).iterator():
                list.append(u.username)

            return Response({'users': list}, status=HTTP_200_OK)





