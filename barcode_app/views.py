from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from django.conf import settings

from .models import Barcode
from .forms import BarcodeForm
from .forms import LinkForm , ProductForm
from .models import Barcode
from .models import Product , Link , Category
import os
import qrcode
from django.core.files.base import ContentFile
import io
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


@login_required
def minu(request):
    if request.method == "POST":

        title = request.POST.get("title", "").strip()

        if not title:
            messages.error(request, "الرجاء إدخال عنوان الباركود")
            return redirect(request.path)

        # =========================
        # إنشاء الباركود
        # =========================
        barcode = Barcode.objects.create(
            user=request.user,
            title=title,
            type="menu"
        )

        # =========================
        # البيانات الديناميكية
        # =========================
        names = request.POST.getlist("name[]")
        prices = request.POST.getlist("price[]")
        descs = request.POST.getlist("desc[]")
        categories = request.POST.getlist("category[]")
        images = request.FILES.getlist("image[]")

        for i in range(len(names)):

            name = names[i].strip()
            price = prices[i]
            desc = descs[i]
            category_name = categories[i] if i < len(categories) else None
            image = images[i] if i < len(images) else None

            if not name:
                continue

            # =========================
            # إنشاء أو جلب القسم
            # =========================
            category_obj = None
            if category_name:
                category_obj, _ = Category.objects.get_or_create(
                    barcode=barcode,
                    name=category_name.strip()
                )

            # =========================
            # إنشاء المنتج
            # =========================
            Product.objects.create(
                barcode=barcode,
                category=category_obj,
                name=name,
                price=price,
                description=desc,
                image=image
            )

        # =========================
        # إنشاء QR ورفعه على Cloudinary
        # =========================
        qr_data = request.build_absolute_uri(
            f"/barcode_app/product/{barcode.id}/"
        )

        img = qrcode.make(qr_data)

        buffer = io.BytesIO()
        img.save(buffer, format='PNG')

        file_name = f"barcode_{barcode.id}.png"

        barcode.qr_code.save(
            file_name,
            ContentFile(buffer.getvalue()),
            save=True
        )

        messages.success(request, "تم إنشاء المنيو بنجاح ✅")
        return redirect("accounts:dashboard")

    return render(request, "minu.html")
@login_required
#-------داله حزف المنيو كله 
def delete_barcode(request, barcode_id):
    barcode = get_object_or_404(Barcode, id=barcode_id, user=request.user)

    if request.method == "POST":
        barcode.delete()
        messages.success(request, "تم حذف الباركود بنجاح 🗑️")
        return redirect("accounts:dashboard")




def product_detail(request, barcode_id):
    barcode = get_object_or_404(Barcode, id=barcode_id)

    # المنتجات مباشرة من الباركود
    products = barcode.products.select_related("category")

    # الأقسام
    categories = Category.objects.filter(barcode=barcode)

    return render(request, "product_detail.html", {
        "barcode": barcode,
        "products": products,
        "categories": categories,
    })

def edit_menu(request, barcode_id):
    barcode = get_object_or_404(Barcode, id=barcode_id, user=request.user)
    products = Product.objects.filter(barcode=barcode)
    categories = Category.objects.filter(barcode=barcode)

    if request.method == "POST":
        # تعديل عنوان الباركود
        barcode.title = request.POST.get("title", barcode.title)
        barcode.save()

        product_ids = request.POST.getlist("product_id[]")
        names = request.POST.getlist("name[]")
        prices = request.POST.getlist("price[]")
        descs = request.POST.getlist("desc[]")
        categories_data = request.POST.getlist("category[]")
        images = request.FILES.getlist("image[]")

        for i in range(len(names)):

            name = names[i].strip()
            price = prices[i]
            desc = descs[i]
            category_name = categories_data[i] if i < len(categories_data) else None

            # 🟢 إنشاء أو جلب القسم
            category_obj = None
            if category_name:
                category_obj, _ = Category.objects.get_or_create(
                    name=category_name,
                    barcode=barcode
                )

            # =========================
            # تعديل منتج موجود
            # =========================
            if i < len(product_ids) and product_ids[i]:
                product = Product.objects.get(id=product_ids[i], barcode=barcode)

                product.name = name
                product.price = price
                product.description = desc
                product.category = category_obj

                if i < len(images) and images[i]:
                    product.image = images[i]

                product.save()

            # =========================
            # إضافة منتج جديد
            # =========================
            else:
                if name:
                    Product.objects.create(
                        barcode=barcode,
                        category=category_obj,
                        name=name,
                        price=price,
                        description=desc,
                        image=images[i] if i < len(images) else None
                    )

        messages.success(request, "تم تعديل المنيو بنجاح ✅")
        return redirect("barcode_app:product_detail", barcode.id)

    return render(request, "edit_menu.html", {
        "barcode": barcode,
        "products": products,
        "categories": categories
    })

def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    barcode_id = product.barcode.id

    if request.method == "POST":
        product.delete()

    return redirect("barcode_app:product_detail", barcode_id=barcode_id)

def edit_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    barcode_id = product.barcode.id if product.barcode else None

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            product = form.save(commit=False)

            # مهم جدًا: تأكد من حفظ العلاقة
            product.save()

            form.save_m2m()  # لو category ManyToMany

            if barcode_id:
                return redirect("barcode_app:product_detail", barcode_id=barcode_id)
            return redirect("barcode_app:home")

    else:
        form = ProductForm(instance=product)

    return render(request, "edit_product.html", {
        "form": form,
        "product": product
    })