from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from rezerwacje.models import Namiot, Rezerwacja
from django.db import transaction
from rezerwacje.forms import NamiotForm

# Create your views here.
# widok listy namiotow
class NamiotListView(ListView):
    model = Namiot
    template_name = "index.html"
    queryset = Namiot.objects.all()
    context_object_name = "object_list"

    # za kazdym razem bierz tylko namioty bez rezerwacji
    def get_queryset(self):
        return self.queryset.filter(rezerwacja=None)
        # return [ namiot for namiot in self.queryset if not namiot.is_reserved]

    # tworzac dane dla strony dodaj formularz
    def get_context_data(self, **kwargs):
        context = super(NamiotListView, self).get_context_data(**kwargs)
        # jesli request jest POST to uzupelnij formularz danymi, jesli nie to nie
        context["form"] = NamiotForm(self.request.POST or None)
        return context

    def post(self, *args, **kwargs):
        # deklaracja object_list potrzebna do get_context_data -> uzywa tego wewnatrz
        self.object_list = self.get_queryset()
        # pobierz dane dla strony
        context = self.get_context_data()
        # wybierz formualrz z danych
        form = context["form"]
        # jesli formularz ma poprawne dane
        if form.is_valid():
            # wybierz z danych interesujace nas zmienne
            kolor = self.request.POST["kolor"]
            rozmiar = self.request.POST["rozmiar"]
            standard = self.request.POST["standard"]

            # sprawdz czy dany atrybut nie jest pustym lancuchem znakow, jesl nie jest to przefiltruj juz pobrana object_list
            if kolor != "":
                self.object_list = self.object_list.filter(kolor=kolor)
            if rozmiar != "":
                self.object_list = self.object_list.filter(rozmiar=rozmiar)
            if standard != "":
                self.object_list = self.object_list.filter(standard=standard)
            # podmien nieprzefiltrowana liste obiketow na taka po filtracji
            context[self.context_object_name] = self.object_list
        # wyrendeuj plik html z danymi i zwroc jako odpowiedz na zapytanie
        return render(self.request, self.template_name, context)



class NamiotDetailView(DetailView):
    model = Namiot
    template_name = "detail.html"


class RezerwacjaListView(ListView):
    model = Rezerwacja
    template_name = "rezerwacje.html"

# transaction.atomic gwarantuje ze dwie osoby nie zarezerwuja tego samego namiotu w jednym momencie
@transaction.atomic
def reserve(request, namiot_id):
    # wez namiot
    namiot = Namiot.objects.get(id=namiot_id)
    # sprawdz czy jest zarezerwowany
    if not namiot.is_reserved:
        # jesli nie ma rezerwacji to ja stworz i zapisz
        rez = Rezerwacja(namiot=namiot)
        rez.save()
    # odeslij uzytkownika na strone glowna
    return redirect("index")

@transaction.atomic
def unreserve(request, rezerwacja_id):
    try:
        # wez rezerwacje z podanym ID
        rez = Rezerwacja.objects.get(id=rezerwacja_id)
    except Rezerwacja.DoesNotExist:
        # jesli takiej nie ma to nic sie nie dzieje
        pass
    else:

        # jesli nie znajdziemy bledu (jest taka rezerwacja), to ja usun
        rez.delete()
    # na koniec zawsze odeslij uzytkownika na strone glowna
    return redirect("index")


