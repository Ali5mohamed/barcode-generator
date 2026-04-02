from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from django.conf import settings

from .models import Barcode
from .forms import BarcodeForm

import os
import qrcode

# @login_required
# def create_barcode(request):
#     if request.method == "POST":
#         form = BarcodeForm(request.POST, request.FILES)
#         if form.is_valid():
#             barcode = form.save(commit=False)
#             barcode.user = request.user
#             barcode.save()  

#             # ----------------تحديد بيانات الـ QR
#             #if barcode.type=='link':
#             qr_data = barcode.url
#             #else:
#             qr_data = request.build_absolute_uri(
#                     f"/barcode_app/scan_barcode/{barcode.id}/"
#                 )

#             # ------------------إنشاء صورة QR
#             img = qrcode.make(qr_data)

#             barcode_dir = os.path.join(settings.MEDIA_ROOT, "barcodes")
#             os.makedirs(barcode_dir, exist_ok=True)

#             file_name = f"barcode_{barcode.id}.png"
#             file_path = os.path.join(barcode_dir, file_name)

#             img.save(file_path)

#             # ----------ربط الصورة بالموديل
#             barcode.qr_code.name = f"barcodes/{file_name}"
#             barcode.save(update_fields=["qr_code"])

#             messages.success(request, "تم إنشاء الباركود بنجاح ✅")
#             return redirect("accounts:dashboard")
#     else:
#         form = BarcodeForm()

#     return render(request, "create.html", {"form": form})


@login_required
def create_barcode(request):
    if request.method == "POST":
        form = BarcodeForm(request.POST, request.FILES)
        if form.is_valid():
            barcode = form.save(commit=False)
            barcode.user = request.user

            # إذا أردت يمكنك تعيين نوع الباركود مباشرة
            # barcode.type = 'link'  # لو تريد دائمًا رابط خارجي

            barcode.save()  

            # ----------------تحديد بيانات الـ QR
            # لو حقل url موجود نستخدمه
            if barcode.url:  
                qr_data = barcode.url  # الرابط الذي سيذهب إليه مباشرة
            else:
                # لو لم يكن هناك رابط خارجي، نستخدم رابط داخلي
                qr_data = request.build_absolute_uri(
                    f"/barcode_app/scan_barcode/{barcode.id}/"
                )

            # ------------------إنشاء صورة QR
            img = qrcode.make(qr_data)

            # حفظ الصورة في مجلد media/barcodes
            barcode_dir = os.path.join(settings.MEDIA_ROOT, "barcodes")
            os.makedirs(barcode_dir, exist_ok=True)

            file_name = f"barcode_{barcode.id}.png"
            file_path = os.path.join(barcode_dir, file_name)

            img.save(file_path)

            # ----------ربط الصورة بالموديل
            barcode.qr_code.name = f"barcodes/{file_name}"
            barcode.save(update_fields=["qr_code"])

            messages.success(request, "تم إنشاء الباركود بنجاح ✅")
            return redirect("accounts:dashboard")
    else:
        form = BarcodeForm()

    return render(request, "create.html", {"form": form})

def minu(request):
        if request.method == "POST":
            form = BarcodeForm(request.POST, request.FILES)
            if form.is_valid():
                barcode = form.save(commit=False)
                barcode.user = request.user

                # إذا أردت يمكنك تعيين نوع الباركود مباشرة
                # barcode.type = 'link'  # لو تريد دائمًا رابط خارجي

                barcode.save()  

                # ----------------تحديد بيانات الـ QR
                # لو حقل url موجود نستخدمه
                if barcode.url:  
                    qr_data = barcode.url  # الرابط الذي سيذهب إليه مباشرة
                else:
                    # لو لم يكن هناك رابط خارجي، نستخدم رابط داخلي
                    qr_data = request.build_absolute_uri(
                        f"/barcode_app/scan_barcode/{barcode.id}/"
                    )

                # ------------------إنشاء صورة QR
                img = qrcode.make(qr_data)

                # حفظ الصورة في مجلد media/barcodes
                barcode_dir = os.path.join(settings.MEDIA_ROOT, "barcodes")
                os.makedirs(barcode_dir, exist_ok=True)

                file_name = f"barcode_{barcode.id}.png"
                file_path = os.path.join(barcode_dir, file_name)

                img.save(file_path)

                # ----------ربط الصورة بالموديل
                barcode.qr_code.name = f"barcodes/{file_name}"
                barcode.save(update_fields=["qr_code"])

                messages.success(request, "تم إنشاء الباركود بنجاح ✅")
                return redirect("accounts:dashboard")
        else:
         form = BarcodeForm()

        return render(request , "minu.html" , {"form": form})



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
    barcode = get_object_or_404(Barcode, id=barcode_id)
    if request.method == 'POST':
        form = BarcodeForm(request.POST , request.FILES,instance=barcode)
        if form.is_valid():
            form.save()
            return redirect('accounts:dashboard')
    else:
        form = BarcodeForm(instance=barcode)
    return render(
        request,
        "product_detail.html",
        {
         "barcode": barcode,
         "form":form,
         }
    )


