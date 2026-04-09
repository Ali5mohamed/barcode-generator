from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from django.conf import settings

from .models import Barcode
from .forms import BarcodeForm
from .forms import LinkForm , ProductForm
from .models import Barcode
from .models import Product , Link 
import os
import qrcode


@login_required
def create_barcode(request):
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.barcode = Barcode.objects.create(
                title=request.POST.get("title"),
                user=request.user,
                type="link"
            )
            link.save()

            # إنشاء QR
            qr_data = link.url
            img = qrcode.make(qr_data)
            barcode_dir = os.path.join(settings.MEDIA_ROOT, "barcodes")
            os.makedirs(barcode_dir, exist_ok=True)
            file_name = f"barcode_{link.barcode.id}.png"
            file_path = os.path.join(barcode_dir, file_name)
            img.save(file_path)

            link.barcode.qr_code.name = f"barcodes/{file_name}"
            link.barcode.save(update_fields=["qr_code"])

            messages.success(request, "تم إنشاء اللينك بنجاح ✅")
            return redirect("accounts:dashboard")
    else:
        form = LinkForm()

    return render(request, "create.html", {"form": form})
def minu(request):
    if request.method == "POST":
        # حفظ بيانات الباركود أولاً
        title = request.POST.get("title", "").strip()
        barcode_type = "menu"  # بما أن هذه الصفحة للـ menu فقط
        if not title:
            messages.error(request, "الرجاء إدخال عنوان الباركود")
            return redirect(request.path)

        barcode = Barcode.objects.create(
            user=request.user,
            title=title,
            type=barcode_type
        )

        # حفظ المنتجات الديناميكية
        names = request.POST.getlist("name[]")
        prices = request.POST.getlist("price[]")
        descs = request.POST.getlist("desc[]")

        for name, price, desc in zip(names, prices, descs):
            if name.strip():  # نتأكد أن الاسم مش فاضي
                Product.objects.create(
                    barcode=barcode,
                    name=name,
                    price=price,
                    description=desc
                )

        # حفظ منتج رئيسي من الفورم
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.barcode = barcode
            product.save()
        else:
            messages.warning(request, "تم حفظ الباركود والمنتجات الديناميكية، لكن حدث خطأ في المنتج الرئيسي")

        # ---------------- إنشاء QR لكل الباركود
        qr_data = request.build_absolute_uri(f"/barcode_app/scan_barcode/{barcode.id}/")
        img = qrcode.make(qr_data)

        barcode_dir = os.path.join(settings.MEDIA_ROOT, "barcodes")
        os.makedirs(barcode_dir, exist_ok=True)
        file_name = f"barcode_{barcode.id}.png"
        file_path = os.path.join(barcode_dir, file_name)
        img.save(file_path)

        barcode.qr_code.name = f"barcodes/{file_name}"
        barcode.save(update_fields=["qr_code"])

        messages.success(request, "تم إنشاء الباركود والمنتجات بنجاح ✅")
        return redirect("accounts:dashboard")
    else:
        form = ProductForm()

    return render(request, "minu.html", {"form": form})
@login_required
def delete_barcode(request, barcode_id):
    barcode = get_object_or_404(Barcode, id=barcode_id, user=request.user)

    if request.method == "POST":
        barcode.delete()
        messages.success(request, "تم حذف الباركود بنجاح 🗑️")
        return redirect("accounts:dashboard")


def scan_barcode(request, barcode_id):
    barcode = get_object_or_404(Barcode, id=barcode_id)

    #-------------زيادة عدد المسحات
    Barcode.objects.filter(id=barcode_id).update(scans=F("scans") + 1)

    if barcode.type == "link":
        return redirect(barcode.url)

    return redirect("barcode_app:product_detail", barcode_id=barcode.id)



def product_detail(request, barcode_id):
   # نجيب الباركود أو 404 لو مش موجود
    barcode = get_object_or_404(Barcode, id=barcode_id)
    
    # نجيب كل المنتجات المرتبطة بالباركود
    products = Product.objects.filter(barcode=barcode)

    return render(request, "product_detail.html", {
        "barcode": barcode,
        "products": products
    })