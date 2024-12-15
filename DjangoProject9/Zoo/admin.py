
from django.contrib import admin
from .models import (Cuidador, Animal,
                     Empleado, HistorialMedico,
                     Veterinario, Cliente,
                     Boleto, Guia, PersonalAdministrativo, Jaula,
                     Zoological, Direction, PersonalLimpieza)

# Register your models here.
@admin.register(Cuidador)
class CuidadorAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'cedula')
    list_filter = ('nombre', 'cedula')
    list_display = ('nombre', 'cedula')
@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'especie', 'estado', 'edad', 'zona')
    list_filter = ('nombre','estado')
    list_display = ('nombre', 'especie', 'edad', 'estado', 'dieta', 'cuerpo', 'zona' )
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'cedula')
    list_filter = ('nombre', 'cedula')
    list_display = ('nombre', 'cedula')

@admin.register(HistorialMedico)
class HistorialMedicoAdmin(admin.ModelAdmin):
    search_fields = ( 'diagnostico',)
    list_filter = ('animal__nombre', 'diagnostico')
    list_display = ('animal', 'diagnostico')

@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'especialidad')
    list_filter = ('nombre', 'especialidad')
    list_display = ('nombre', 'especialidad')



@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    search_fields = ('numero',)
    list_filter = ('fecha_visita',)
    list_display = ('numero', 'fecha_visita')

# Definir el InlineFormSet para los boletos
class BoletoInline(admin.TabularInline):
    model = Cliente.boletos_comprados.through  # Many-to-Many intermediary model
    extra = 1  # Número de formularios vacíos que se mostrarán inicialmente

    def get_queryset(self, request):
        # Puedes personalizar la consulta aquí si es necesario
        return super().get_queryset(request)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'cedula', 'edad')
    list_filter = ('nombre', 'cedula', 'edad')
    list_display = ('nombre', 'cedula', 'edad')
    inlines = [BoletoInline]

@admin.register(Guia)
class GuiaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'cedula')
    list_display = ('nombre', 'cedula', 'recorrido')
    list_filter = ('nombre', 'cedula')

@admin.register(PersonalAdministrativo)
class PersonalAdministrativoAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'cedula', 'departamento', 'salario')
    list_display = ('nombre', 'cedula', 'departamento', 'salario')

@admin.register(Jaula)
class JaulaAdmin(admin.ModelAdmin):
    search_fields = ('numero_jaula',)
    list_filter = ( 'esta_limpio',)
    list_display = ('numero_jaula','capacidad', 'esta_limpio')

@admin.register(Zoological)
class ZoologicalAdmin(admin.ModelAdmin):
    search_fields = ('nombre', '', 'capacidad', 'horario_apertura' )
    list_filter = ('nombre',)
    list_display = ('nombre', 'capacidad', 'horario_apertura')

@admin.register(PersonalLimpieza)
class PersonalLimpiezaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'cedula', 'salario')
    list_display = ('nombre', 'cedula', 'salario')

admin.site.register(Direction)