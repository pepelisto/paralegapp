from django.contrib import admin
from .models import Caso, Estado, Usuario_t_caso, Usuario_T_estado, Pago, Tareas, Casos_t_cuadernos, \
    Litigante, Profile, Notificacion_caso, Ute_invitado, Tareas_invitado, Anotacion, Tribunal
from django.contrib.auth.models import User


admin.site.register(Caso)
admin.site.register(Estado)
admin.site.register(Usuario_t_caso)
admin.site.register(Usuario_T_estado)
admin.site.register(Pago)
admin.site.register(Tareas)
admin.site.register(Casos_t_cuadernos)
admin.site.register(Litigante)
admin.site.register(Profile)
admin.site.register(Notificacion_caso)
admin.site.register(Ute_invitado)
admin.site.register(Tareas_invitado)
admin.site.register(Anotacion)
admin.site.register(Tribunal)
