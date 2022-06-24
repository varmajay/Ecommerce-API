from django.urls import path
from .import views

urlpatterns = [
  path('',views.index,name='index'),
  path('register/',views.RegisterAPI.as_view()),
  path('login/',views.LoginAPI.as_view()),
  path('logout/',views.LogoutView.as_view()),

# ---------------------------Admin-------------------------------
  path('profile-admin/<int:pk>',views.ProfileAdminAPI.as_view()),
  path('view-seller',views.ViewSellerAPI.as_view()),
  path('verify-seller/<int:pk>',views.VerifySellerAPI.as_view()),
  path('delete-seller/<int:pk>',views.DeleteSellerAPI.as_view()),
   path('view-buyer',views.ViewBuyerAPI.as_view()),
  path('verify-buyer/<int:pk>',views.VerifyBuyerAPI.as_view()),
  path('delete-buyer/<int:pk>',views.DeleteBuyerAPI.as_view()),

# ----------------------------Seller-----------------------------
  path('add-product',views.AddProductAPI.as_view()),
  path('view-product',views.ViewProductAPI.as_view()),
  path('edit-product/<int:pk>',views.EditProductAPI.as_view()),
  path('delete-product/<int:pk>',views.DeleteProductAPI.as_view()),
  path('profile-seller/<int:pk>',views.ProfileSellerAPI.as_view()),
  path('update-status/<int:pk>',views.UpdateOrderStatusAPI.as_view()),
# ----------------------------Buyer-----------------------------
  path('all-product',views.AllproductView.as_view()),
  path('detail-product/<int:pk>',views.DetailProductView.as_view()),
  path('add-to-cart/<int:pk>',views.AddToCartAPI.as_view()),
  path('my-cart',views.MyCartAPI.as_view()),  
  path('edit-cart/<int:pk>',views.EditMycartAPI.as_view()),
  path('delete-cart/<int:pk>',views.DeleteCartAPI.as_view()),
  path('checkout',views.CheckoutAPI.as_view()),
  path('my-buy',views.BuyViewAPI.as_view()),
  path('cancel-order/<int:pk>',views.CancelOrderedAPI.as_view()),
]
