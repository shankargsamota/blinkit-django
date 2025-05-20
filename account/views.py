from django.shortcuts import render
from account.models import User
from django.contrib.auth import login , authenticate
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView , CreateAPIView , GenericAPIView
from .serializers import RegisterSerializer, LoginSerializer, TokenSerializer , UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny


# Create your views here.
class SignupView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        tokens = TokenSerializer.get_token(user)
        return Response(
            {
                "data": UserSerializer(user).data , 
                "tokens":tokens
            }, 
            status=status.HTTP_200_OK
        )
    
    


# class AddressList(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = AddressSerializer

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Address.objects.filter(user=user)
#         return queryset
    
#     def list(self,request,*args,**kwargs):
#         queryset = self.get_queryset()

#         if not queryset.exists():
#             return Response(
#                  {
#                     "status": "success",
#                     "status_code": status.HTTP_200_OK,
#                     "data": []
#                 },
#                 status=status.HTTP_200_OK
#             )

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(
#             {
#                 "status": "success",
#                 "status_code": status.HTTP_200_OK,
#                 "data": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )
    

# class AddAddressView(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = AddressSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save(user=request.user)

#             return Response(
#                 {
#                     "status":"success",
#                     "status_code": status.HTTP_200_OK,
#                     "message": "Address added successfully",
#                     "data": serializer.data,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )
        
#         return Response(
#             {
#                 "status": "error",
#                 "status_code": status.HTTP_400_BAD_REQUEST,
#                 "message": "Invalid data",
#                 "errors": serializer.errors,
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )