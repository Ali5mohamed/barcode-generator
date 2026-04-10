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
        images = request.FILES.getlist("image[]")

        for i in range(len(names)):

            name = names[i]
            price = prices[i]
            desc = descs[i]

            image = None
            if i < len(images):
                image = images[i]

            if name.strip():
                Product.objects.create(
                    barcode=barcode,
                    name=name,
                    price=price,
                    description=desc,
                    image=image
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




def product_detail(request, barcode_id):
   # نجيب الباركود أو 404 لو مش موجود
    barcode = get_object_or_404(Barcode, id=barcode_id)
    
    # نجيب كل المنتجات المرتبطة بالباركود
    products = Product.objects.filter(barcode=barcode)

    return render(request, "product_detail.html", {
        "barcode": barcode,
        "products": products
    })

def edit_menu(request, barcode_id):
    barcode = get_object_or_404(Barcode, id=barcode_id, user=request.user)
    products = barcode.products.all()

    if request.method == "POST":
        barcode.title = request.POST.get("title", barcode.title)
        barcode.save()

        product_ids = request.POST.getlist("product_id[]")
        names = request.POST.getlist("name[]")
        prices = request.POST.getlist("price[]")
        descs = request.POST.getlist("desc[]")
        images = request.FILES.getlist("image[]")

        for i in range(len(names)):

            name = names[i]
            price = prices[i]
            desc = descs[i]

            if i < len(product_ids) and product_ids[i]:
                # ===== تعديل منتج موجود =====
                product = Product.objects.get(id=product_ids[i], barcode=barcode)

                product.name = name
                product.price = price
                product.description = desc

                # 🟢 الصورة: لو المستخدم رفع جديدة غيرها
                if i < len(images) and images[i]:
                    product.image = images[i]
                # else: نسيب القديمة زي ما هي

                product.save()

            else:
                # ===== إضافة منتج جديد =====
                image = None
                if i < len(images) and images[i]:
                    image = images[i]

                if name.strip():
                    Product.objects.create(
                        barcode=barcode,
                        name=name,
                        price=price,
                        description=desc,
                        image=image
                    )

        messages.success(request, "تم تعديل المنيو بنجاح ✅")
        return redirect("barcode_app:product_detail", barcode.id)

    return render(request, "edit_menu.html", {
        "barcode": barcode,
        "products": products
    })