from django.contrib import admin

# Register your models here.
from boe_api.state.models import Partido, Legislatura

admin.site.register(Partido)
admin.site.register(Legislatura)