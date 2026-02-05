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
    path("scan_barcode/<int:barcode_id>/", views.scan_barcode, name="scan_barcode"),
    path("product/<int:barcode_id>/", views.product_detail, name="product_detail"),
]
