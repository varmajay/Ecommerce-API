from itertools import product
from random import choices
from wsgiref import headers
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import *
from rest_framework.permissions import *
from django.conf import settings
from django.core.mail import send_mail
from myapp.serializers import *
from .models import * 
from rest_framework import status
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
import jwt, json
from .utils import *
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date
from django.db.models import Value, DateField

# Create your views here.
@api_view(['GET'])
def index(request):
    url_pattern ={

        'Index':'',
        'Register':'/register/',
        'Login':'/login/',
        'Admin Profile':'profile-admin/id',
        'View Seller':'view-seller',
        'Verify Seller':'verify-seller/id',
        'Delete Seller':'delete-seller/id',
        'View Buyer':'view-buyer',
        'Verify Buyer':'verify-buyer/id',
        'Delete Buyer':'delete-buyer/id',
        'Add Product':'add-product',
        'View Product':'view-product',
        'Edit Product':'edit-product/id',
        'Delete Product ':'delete-product/id',
        'Seller Profile':'profile-seller/id',
        'Update Buyer Product Status':'update-status/id',
        'All Product':'all-product',
        'View One Product In Detail':'detail-product/id',
        'Add To Cart':'add-to-cart/id',
        'MyCart':'my-cart',
        'Edit Cart':'edit-cart/id',
        'Delete Cart':'delete-cart/id',
        'Checkout Product ':'checkout',
        'View My Buys':'my-buy',
        'Cancel Order ':'cancel-order/id',
        
    }
    return Response(url_pattern)


class RegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginAPI(GenericAPIView):
    # permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            email = request.data['email']
            password = request.data['password']
            user1 = User.objects.get(email=email)
            if user1 is not None:
                try:
                    user = authenticate(request, email=user1.email, password=password)
                    if user is None:
                        return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid email or password"},status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid email or password"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid email or password"},status=status.HTTP_400_BAD_REQUEST)
        if user:
            payload = {
                'id': user.id,
                'email': user.email,
            }
            jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            UserToken.objects.create(user=user, token=jwt_token)
            return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "User Login Successfully.",
                                    "result": {'id': user.id,
                                            'name':user.name, 
                                            'email':user.email, 
                                            'token': jwt_token,
                                            }},
                                status=status.HTTP_200_OK)




class LogoutView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        try:
            token = Authenticate(self, request)
            token1 = token.decode("utf-8")
            try:
                user_token = UserToken.objects.get(user=request.user, token=token1)
                user_token.delete()
                logout(request)
            except:
                return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                      "Message": 'Already Logged Out.'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"Status": status.HTTP_200_OK,
                                  "Message": "User Logged Out."},
                            status=status.HTTP_200_OK)
        except:
            return Response(data={"Status":status.HTTP_400_BAD_REQUEST,
                                    "Message":'Already Logged Out.'},
                            status=status.HTTP_400_BAD_REQUEST)




# ----------------------------------__Admin___-------------------------------------------

class ProfileAdminAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer


class ViewSellerAPI(ListAPIView):
    permission_classes= [IsAdminUser]
    queryset = User.objects.filter(role = 'seller')
    serializer_class = ViewSerializer

class VerifySellerAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(role='seller')
    serializer_class = VerifySerializer


class DeleteSellerAPI(GenericAPIView):
    permission_classes = [IsAdminUser]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = ViewSerializer(user)
        return Response(serializer.data)

    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response('data deleted sucessfully')

    
class ViewBuyerAPI(ListAPIView):
    permission_classes= [IsAdminUser]
    queryset = User.objects.filter(role = 'buyer')
    serializer_class = ViewSerializer

class VerifyBuyerAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(role = 'buyer')
    serializer_class = VerifySerializer


