from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, Group, User
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView, status
from axes.utils import reset
import datetime

class AuthTokenLogin(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created =  Token.objects.get_or_create(user=serializer.object['user'])

            utc_now = datetime.datetime.now()    
            if not created and token.created < utc_now - datetime.timedelta(hours=24):
                token.delete()
                token = Token.objects.create(user=serializer.object['user'])
                token.created = datetime.datetime.now()
                token.save()

            #return Response({'token': token.key})
            return Response({'token2': token.key}, content_type="application/json")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def GetSessionInfo(request):
    """API View que retorna os dados atuais da sessão

    Args:
        request (obj): Objeto request de requisição

    Returns:
        Dict: Retorna um dicionário com informações da sessão atual. 
    """    
    isAuthenticated = request.user.is_authenticated
    def userPermissions() -> list:
        permissions = list()
        permissionsQuery = Permission.objects.filter(user=request.user)
        return [permission.codename for permission in permissionsQuery]
    
    def userGroups() -> list:
        groups = list()
        groupQuery = Group.objects.filter(user = request.user)
        return [group.name for group in groupQuery]
    
    if(isAuthenticated):
        return JsonResponse(
            {
                "id": request.user.id,
                "email": request.user.email,
                'username': request.user.username,
                'firstName': request.user.first_name,
                'lastName': request.user.last_name,
                'isActive': request.user.is_active,
                'isAdmin': request.user.is_staff,
                'isAuthenticated': True,
                "profileImage": UserProfile.getAvatar(request.user.username),
                "verified": True,
                "role":  {
                    "id": request.user.id,
                    "groups": userGroups(),
                    "permissions": userPermissions()
            },
        })
    return JsonResponse({
            "id": None,
            "email": '',
            'username': '',
            'firstName': '',
            'lastName': '',
            'isActive': '',
            'isAdmin': '',
            'isAuthenticated': False,
            "profileImage": '',
            "verified": False,
            "role":  {
                "id": None,
                "groups": [],
                "permissions": []
        },
    })

@csrf_protect
def attemptLogin(request):
    """Tenta fazer login no sistema

    Args:
        request (Form): Requer usuário e senha

    Returns:
        dict: Retorna um dicionário com informações de status de requisição
    """    
    if(request.method == 'POST'):
        username =  request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if(user):
            reset(ip = request.META.get("REMOTE_ADDR"))
            login(request, user)
            # return suc
    # return errorJsonResponse()

def logoutView(request) -> dict:
    """API View que faz logout do sistema 

    Args:
        request (obj): Objeto de requisição

    Returns:
        dict: Retorna um dicionário com informações de status de requisição
    """    
    logout(request)
    return successJsonResponse()