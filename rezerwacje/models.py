from django.db import models

# Create your models here.
class Namiot(models.Model):
    KOLORY_CHOICES = [("ZIELONY", "zielony"), ("CZERWONY", "czerwony"), ("ZOLTY", "zolty")]
    STANDARD_CHOICES = [("PREMIUM", "premium"), ("OK", "ok"), ("BUDGET", "budget")]
    rozmiar = models.PositiveSmallIntegerField()
    kolor = models.CharField(max_length=16, choices=KOLORY_CHOICES, default="CZERWONY")
    standard = models.CharField(max_length=16, choices=STANDARD_CHOICES, default="OK")

    @property
    def is_reserved(self):
        try:
            rez = self.rezerwacja
        except Rezerwacja.DoesNotExist:
            return False
        else:
            return True

    def __str__(self):
        #4_zielony_ok
        return f"{self.id}_{self.rozmiar}_{self.kolor}_{self.standard}"

class Rezerwacja(models.Model):
    namiot = models.OneToOneField(Namiot, on_delete=models.CASCADE)
    # dobrze by bylo zapisac date stworzenia

    def __str__(self):
        return f"{self.id}/{self.namiot}"
