
from django.shortcuts import render, redirect
from .models import Resimler
from .forms import ImageForm


def anasayfa(request):
    son_nesne = Resimler.objects.order_by("created_at").last()
    son_resim = son_nesne.image.url
    ad = son_nesne.title
    if request.method == "POST":

        response = """<script>$("#my-spinner").show();</script>"""
        yield response

        form = ImageForm(request.POST, request.FILES)        
        if form.is_valid():
            form.save()
            
            response = """<script>$("#my-spinner").hide();</script>"""
            return response
         

    else:
        form = ImageForm()


    return render(request, "marble/anasayfa.html",{"images":son_resim, "form":form, "ad":ad})

