from django.db import models
from django import forms
from django.contrib.auth.models import User, Permission
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, help_text='Telefono' , null=True, blank=True)
    direccion = models.CharField(max_length=20, help_text='Direccion', null=True, blank=True)
    tipos = (
        ('master', 'master'),
        ('usuario', 'usuario'))
    tipo_cuenta = models.CharField(max_length=20, help_text='Cuenta', choices = tipos, null=True, blank=True)
    empresa = models.CharField(max_length=50, help_text='Empresa', null=True, blank=True)
    def __str__(self):
        return self.user.username

class Tribunal(models.Model):
    tribunal = models.CharField(max_length=52)
    def __str__(self):
        return  self.tribunal

class Caso(models.Model):
     rol = models.CharField(max_length=1, help_text='Rol')
     numero = models.PositiveIntegerField(help_text='Numero')
     year = models.PositiveIntegerField(help_text='Año')
     caratulado = models.CharField(max_length=100, null=True, blank=True)
     fecha_ingreso = models.DateField(max_length=20, blank=True, null=True)
     tribunal = models.ForeignKey(Tribunal, on_delete=models.CASCADE, help_text='Tribunal')
     dte_nombre = models.CharField(max_length=100, null=True, blank=True)
     last_chek = models.DateTimeField(blank=True, null=True)
     last_chenge_coment = models.CharField(max_length=60, null=True, blank=True)
     last_change = models.DateTimeField(blank=True, null=True)
     ubicacion = models.CharField(max_length=80, null=True, blank=True)
     proc = models.CharField(max_length=100, null=True, blank=True)
     est_adm = models.CharField(max_length=60, null=True, blank=True)###agregar ruta de la carpetita
     etapa = models.CharField(max_length=60, null=True, blank=True)
     archivo = models.CharField(max_length=400, null=True, blank=True)
     estprocnmenos1 = models.CharField(max_length=60, null=True, blank=True)
     estproceso = models.CharField(max_length=60, null=True, blank=True)
     def __str__(self):
          return self.rol + ' - ' + str(self.numero) + ' - ' + str(self.year) + ' - ' + str(self.tribunal)

class Caso_t_archivo(models.Model):
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    archivo = models.CharField(max_length=400, null=True, blank=True)

class Casos_t_cuadernos(models.Model):
     fecha_creacion = models.DateField(null=True, blank=True)
     caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
     cuaderno = models.CharField(max_length=60, null=True, blank=True)
     numero = models.PositiveIntegerField(null=True, blank=True)
     estado_n = models.PositiveIntegerField(null=True, blank=True)
     estado_previo_n = models.PositiveIntegerField(null=True, blank=True)
     def __str__(self):
         return str(self.numero) + ' - ' + self.cuaderno
     def get_absolute_url(self):
          return reverse('paralegapp:detalle_caso', kwargs={'pkc': self.pk, 'num': self.numero})

class Notificacion_caso(models.Model):
     fecha_creacion = models.DateField(null=True, blank=True)
     caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
     est_not = models.CharField(max_length=60, null=True, blank=True)
     fectram = models.CharField(max_length=30, null=True, blank=True)
     rol = models.CharField(max_length=30, null=True, blank=True)
     ruc = models.CharField(max_length=30, null=True, blank=True)
     tip_part = models.CharField(max_length=60, null=True, blank=True)
     nombre = models.CharField(max_length=60, null=True, blank=True)
     tramite = models.PositiveIntegerField(null=True, blank=True)
     obs_fallido = models.CharField(max_length=60, null=True, blank=True)

class Litigante(models.Model):
    fecha_creacion = models.DateField(null=True, blank=True)
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    participante = models.CharField(max_length=60, null=True, blank=True)
    rut = models.CharField(max_length=30, null=True, blank=True)
    persona = models.CharField(max_length=60, null=True, blank=True)
    nombre = models.CharField(max_length=60, null=True, blank=True)

class Exohorto(models.Model):
    fecha_creacion = models.DateField(null=True, blank=True)
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    tipo_exohorto = models.CharField(max_length=60, null=True, blank=True)
    rol_origen = models.CharField(max_length=30, null=True, blank=True)
    rol_destino = models.CharField(max_length=30, null=True, blank=True)
    fecha_ord_exohorto = models.DateField()
    fecha_ing_exohorto = models.DateField()
    tribunal_destino= models.CharField(max_length=60, null=True, blank=True)
    estado_exohorto = models.CharField(max_length=60, null=True, blank=True)

class Esc_por_resolver(models.Model):
    fecha_creacion = models.DateField(null=True, blank=True)
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
    doc = models.CharField(max_length=60, null=True, blank=True)
    anexo = models.CharField(max_length=300, null=True, blank=True)
    fecha_ing = models.DateField()
    tipo_escrito = models.CharField(max_length=30, null=True, blank=True)
    solicitante = models.CharField(max_length=60, null=True, blank=True)
    ###agregar Tipo escrito

