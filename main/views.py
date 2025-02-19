from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageUploadForm
from .models import UploadedImage
from PIL import Image
import os
from django.conf import settings

def upload_images(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')  # Correctly get multiple uploaded files

        if files:
            images = []
            for file in files:
                image_instance = UploadedImage(image=file)
                image_instance.save()
                images.append(image_instance.image.path)

            if images:
                pdf_path = os.path.join(settings.MEDIA_ROOT, "converted.pdf")
                image_list = [Image.open(img).convert("RGB") for img in images]
                image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])

                with open(pdf_path, "rb") as pdf_file:
                    response = HttpResponse(pdf_file.read(), content_type="application/pdf")
                    response["Content-Disposition"] = 'attachment; filename="converted.pdf"'
                    return response

    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})
