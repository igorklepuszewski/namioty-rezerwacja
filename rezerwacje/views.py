from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from rezerwacje.models import Namiot, Rezerwacja
from django.db import transaction
from rezerwacje.forms import NamiotForm

# Create your views here.
class NamiotListView(ListView):
    model = Namiot
    template_name = "index.html"
    queryset = Namiot.objects.all()
    context_object_name = "object_list"

    def get_queryset(self):
        return self.queryset.filter(rezerwacja=None)
        # return [ namiot for namiot in self.queryset if not namiot.is_reserved]

    def get_context_data(self, **kwargs):
        context = super(NamiotListView, self).get_context_data(**kwargs)
        context["form"] = NamiotForm(self.request.POST or None)
        return context

    def post(self, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        form = context["form"]
        if form.is_valid():
            kolor = self.request.POST["kolor"]
            rozmiar = self.request.POST["rozmiar"]
            standard = self.request.POST["standard"]

            if kolor != "":
                self.object_list = self.object_list.filter(kolor=kolor)
            if rozmiar != "":
                self.object_list = self.object_list.filter(rozmiar=rozmiar)
            if standard != "":
                self.object_list = self.object_list.filter(standard=standard)

            context[self.context_object_name] = self.object_list
        return render(self.request, self.template_name, context)



class NamiotDetailView(DetailView):
    model = Namiot
    template_name = "detail.html"


class RezerwacjaListView(ListView):
    model = Rezerwacja
    template_name = "rezerwacje.html"


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


