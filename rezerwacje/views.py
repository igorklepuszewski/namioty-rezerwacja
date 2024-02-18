from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from rezerwacje.models import Namiot, Rezerwacja
from django.db import transaction

# Create your views here.
class NamiotListView(ListView):
    model = Namiot
    template_name = "index.html"
    queryset = Namiot.objects.all()

    def get_queryset(self):
        return self.queryset.filter(rezerwacja=None)
        # return [ namiot for namiot in self.queryset if not namiot.is_reserved]

class NamiotDetailView(DetailView):
    model = Namiot
    template_name = "detail.html"

@transaction.atomic
def reserve(request, namiot_id):
    namiot = Namiot.objects.get(id=namiot_id)
    if not namiot.is_reserved:
        rez = Rezerwacja(namiot=namiot)
        rez.save()
    return redirect("index")

@transaction.atomic
def unreserve(request, rezerwacja_id):
    try:
        rez = Rezerwacja.objects.get(id=rezerwacja_id)
    except Rezerwacja.DoesNotExist:
        pass
    else:
        rez.delete()
    return redirect("index")