class Usuario_t_caso(models.Model):
     fecha_inicio = models.DateTimeField(null=True, blank=True)
     fecha_fin = models.DateField(null=True, blank=True)
     meses_seguidos = models.PositiveIntegerField(null=True, blank=True)
     meses_pagados = models.PositiveIntegerField(null=True, blank=True)
     caso = models.ForeignKey(Caso, on_delete=models.CASCADE)
     usuario = models.ForeignKey(User, on_delete=models.CASCADE)
     monto = models.PositiveIntegerField(null=True, blank=True)###integerfield
     favorito = models.BooleanField(default=False)
     horas = models.DecimalField(max_length=10, max_digits=5, decimal_places=1, default=0)
     def __str__(self):  #self.usuario.username
          return  self.usuario.username + ' - ' + self.caso.rol + ' - ' + str(self.caso.numero) + ' - ' + str(self.caso.year) + ' - ' + self.caso.tribunal.tribunal
     def get_absolute_url(self):
          return reverse('paralegapp:detalle_caso', kwargs={'pk': self.pk})

class Estado(models.Model):
     folio = models.CharField(max_length=30, null=True, blank=True)
     etapa = models.CharField(max_length=60, null=True, blank=True)
     tramite = models.CharField(max_length=60, null=True, blank=True)
     desc_tramite = models.CharField(max_length=300, null=True, blank=True)
     numero_archivo = models.PositiveIntegerField(null=True, blank=True)
     archivo = models.CharField(max_length=400, null=True, blank=True)
     tipoarchivo = models.CharField(max_length=10, null=True, blank=True)
     archivo_2 = models.CharField(max_length=60, null=True, blank=True)
     tipoarchivo_2 = models.CharField(max_length=10, null=True, blank=True)
     fecha_tramite = models.CharField(max_length=60, null=True, blank=True)
     cuaderno = models.ForeignKey(Casos_t_cuadernos, on_delete=models.CASCADE)
     doc = models.CharField(max_length=60, null=True, blank=True)
     foja = models.CharField(max_length=30, null=True, blank=True)
     def __str__(self):
         return str(self.pk) + ' - ' + self.folio + ' - ' + self.etapa + ' - ' + str(self.fecha_tramite) + ' - ' + str(self.cuaderno.caso)

class Usuario_T_estado(models.Model):
     estados_estados = (
          ('previo', 'previo'),
          ('sinfinalizar', 'sinfinalizar'),
          ('Ingresado', 'Ingresado'),
          ('En proceso', 'En proceso'),
          ('Terminado', 'Terminado'),
     )
     estado_estado = models.CharField(max_length=20, choices=estados_estados, default='Ingresado') #rojo, amarillo, verde
     anotaciones = models.TextField(max_length=1000, null=True, blank=True)
     fecha_ingreso = models.DateField()
     fecha_toma = models.DateField(null=True, blank=True)
     fecha_finalizado = models.DateField(null=True, blank=True)
     estado_caso = models.ForeignKey(Estado, on_delete=models.CASCADE)
     usuario = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
     plazo = models.DateField(max_length=20, null=True, blank=True)
     caso_activo = models.BooleanField(default=True)
     def get_absolute_url(self):
          return reverse('paralegapp:detalle_actualizacion', kwargs={'pka': self.pk})
     def __str__(self):
         return self.usuario.username + ' - ' + str(self.estado_caso.cuaderno.caso) + ' - ' + str(self.estado_caso)

class Ute_invitado(models.Model):
    fecha_invitacion = models.DateField(max_length=20)
    usuario = models.ForeignKey(Usuario_T_estado, on_delete=models.CASCADE)
    invitado = models.ForeignKey(User, on_delete=models.CASCADE)

class Tareas(models.Model):
    usuario = models.ForeignKey(Usuario_T_estado, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    desc = models.CharField(max_length=300, null=True, blank=True)
    comentarios = models.TextField(max_length=300, null=True, blank=True)
    numero = models.PositiveIntegerField(null=True, blank=True)
    horas = models.DecimalField(max_length=10, max_digits=5, decimal_places=1, default=0)
    estados = (
        ('Por realizar', 'Por realizar'),
        ('En proceso', 'En proceso'),
        ('Finalizada', 'Finalizada'),)
    estado = models.CharField(max_length=20, choices=estados, default='Por realizar')
    fecha_creacion = models.DateField()
    fecha_tarea = models.DateField()
    fecha_plazo = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True, default=None)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    importancias = (
        ('Baja', 'Baja'),
        ('Intermedia', 'Intermedia'),
        ('Urgente', 'Urgente'),
        ('Prioritario', 'Prioritario'),)
    importancia = models.CharField(max_length=20, choices=importancias)

class Tareas_invitado(models.Model):
    fecha_invitacion = models.DateField()
    tarea = models.ForeignKey(Tareas, on_delete=models.CASCADE)
    invitado = models.ForeignKey(User, on_delete=models.CASCADE)

class Anotacion(models.Model):
    tarea = models.ForeignKey(Tareas, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField(max_length=300)
    fecha = models.DateTimeField()
    tipo = models.CharField(max_length=20)

class Pago(models.Model):
     fecha_pago = models.DateField(null=True, blank=True)
     monto = models.PositiveIntegerField(null=True, blank=True)
     numero_casos = models.PositiveIntegerField(null=True, blank=True)
     mes_correspondiente = models.DateField(max_length=20, null=True, blank=True)
     estados = (
          ('Pendiente', 'Pendiente'),
          ('Pagado', 'Pagado'),
     )
     estado_pago = models.CharField(max_length=20, choices=estados, null=True, blank=True)
     metodo_pago = models.CharField(max_length=20, null=True, blank=True)
     usuario = models.ForeignKey(User, default=1, on_delete=models.CASCADE) #dependiendo del tipo de pago