class DeleteBuyerAPI(GenericAPIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = ViewSerializer(user)
        return Response(serializer.data)

    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response('data deleted sucessfully')


class AddProductAPI(GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save(seller=request.user)
            return Response(data={"message": "Product Add sucessfully.","result": serializer.data },status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ViewProductAPI(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self,request):
        return Product.objects.filter(seller = request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(request))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data is not None:
            return Response(serializer.data)
        else:
            return Response(data={
                                    "Message":'Invalid User.'},
                            status=status.HTTP_400_BAD_REQUEST)


class EditProductAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DeleteProductAPI(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProfileSellerAPI(RetrieveUpdateAPIView):
    permission_classes =[IsAuthenticated]
    queryset = User.objects.filter(role = 'seller')
    serializer_class = ProfileSerializer


class UpdateOrderStatusAPI(GenericAPIView):
    
    permission_classes=[IsAuthenticated]
    serializer_class=UpdateOderStatusSerilizer
    
    def get_object(self, pk):
        try:
            return Buyproduct.objects.get(pk=pk)
        except Buyproduct.DoesNotExist:
            raise Http404
        
    def put(self,request,pk):
        buy = self.get_object(pk=pk)
        # print(request.user)
        # print(buy.product.seller)
        if buy.product.seller == request.user:
            serializer=UpdateOderStatusSerilizer(instance=buy,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_200_OK,'msg':'status update','results':serializer.data})
            else:
                return Response({'status':status.HTTP_404_NOT_FOUND,'msg':'enter the valid status'})
        else:
            return Response('you cannot edit other ordered status')


            
# ----------------------------------Buyer-------------------------------
class AllproductView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class DetailProductView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AddToCartAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerailizer

    def post(self, request, pk):
        product = Product.objects.get(id=pk)
        quantity = int(request.data['quantity'])
        if request.user.role == 'buyer':
            if product.quantity >= quantity:
                serializer = AddToCartSerailizer(data = request.data)
                if serializer.is_valid(raise_exception= True):
                    serializer.save(user=request.user,product = product)
                    return Response(data={"message": "Product Add sucessfully.",
                                            "result": serializer.data },
                                            status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"Message":'Your Quantity is more than available Quantity.'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data={"Message":'Invalid User.'},status=status.HTTP_400_BAD_REQUEST)



class MyCartAPI(GenericAPIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        cart=Mycart.objects.filter(user=request.user)
        serializer=MyCartSerailizer(cart,many=True)
        return Response(serializer.data)  





class EditMycartAPI(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=AddToCartSerailizer
    
    def get_object(self, pk):
        try:
            return Mycart.objects.get(pk=pk)
        except Mycart.DoesNotExist:
            raise Http404
        
    def patch(self,request,pk):
        cart=self.get_object(pk=pk)
        if request.user == cart.user:
            serializer=AddToCartSerailizer(instance=cart,data=request.data)
            if serializer.is_valid():
                quantity = int(request.data['quantity'])
                if cart.product.quantity >= quantity:
                    serializer.save()
                    return Response({'status':status.HTTP_200_OK,'msg':'your cart update','data':serializer.data},status=status.HTTP_200_OK)
                return Response('Your Quantity is more than available Quantity.')
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"Message":'Invalid User.'},status=status.HTTP_400_BAD_REQUEST)  




class DeleteCartAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Mycart.objects.get(pk=pk)
        except Mycart.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = MyCartSerailizer(user)
        return Response(serializer.data)

    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response('data deleted sucessfully')




class CheckoutAPI(GenericAPIView):

    def post(self, request):
        cart = Mycart.objects.filter(user = request.user)
        total_amount = 0
        for d in cart:
            total_amount += d.product.quantity * d.product.price
        print(total_amount)
        for data in cart:
            if data.product.quantity >= data.quantity:
                serializer = BuyProductSerailizer(data = request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(buyer=request.user, product=data.product, total_amount= total_amount, quantity = data.quantity)
                    data.product.quantity -= data.quantity
                    data.product.save()
                    data.delete()
                    return Response({'status':status.HTTP_200_OK,
                                    'message':'Order Placed','data':serializer.data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status':status.HTTP_406_NOT_ACCEPTABLE,'message':'Quantity is Not available'},status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'status':status.HTTP_302_FOUND,'message':'Your cart is Empty'},status=status.HTTP_302_FOUND)





class BuyViewAPI(ListAPIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        cart = Buyproduct.objects.filter(buyer=request.user)
        serializer=BuyProductViewSerailizer(cart,many=True)
        return Response(serializer.data)


class CancelOrderedAPI(GenericAPIView):
    permission_classes=[IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Buyproduct.objects.get(pk=pk)
        except Buyproduct.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = BuyProductViewSerailizer(user)
        return Response(serializer.data)

    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response('Order  is Cancel ')