from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import RegisterSerializer


@method_decorator(swagger_auto_schema(operation_id='Register User - POST'), name='post')
class RegisterUserView(GenericAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response(data={'success': 'success'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(swagger_auto_schema(operation_id='Logout User - POST'), name='post')
class BlackListTokenView(APIView):
    """
    This view is same as a logout's view functionality.

    send a POST request with only the refresh_token object.

    {
        refresh_token: <user_refresh_token>
    }
    """
    permission_classes = [HasAPIKey]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(data={'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
