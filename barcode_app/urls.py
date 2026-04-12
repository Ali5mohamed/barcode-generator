# from django.urls import path
# from . import views




# app_name = 'barcode_app'
# urlpatterns = [
#     path("create/", views.create_barcode, name="create_barcode"),
#     path("delete_barcode/<int:barcode_id>", views.delete_barcode, name="delete_barcode"),
#     path("product_detail/<int:barcode_id>/", views.product_detail, name="product_detail"),
# ]


from django.urls import path
from . import views

app_name = "barcode_app"

urlpatterns = [
 
    path("create/", views.create_barcode, name="create_barcode"),
    path("delete/<int:barcode_id>/", views.delete_barcode, name="delete_barcode"),
    path("edit_menu/<int:barcode_id>/", views.edit_menu, name="edit_menu"),
    path("product/<int:barcode_id>/", views.product_detail, name="product_detail"),
    path("delete/product/<int:pk>/", views.delete_product, name="delete_product"),
    path("edit/product/<int:pk>/", views.edit_product, name="edit_product"),
    path ("minu/" , views.minu , name="minu")
]
