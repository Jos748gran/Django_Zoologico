
from django.db import models
from django.utils.translation import gettext_lazy as _


class Estado(models.TextChoices):
    COMIENDO = 'COMIENDO', _('Comiendo')
    DORMIDO = 'DORMIDO', _('Dormido')
    ENFERMO = 'ENFERMO', _('Enfermo')
    ESTRESADO = 'ESTRESADO', _('Estresado')
    HAMBRIENTO = 'HAMBRIENTO', _('Hambriento')
    HERIDO = 'HERIDO', _('Herido')
    NORMAL = 'NORMAL', _('Normal')


class TipoDieta(models.TextChoices):
    CARNIVORE = 'CARNIVORE', _('Carnívoro')
    HERBIVORE = 'HERBIVORE', _('Herbívoro')
    OMNIVORE = 'OMNIVORE', _('Omnívoro')


class TipoCuerpo(models.TextChoices):
    INVERTEBRADO = 'INVERTEBRADO', _('Invertebrado')
    VERTEBRADO = 'VERTEBRADO', _('Vertebrado')


class Zona(models.TextChoices):
    ESTE = 'ESTE', _('Este')
    NORTE = 'NORTE', _('Norte')
    OESTE = 'OESTE', _('Oeste')
    SUR = 'SUR', _('Sur')


class TipoAlimento(models.TextChoices):
    CARNE = 'CARNE', _('Carne')
    PESCADO = 'PESCADO', _('Pescado')
    HIERBA = 'HIERBA', _('Hierba')
    FRUTA = 'FRUTA', _('Fruta')


class Persona(models.Model):
    cedula = models.CharField(max_length=10, null=True, blank=True, default='0')
    nombre = models.CharField(max_length=200, default='Nombre desconocido')
    edad = models.IntegerField(default=0)

    class Meta:
        abstract = True  # Esto define que no se cree una tabla para Persona.

    def mostrar_datos(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}"


class Empleado(Persona):
    salario = models.FloatField()
    fecha_ingreso = models.DateField()
    zona = models.CharField(max_length=10, choices=Zona.choices, default=Zona.ESTE)

    def __str__(self):
        return f"Empleado: {self.nombre}"


class Guia(Empleado):
    clientes = models.ManyToManyField('Cliente', related_name='guias')
    recorrido = models.CharField(max_length=10, choices=Zona.choices, default=Zona.ESTE)

    def __str__(self):
        return f"Guía: {self.nombre} - Recorrido: {self.recorrido}"


class Cuidador(Empleado):
    animales_a_cargo = models.ManyToManyField('Animal', related_name='cuidadores')

    def cuidar_animal(self, animal):
        return f"{self.nombre} está cuidando al animal {animal.nombre} "

    def __str__(self):
        return f"Cuidador: {self.nombre}"


class Direction(models.Model):
    calle = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=20, blank=True, null=True)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.calle}, {self.ciudad}, {self.pais}"


class Zoological(models.Model):
    nombre = models.CharField(max_length=100)
    direction = models.OneToOneField(Direction, on_delete=models.CASCADE, related_name="zoological")
    capacidad = models.IntegerField()  # Capacidad máxima de animales o visitantes
    horario_apertura = models.CharField(max_length=100)  # Horarios de apertura
    description = models.TextField(blank=True, null=True)  # Descripción adicional del zoológico

    def __str__(self):
        return f"{self.nombre} - {self.direction}"


class Animal(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del animal
    especie = models.CharField(max_length=100)  # Especie del animal (ejemplo: León, Tigre)
    edad = models.IntegerField()  # Edad del animal (en años)
    estado = models.CharField(max_length=100, choices=Estado.choices, default=Estado.NORMAL)
    dieta = models.CharField(max_length=100, choices=TipoDieta.choices, default=TipoDieta.CARNIVORE)
    cuerpo = models.CharField(max_length=100, choices=TipoCuerpo.choices, default=TipoCuerpo.VERTEBRADO)
    zona = models.CharField(max_length=100, choices=Zona.choices, default=Zona.ESTE)

    def __str__(self):
        return f"{self.nombre} - {self.especie}"


class Veterinario(Empleado):
    especialidad = models.CharField(max_length=100)
    animales_asignados = models.ManyToManyField('Animal', related_name='veterinarios')

    def __str__(self):
        return f"Veterinario: {self.nombre} - Especialidad: {self.especialidad} - Cédula: {self.cedula}"


class HistorialMedico(models.Model):
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE, related_name='historial_medico')
    diagnostico = models.TextField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal} - {self.diagnostico}"


class Cliente(Persona):
    boletos_comprados = models.ManyToManyField('Boleto', related_name='clientes')

    def comprar_boleto(self, fecha_visita, valor):
        # Crear un nuevo boleto y asociarlo al cliente
        boleto = Boleto.objects.create(
            fecha_visita=fecha_visita,
            valor=valor
        )
        self.boletos_comprados.add(boleto)
        return f"Boleto comprado para la fecha {fecha_visita} por ${valor}"

    def listar_information(self):
        # Retorna información sobre los boletos comprados
        return [f"Boleto #{boleto.numero} - Fecha: {boleto.fecha_visita}, Valor: ${boleto.valor}"
                for boleto in self.boletos_comprados.all()]

    def __str__(self):
        return f"Cliente: {self.nombre} - {self.cedula}"


class Boleto(models.Model):
    contador = models.AutoField(primary_key=True)  # ID único para cada boleto
    fecha_visita = models.DateField()
    valor = models.FloatField()
    numero = models.PositiveIntegerField(unique=True)

    def save(self, *args, **kwargs):
        # Generar un número único para el boleto si no está definido
        if not self.numero:
            self.numero = self.contador
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Boleto #{self.numero} - Fecha: {self.fecha_visita}, Valor: ${self.valor}"


class PersonalAdministrativo(Empleado):
    departamento = models.CharField(max_length=100)

    def __str__(self):
        return f"Personal Administrativo: {self.nombre} - Departamento: {self.departamento}"


class PersonalLimpieza(Empleado):
    jaulas = models.ManyToManyField('Jaula', related_name='personal_limpieza')

    def limpiar_jaula(self, numero_jaula):
        """
        Limpia una jaula específica.

        Args:
            numero_jaula (int): Número de la jaula a limpiar.

        Returns:
            str: Mensaje confirmando la limpieza.
        """
        return f"La jaula número {numero_jaula} ha sido limpiada correctamente por {self.nombre}."


class Jaula(models.Model):
    zoological = models.ForeignKey('Zoological', on_delete=models.CASCADE, related_name='jaulas')
    capacidad = models.IntegerField()
    numero_jaula = models.CharField(max_length=10, unique=True)
    esta_limpio = models.BooleanField(default=True)

    def __str__(self):
        return f"Jaula: {self.numero_jaula}"
