from django.db import models
from decimal import Decimal

# Create your models here.

class Estudiante(models.Model):
    opciones_tipo_estudiante = (
        ('becado', 'Estudiante Becado'),
        ('no-becado', 'Estudiante No Becado'),
        )

    nombre = models.CharField("Nombre de estudiante", max_length=30)
    apellido = models.CharField(max_length=30)
    cedula = models.CharField(max_length=30, unique=True)
    edad = models.IntegerField("edad de estudiante") # Verbose field names
    tipo_estudiante = models.CharField(max_length=30, \
            choices=opciones_tipo_estudiante)
    modulos = models.ManyToManyField('Modulo', through='Matricula')


    def __str__(self):
        return "%s - %s - %s - edad: %d - tipo: %s" % (self.nombre,
                self.apellido,
                self.cedula,
                self.edad,
                self.tipo_estudiante)

    @property
    def matriculas_inscritas(self):
        return self.lasmatriculas.all()

    @property
    def detalle_matriculas_inscritas(self):
        return [
            f"Módulo: {matricula.modulo.nombre} - Costo: ${matricula.costo}"
            for matricula in self.matriculas_inscritas
        ]

    @property
    def costo_total_matriculas(self):
        return sum((matricula.costo for matricula in self.matriculas_inscritas), Decimal('0.00'))

class Modulo(models.Model):
    """
    """
    opciones_modulo = (
        ('1', 'Primero'),
        ('2', 'Segundo'),
        ('3', 'Tercero'),
        ('4', 'Cuarto'),
        ('5', 'Quinto'),
        ('6', 'Sexto'),
        )

    nombre = models.CharField(max_length=30, \
            choices=opciones_modulo)
    estudiantes = models.ManyToManyField(Estudiante, through='Matricula')

    def __str__(self):
        return "Módulo: %s" % (self.nombre)

class Matricula(models.Model):
    """
    Representa la matrícula de un estudiante en un módulo.
    """
    estudiante = models.ForeignKey(Estudiante, related_name='lasmatriculas',
            on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, related_name='lasmatriculas',
            on_delete=models.CASCADE)
    comentario = models.CharField(max_length=200)
    costo = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # nuevo campo

    def __str__(self):
        return "Matricula: Estudiante(%s) - Modulo(%s)" % \
                (self.estudiante, self.modulo.nombre)
