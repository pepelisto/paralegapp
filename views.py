from django.db.models import Sum, Count
from .models import Caso, Estado, Usuario_T_estado, Usuario_t_caso, User, Casos_t_cuadernos, Tribunal, \
    Litigante, Notificacion_caso, Exohorto, Esc_por_resolver, Tareas, Tareas_invitado, Ute_invitado, Anotacion, Profile
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, CasoForm, ValueForm, PlazoForm, TareaForm, NotaForm, HorasForm
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from django.views.generic import ListView, DetailView, FormView

from django.core.mail import send_mail

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

hoy = datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def signup(request):
   if request.method == 'POST':
       form = UserRegisterForm(request.POST)
       # print(form.errors.as_data())
       if form.is_valid():
           user = form.save(commit=False)
           user.is_active = False
           user.save()
           pro = Profile(user=user, empresa=None, tipo_cuenta='usuario')
           pro.save()
           current_site = get_current_site(request)
           mail_subject = 'Activate your account.'
           message = render_to_string('casos/acc_active_email.html', {
               'user': user,
               'domain': current_site.domain,
               'uid': urlsafe_base64_encode(force_bytes(user.id)),
               'token': account_activation_token.make_token(user),
           })
           to_email = form.cleaned_data.get('email')
           email = EmailMessage(
               mail_subject, message, to=[to_email]
           )
           email.send()
           return render(request, 'casos/esperandoconfirmacion.html')
   else:
       form = UserRegisterForm()
   return render(request, 'casos/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'casos/activado.html')
    else:
        return HttpResponse('Link de activación invalido')


def home(request):
    return render(request, 'casos/home.html')

def ayuda(request):
    return render(request, 'casos/ayuda.html')

@login_required


def usuario(request):
    usuario_activo = request.user
    usuario = Profile.objects.get(user=usuario_activo)
    mis_casos_a = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_fin=None).count()
    mis_casos_t = Usuario_t_caso.objects.filter(usuario=usuario_activo).count()
    return render(request, 'casos/usuario.html', {'usuario': usuario, 'mis_casos_a':mis_casos_a, 'mis_casos_t': mis_casos_t, 'usuario_activo': usuario_activo})

def inicio(request):
   usuario_activo = request.user
   usuario = Profile.objects.get(user=usuario_activo)
   mis_estados = Usuario_T_estado.objects.filter(usuario=usuario_activo, caso_activo=True).order_by('-fecha_ingreso').exclude(estado_estado='previo').exclude(estado_estado='Terminado')[:15]
   con_est = Usuario_T_estado.objects.filter(usuario=usuario_activo).exclude(estado_estado='previo').exclude(estado_estado='Terminado').count()
   tareas = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__usuario__caso_activo=True).order_by('-tarea__fecha_creacion')[:15]
   con_ta = Tareas_invitado.objects.filter(invitado=usuario_activo).exclude(tarea__estado='Finalizada').count()
   comentarios = Anotacion.objects.filter(tarea__tareas_invitado__invitado=usuario_activo, tipo='nota', tarea__usuario__caso_activo=True).exclude(usuario=usuario_activo).order_by('-fecha')[:15]
   mis_casos = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_fin=None).count()
   months = ['zero', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
   now = date.today()
   mes00 = now.month
   ano00= now.year
   mes11 = now.month - 1
   mes22 = date.today().month - 2
   mes0 = months[now.month]
   mes1 = months[now.month - 1]
   if  mes1 == 'Dic':
      ano11 = now.year - 1
   else:
      ano11 = now.year
   mes2 = months[now.month - 2]
   if mes2 == 'Nov' or mes2 == 'Dic':
      ano22 = now.year - 1
   else:
      ano22 = now.year
   ca_in_0 = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_inicio__month=mes00, fecha_inicio__year=ano00).count()
   ca_in_1 = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_inicio__month=mes11, fecha_inicio__year=ano11).count()
   ca_in_2 = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_inicio__month=mes22, fecha_inicio__year=ano22).count()
   ca_fi_0 = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_fin__month=mes00, fecha_fin__year=ano00).count()
   ca_fi_1 = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_fin__month=mes11, fecha_fin__year=ano11).count()
   ca_fi_2 = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_fin__month=mes22, fecha_fin__year=ano22).count()

   ac_in_0 = Usuario_T_estado.objects.filter(usuario=usuario_activo, fecha_ingreso__month= mes00, fecha_ingreso__year=ano00).count()
   ac_in_1 = Usuario_T_estado.objects.filter(usuario=usuario_activo, fecha_ingreso__month=mes11,fecha_ingreso__year=ano11).count()
   ac_in_2 = Usuario_T_estado.objects.filter(usuario=usuario_activo, fecha_ingreso__month=mes22,fecha_ingreso__year=ano22).count()
   ac_fi_0 = Usuario_T_estado.objects.filter(usuario=usuario_activo, fecha_finalizado__month= mes00, fecha_finalizado__year=ano00).count()
   ac_fi_1 = Usuario_T_estado.objects.filter(usuario=usuario_activo, fecha_finalizado__month=mes11,fecha_finalizado__year=ano11).count()
   ac_fi_2 = Usuario_T_estado.objects.filter(usuario=usuario_activo, fecha_finalizado__month=mes22,fecha_finalizado__year=ano22).count()

   ta_in_0 = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__fecha_creacion__month=mes00, tarea__fecha_creacion__year=ano00).count()
   ta_in_1 = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__fecha_creacion__month=mes11,tarea__fecha_creacion__year=ano11).count()
   ta_in_2 = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__fecha_creacion__month=mes22,tarea__fecha_creacion__year=ano22).count()
   ta_fi_0 = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__fecha_fin__month=mes00, tarea__fecha_fin__year=ano00, tarea__estado='Finalizada').count()
   ta_fi_1 = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__fecha_fin__month=mes11, tarea__fecha_fin__year=ano11, tarea__estado='Finalizada').count()
   ta_fi_2 = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__fecha_fin__month=mes22, tarea__fecha_fin__year=ano22, tarea__estado='Finalizada').count()

   #send_mail('login prueba', 'You have loged in', 'paralegapp@gmail.com', ['martinmoran422@gmail.com'], fail_silently=False)
   return render(request, 'casos/inicio.html', {
       'tareas':tareas, 'usuario':usuario,'mis_estados':mis_estados,'con_ta':con_ta, 'con_est':con_est ,'comentarios': comentarios,'mis_casos': mis_casos,
       'ca_in_0':ca_in_0,'ca_in_1': ca_in_1,'ca_in_2':ca_in_2,'ca_fi_1': ca_fi_1,'ca_fi_2':ca_fi_2,'ca_fi_0':ca_fi_0,
       'ac_in_0':ac_in_0, 'ac_in_1':ac_in_1, 'ac_in_2':ac_in_2, 'ac_fi_0':ac_fi_0, 'ac_fi_1':ac_fi_1, 'ac_fi_2':ac_fi_2,
       'ta_in_0': ta_in_0,'ta_in_1': ta_in_1,'ta_in_2': ta_in_2, 'ta_fi_0': ta_fi_0, 'ta_fi_1': ta_fi_1, 'ta_fi_2': ta_fi_2,
        'usuario_activo': usuario_activo, 'mes0': mes0, 'mes1': mes1, 'mes2': mes2
   })

def gestion(request):
    usuario_activo = request.user
    usuario = Profile.objects.get(user=usuario_activo)
    con_est = Usuario_T_estado.objects.filter(usuario=usuario_activo).exclude(estado_estado='Terminado').count()
    con_ta = Tareas_invitado.objects.filter(invitado=usuario_activo).exclude(tarea__estado='Finalizada').count()
    mis_casos = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_fin=None).count()
    months = ['zero', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    now = date.today()
    mes00 = now.month
    ano00 = now.year
    mes11 = now.month - 1
    mes22 = date.today().month - 2
    mes0 = months[now.month]
    mes1 = months[now.month - 1]
    if mes1 == 'Dic':
        ano11 = now.year - 1
    else:
        ano11 = now.year
    mes2 = months[now.month - 2]
    if mes2 == 'Nov' or mes2 == 'Dic':
        ano22 = now.year - 1
    else:
        ano22 = now.year
    ca_in_0 = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_inicio__month=mes00,fecha_inicio__year=ano00).count()
    ca_in_1 = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_inicio__month=mes11,fecha_inicio__year=ano11).count()
    ca_in_2 = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_inicio__month=mes22,fecha_inicio__year=ano22).count()
    ca_fi_0 = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_fin__month=mes00,fecha_fin__year=ano00).count()
    ca_fi_1 = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_fin__month=mes11,fecha_fin__year=ano11).count()
    ca_fi_2 = Usuario_t_caso.objects.filter(usuario=usuario_activo, fecha_fin__month=mes22,fecha_fin__year=ano22).count()

    ac_in_0 = Usuario_T_estado.objects.filter(usuario=usuario_activo, fecha_ingreso__month=mes00,fecha_ingreso__year=ano00).count()
    ac_in_1 = Usuario_T_estado.objects.filter(usuario=usuario_activo, fecha_ingreso__month=mes11,fecha_ingreso__year=ano11).count()
    ac_in_2 = Usuario_T_estado.objects.filter(usuario=usuario_activo, fecha_ingreso__month=mes22,fecha_ingreso__year=ano22).count()
    ac_fi_0 = Usuario_T_estado.objects.filter(usuario=usuario_activo, fecha_finalizado__month=mes00,fecha_finalizado__year=ano00).count()
    ac_fi_1 = Usuario_T_estado.objects.filter(usuario=usuario_activo, fecha_finalizado__month=mes11,fecha_finalizado__year=ano11).count()
    ac_fi_2 = Usuario_T_estado.objects.filter(usuario=usuario_activo, fecha_finalizado__month=mes22,fecha_finalizado__year=ano22).count()

    ta_in_0 = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__fecha_creacion__month=mes00,tarea__fecha_creacion__year=ano00).count()
    ta_in_1 = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__fecha_creacion__month=mes11,tarea__fecha_creacion__year=ano11).count()
    ta_in_2 = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__fecha_creacion__month=mes22,tarea__fecha_creacion__year=ano22).count()
    ta_fi_0 = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__fecha_fin__month=mes00,tarea__fecha_fin__year=ano00, tarea__estado='Finalizada').count()
    ta_fi_1 = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__fecha_fin__month=mes11,tarea__fecha_fin__year=ano11, tarea__estado='Finalizada').count()
    ta_fi_2 = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__fecha_fin__month=mes22,tarea__fecha_fin__year=ano22, tarea__estado='Finalizada').count()

    return render(request, 'casos/gestion.html', {
         'usuario': usuario, 'mis_estados': mis_estados, 'con_ta': con_ta, 'con_est': con_est, 'mis_casos': mis_casos,
        'ca_in_0': ca_in_0, 'ca_in_1': ca_in_1, 'ca_in_2': ca_in_2, 'ca_fi_1': ca_fi_1, 'ca_fi_2': ca_fi_2,'ca_fi_0': ca_fi_0,
        'ac_in_0': ac_in_0, 'ac_in_1': ac_in_1, 'ac_in_2': ac_in_2, 'ac_fi_0': ac_fi_0, 'ac_fi_1': ac_fi_1,'ac_fi_2': ac_fi_2,
        'ta_in_0': ta_in_0, 'ta_in_1': ta_in_1, 'ta_in_2': ta_in_2, 'ta_fi_0': ta_fi_0, 'ta_fi_1': ta_fi_1,'ta_fi_2': ta_fi_2,
        'usuario_activo': usuario_activo, 'mes0': mes0, 'mes1': mes1, 'mes2': mes2
    })

###lista de casos OK
class CasoListView(ListView):
   model = Usuario_t_caso
   template_name = 'casos/casos.html'
   ordering = '-caso__fecha_ingreso' ###
   context_object_name = 'mis_casos'
   #paginate_by = 11
   def get_queryset(self):
      mis_casos = super().get_queryset()
      return mis_casos.filter(usuario=self.request.user, fecha_fin=None)
   def get_ordering(self):
      self.order = self.request.GET.get('order', 'asc')
      selected_ordering = self.request.GET.get('ordering', '-caso__fecha_ingreso')
      if self.order == "desc":
         selected_ordering = "-" + selected_ordering
      return selected_ordering
   def get_context_data(self, *args, **kwargs):
      context = super(CasoListView, self).get_context_data(*args, **kwargs)
      ###context['mis_casos'] = Usuario_t_caso.objects.filter(usuario=self.request.user).order_by('-caso__fecha_ingreso')
      context['current_order'] = self.get_ordering()
      context['order'] = self.order
      context['todos'] = 0
      context['ruta'] = 'paralegapp:mis_casos'
      return context

class CasoListViewTodos(ListView):
   model = Usuario_t_caso
   template_name = 'casos/casos.html'
   ordering = '-caso__fecha_ingreso' ###
   context_object_name = 'mis_casos'
   #paginate_by = 11
   def get_queryset(self):
      mis_casos = super().get_queryset()
      return mis_casos.filter(usuario=self.request.user)
   def get_ordering(self):
      self.order = self.request.GET.get('order', 'asc')
      selected_ordering = self.request.GET.get('ordering', '-caso__fecha_ingreso')
      if self.order == "desc":
         selected_ordering = "-" + selected_ordering
      return selected_ordering
   def get_context_data(self, *args, **kwargs):
      context = super(CasoListViewTodos, self).get_context_data(*args, **kwargs)
      ###context['mis_casos'] = Usuario_t_caso.objects.filter(usuario=self.request.user).order_by('-caso__fecha_ingreso')
      context['current_order'] = self.get_ordering()
      context['order'] = self.order
      context['todos'] = 1
      context['ruta'] = 'paralegapp:mis_casos_todos'
      return context

def FinalizarCausa(request, pkc, ac):
    usuario_activo = request.user
    micaso = Usuario_t_caso.objects.get(pk=pkc)
    mis_estados = Usuario_T_estado.objects.filter(usuario=usuario_activo, estado_caso__cuaderno__caso__pk=micaso.caso.pk)
    usuario_estado = micaso.usuario
    if usuario_activo == usuario_estado:
        if ac == 1:
            micaso.fecha_fin = date.today()
            for estado in mis_estados:
                estado.caso_activo = False
                estado.save()
            messages.success(request, f'Haz dejado de seguir esta causa')
        if ac == 0:
            micaso.fecha_fin = None
            for estado in mis_estados:
                estado.caso_activo = True
                estado.save()
            messages.success(request, f'Haz vuelto a seguir la causa nuevamente')
        micaso.save()
        return redirect('paralegapp:detalle_caso', pk=pkc, num=1)

def CasoFavorito(request,pkc, f):
    usuario_activo = request.user
    caso = Usuario_t_caso.objects.get(pk=pkc)
    usuario_caso = caso.usuario
    if usuario_activo == usuario_caso:
        if caso.favorito == False:
            caso.favorito = True
        else:
            caso.favorito = False
        caso.save()
        if f == 1:
            return redirect('paralegapp:mis_casos')
        if f == 2:
            return redirect('paralegapp:detalle_caso', pk=pkc, num=1)
        if f == 3:
            return redirect('paralegapp:mis_casos_todos')
####casos detalles OK ### muy bueno y casi listo, solo faltaa agregar el separador de miles para que se vea mejor

def casoDetail(request, pk, num): ##para las historias
   usuario_activo = request.user
   micaso = Usuario_t_caso.objects.get(pk=pk)
   usuario_caso = micaso.usuario
   if usuario_activo == usuario_caso:
       usuario = Profile.objects.get(user=usuario_activo)
       caso = micaso.caso
       caso_id = caso.id
       participantes = Usuario_t_caso.objects.filter(caso=micaso.caso, usuario__profile__empresa=usuario.empresa)
       try:
          cuaderno = Casos_t_cuadernos.objects.get(numero=num, caso=caso_id)
          cuaderno_id = cuaderno.id
          cuadernos = Casos_t_cuadernos.objects.filter(caso=caso_id)
          #estados = Estado.objects.filter(cuaderno__caso=caso_id, cuaderno=cuaderno_id)
          mis_estados = Usuario_T_estado.objects.filter(usuario=usuario_activo, estado_caso__cuaderno__caso=micaso.caso.pk,
                          estado_caso__cuaderno=cuaderno_id).order_by('-estado_caso__numero_archivo').annotate(ta=Count('tareas'), ht=Sum('tareas__horas'))
          est_act = Usuario_T_estado.objects.filter(usuario=usuario_activo, estado_caso__cuaderno__caso=micaso.caso.pk, estado_estado= 'Ingresado' or 'En proceso').count()
          tareas = Tareas.objects.filter(usuario__usuario=usuario_activo, usuario__estado_caso__cuaderno__caso=micaso.caso.pk)
          horas = tareas.aggregate(Sum('horas'))['horas__sum']
          cuX = 1
          if request.method == 'POST':
              form = ValueForm(request.POST)
              if form.is_valid():
                  valory = form.cleaned_data.get('monto')
                  micaso.monto = valory
                  micaso.save()
                  messages.success(request, f'Valor de  {valory}  agregado al caso')
                  return redirect('paralegapp:detalle_caso', pk=micaso.pk, num=cuaderno_id)
          else:
              form = ValueForm()
              return render(request, 'casos/historias_caso.html', {'form': form, 'micaso': micaso, 'caso': caso, 'mis_estados':mis_estados,'usuario':usuario, 'est_act':est_act,
                                             'cuadernos': cuadernos,'cuaderno': cuaderno, 'cuX': cuX, 'horas':horas, 'tareas':tareas, 'participantes':participantes})
       except:
          cuX = 0
       if request.method == 'POST':
         form = ValueForm(request.POST)
         if form.is_valid():
            valory = form.cleaned_data.get('monto')
            micaso.monto = valory
            micaso.save()
            messages.success(request, f'Valor de  {valory}  agregado al caso')
            return redirect('paralegapp:detalle_caso', pk=micaso.pk, num=1)
       else:
         form = ValueForm()
         return render(request, 'casos/historias_caso.html', {'form': form, 'micaso': micaso, 'caso': caso, 'cuX': cuX,
                                                              'participantes':participantes,'usuario':usuario})
   else:
       messages.warning(request, f'Caso no corresponde a "tus casos" o no has iniciado sesión')
       return render(request, 'casos/historias_caso.html')

def casoLitigantes(request, pk, num): ##para las historias
   usuario_activo = request.user
   micaso = Usuario_t_caso.objects.get(pk=pk)
   usuario_caso = micaso.usuario
   if usuario_activo == usuario_caso:
       caso = micaso.caso
       caso_id = caso.id
       cuadernos = Casos_t_cuadernos.objects.filter(caso=caso_id)
       litigantes = Litigante.objects.filter(caso=caso_id)
       if litigantes.exists():
           X = 1
       else:
           X = 0
       if request.method == 'POST':
         form = ValueForm(request.POST)
         if form.is_valid():
            valory = form.cleaned_data.get('monto')
            micaso.monto = valory
            micaso.save()
            messages.success(request, f'Valor de  {valory}  agregado al caso')
            return render(request, 'casos/litigantes_caso.html', {'form': form, 'micaso': micaso, 'caso':caso,'X':X,
                                             'litigantes': litigantes, 'cuadernos': cuadernos})
       else:
         form = ValueForm()
         return render(request, 'casos/litigantes_caso.html', {'form': form, 'micaso': micaso, 'caso': caso,'X':X,
                                             'litigantes': litigantes, 'cuadernos': cuadernos})
   else:
       messages.warning(request, f'Caso no corresponde a "tus casos" o no has iniciado sesión')
       return render(request, 'casos/historias_caso.html')

def casoNotificaciones(request, pk, num): ##para las historias
   usuario_activo = request.user
   micaso = Usuario_t_caso.objects.get(pk=pk)
   usuario_caso = micaso.usuario
   if usuario_activo == usuario_caso:
       caso = micaso.caso
       caso_id = caso.id
       cuadernos = Casos_t_cuadernos.objects.filter(caso=caso_id)
       notificaciones = Notificacion_caso.objects.filter(caso=caso_id)
       if notificaciones.exists():
           X = 1
       else:
           X = 0
       if request.method == 'POST':
         form = ValueForm(request.POST)
         if form.is_valid():
            valory = form.cleaned_data.get('monto')
            micaso.monto = valory
            micaso.save()
            messages.success(request, f'Valor de  {valory}  agregado al caso')
            return render(request, 'casos/notificaciones_caso.html', {'form': form, 'micaso': micaso, 'caso':caso,'X':X,
                                             'notificaciones': notificaciones, 'cuadernos': cuadernos})
       else:
         form = ValueForm()
         return render(request, 'casos/notificaciones_caso.html', {'form': form, 'micaso': micaso, 'caso': caso,'X':X,
                                             'notificaciones': notificaciones, 'cuadernos': cuadernos})
   else:
       messages.warning(request, f'Caso no corresponde a "tus casos" o no has iniciado sesión')
       return render(request, 'casos/historias_caso.html')

def casoExohortos(request, pk, num): ##para las historias
   usuario_activo = request.user
   micaso = Usuario_t_caso.objects.get(pk=pk)
   usuario_caso = micaso.usuario
   if usuario_activo == usuario_caso:
       caso = micaso.caso
       caso_id = caso.id
       cuadernos = Casos_t_cuadernos.objects.filter(caso=caso_id)
       exohortos = Exohorto.objects.filter(caso=caso_id)
       if exohortos.exists():
           X = 1
       else:
           X = 0
       if request.method == 'POST':
         form = ValueForm(request.POST)
         if form.is_valid():
            valory = form.cleaned_data.get('monto')
            micaso.monto = valory
            micaso.save()
            messages.success(request, f'Valor de  {valory}  agregado al caso')
            return render(request, 'casos/exohortos_caso.html', {'form': form, 'micaso': micaso, 'caso':caso,'X':X,
                                             'exohortos': exohortos, 'cuadernos': cuadernos})
       else:
         form = ValueForm()
         return render(request, 'casos/exohortos_caso.html', {'form': form, 'micaso': micaso, 'caso': caso,'X':X,
                                             'exohortos': exohortos, 'cuadernos': cuadernos})
   else:
       messages.warning(request, f'Caso no corresponde a "tus casos" o no has iniciado sesión')
       return render(request, 'casos/historias_caso.html')

def casoEsc(request, pk, num): ##para las historias
   usuario_activo = request.user
   micaso = Usuario_t_caso.objects.get(pk=pk)
   usuario_caso = micaso.usuario
   if usuario_activo == usuario_caso:
       caso = micaso.caso
       caso_id = caso.id
       cuadernos = Casos_t_cuadernos.objects.filter(caso=caso_id)
       escs = Esc_por_resolver.objects.filter(caso=caso_id)
       if escs.exists():
           X = 1
       else:
           X = 0
       if request.method == 'POST':
         form = ValueForm(request.POST)
         if form.is_valid():
            valory = form.cleaned_data.get('monto')
            micaso.monto = valory
            micaso.save()
            messages.success(request, f'Valor de  {valory}  agregado al caso')
            return render(request, 'casos/esc_caso.html', {'form': form, 'micaso': micaso, 'caso':caso,'X':X,
                                             'escs': escs, 'cuadernos': cuadernos})
       else:
         form = ValueForm()
         return render(request, 'casos/esc_caso.html', {'form': form, 'micaso': micaso, 'caso': caso,'X':X,
                                             'escs': escs, 'cuadernos': cuadernos})
   else:
       messages.warning(request, f'Caso no corresponde a "tus casos" o no has iniciado sesión')
       return render(request, 'casos/historias_caso.html')
###### hasta aqui casos detalles####

###para ir a la actualizacion del usuario del estado particular
def iractualizacion(request, pk):
    usuario_activo = request.user
    miestado = Usuario_T_estado.objects.get(estado_caso=pk, usuario=usuario_activo)
    miestado_id = miestado.pk
    usuario_estado = miestado.usuario
    if usuario_activo == usuario_estado:
        return redirect('paralegapp:detalle_actualizacion', pka=miestado_id)

###lista de actualizacion aun por mejorar
def mis_estados(request, orden, can):
   usuario_activo = request.user
   if can == 2:
       mis_estados = Usuario_T_estado.objects.filter(usuario=usuario_activo, caso_activo=True).order_by(orden).annotate(ta=Count('tareas'), ho=Sum('tareas__horas'))
   else:
       mis_estados = Usuario_T_estado.objects.filter(usuario=usuario_activo, caso_activo=True).order_by(orden).exclude(
           estado_estado='Terminado').exclude(estado_estado='previo').annotate(ta=Count('tareas'), ho=Sum('tareas__horas'))
   return render(request, 'casos/estados.html', {'mis_estados': mis_estados, 'orden':orden, 'hoy': date.today(), 'can':can})


###detalles de actualizaciones
def detalleActualizacion(request, pka): ##para las historias
   usuario_activo = request.user
   miestado = Usuario_T_estado.objects.get(pk=pka)
   usuario_estado = miestado.usuario
   if usuario_activo == usuario_estado:
      usuario = Profile.objects.get(user=usuario_activo)
      caso = miestado.estado_caso.cuaderno.caso
      micaso = Usuario_t_caso.objects.get(caso=caso, usuario=usuario_activo).pk
      tareas = Tareas.objects.filter(usuario=miestado.pk).annotate(i=Count('tareas_invitado'))
      ta_te = Tareas.objects.filter(usuario=miestado.pk, estado='Finalizada').count()
      horas = tareas.aggregate(Sum('horas'))['horas__sum']
      participantes = Usuario_t_caso.objects.filter(caso=miestado.estado_caso.cuaderno.caso, usuario__profile__empresa=usuario.empresa)
      if request.method == 'POST':
          form1 = PlazoForm(request.POST)
          form2 = TareaForm(request.POST)
          if form1.is_valid():
              plazoy = form1.cleaned_data.get('plazo')
              if plazoy != None:
                  if plazoy < date.today():
                      messages.success(request, f'Plazo no puede ser anterior a la fecha actual')
                      return redirect('paralegapp:detalle_actualizacion', pka=pka)
                  miestado.plazo = plazoy
                  miestado.save()
                  messages.success(request, f'Plazo para   {plazoy}  agregado a el estado')
                  return redirect('paralegapp:detalle_actualizacion', pka=pka)
          if form2.is_valid():
              nombre = form2.cleaned_data['nombre']
              desc = form2.cleaned_data['desc']
              comentarios = form2.cleaned_data['comentarios']
              fecha = form2.cleaned_data['fecha_tarea']
              plazo = form2.cleaned_data['fecha_plazo']
              if fecha < date.today() or plazo < date.today():
                  messages.success(request, f'Fechas no pueden ser anteriores a la fecha actual')
                  return redirect('paralegapp:detalle_actualizacion', pka=pka)
              importancia = form2.cleaned_data['importancia']
              obj, created = Tareas.objects.get_or_create(importancia=importancia, nombre=nombre, desc=desc, creador=usuario_activo,
                                                          comentarios=comentarios, fecha_creacion=date.today(), fecha_tarea=fecha, fecha_plazo=plazo, usuario=miestado)
              if created:
                  obj.numero = tareas.count()
                  obj.save()
                  t = Tareas_invitado(fecha_invitacion=date.today(), tarea=obj, invitado=usuario_activo)
                  t.save()
                  messages.success(request, f'Nueva tarea {nombre} agregada a el estado')
                  return redirect('paralegapp:detalle_actualizacion', pka=pka)
              messages.success(request, f'Ya agrego una tarea con estas mismas caracteristicas previamente')
              return redirect('paralegapp:detalle_actualizacion', pka=pka)
      else:
          form1 = PlazoForm()
          form2 = TareaForm()
          return render(request, 'casos/detalle_actualizacion.html',
                        {'form1': form1, 'form2': form2, 'miestado': miestado, 'caso': caso, 'tareas': tareas,'micaso':micaso,
                         'horas':horas, 'ta_te': ta_te, 'participantes':participantes, 'usuario':usuario})
   else:
       messages.warning(request, f'Actualizacion no corresponde a "tus casos" o no has iniciado sesión')
       return render(request, 'casos/detalle_actualizacion.html')

def TomarActualizacion(request, pka):
    usuario_activo = request.user
    miestado = Usuario_T_estado.objects.get(pk=pka)
    usuario_estado = miestado.usuario
    if usuario_activo == usuario_estado:
        miestado.estado_estado = 'En proceso'
        miestado.fecha_toma = date.today()
        miestado.fecha_finalizado = None
        miestado.save()
        messages.success(request, f'Estado fue tomado con exito, ahora puede programar tareas para el estado')
        return redirect('paralegapp:detalle_actualizacion', pka=pka)

def FinalizarActualizacion(request, pka):
    usuario_activo = request.user
    miestado = Usuario_T_estado.objects.get(pk=pka)
    usuario_estado = miestado.usuario
    if usuario_activo == usuario_estado:
        miestado.estado_estado = 'Terminado'
        miestado.fecha_finalizado = date.today()
        miestado.save()
        messages.success(request, f'Estado fue finalizado con exito con fecha {hoy}')
        return redirect('paralegapp:detalle_actualizacion', pka=pka)

###Tareas
def mis_tareas(request, orden): ##para las tareas
     usuario_activo = request.user
     tareas = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea__usuario__caso_activo=True).order_by(orden)
     return render(request, 'casos/tareas.html', {'tareas': tareas, 'orden':orden})

def detalle_tarea(request, pkt):
    usuario_activo = request.user
    tarea = Tareas.objects.get(pk=pkt)
    usuario_tarea = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea=tarea)
    usuario = Profile.objects.get(user=usuario_activo)
    if usuario_tarea.count() > 0:
        mi_estado = tarea.usuario
        estado = mi_estado.estado_caso
        cuaderno = estado.cuaderno
        caso = cuaderno.caso
        mi_caso = Usuario_t_caso.objects.get(caso=caso.pk, usuario=usuario_activo)
        emp = Profile.objects.get(user=usuario_activo).empresa
        anotaciones = Anotacion.objects.filter(tarea=tarea).order_by('-fecha')
        invitados = Tareas_invitado.objects.filter(tarea=tarea)
        participantes = invitados.values_list('invitado')
        colaboradores = Profile.objects.filter(empresa=emp, tipo_cuenta='usuario').exclude(user__in=participantes)
        if request.method == 'POST':
            form = NotaForm(request.POST)
            form2 = HorasForm(request.POST)
            if form.is_valid():
                nota = form.cleaned_data.get('comentario')
                if nota != None:
                    n = Anotacion(tarea=tarea, comentario=nota, fecha=datetime.today(), usuario=usuario_activo, tipo='nota')
                    n.save()
                    return redirect('paralegapp:detalle_tarea', pkt=pkt)
            if form2.is_valid():
                ho = form2.cleaned_data.get('horas')
                if ho < 0:
                    messages.success(request,f'Total de horas no puede ser negativo')
                    return redirect('paralegapp:detalle_tarea', pkt=pkt)
                tarea.horas = ho
                tarea.estado = 'Finalizada'
                tarea.fecha_fin = date.today()
                tarea.save()
                c = Usuario_t_caso.objects.get(usuario=usuario_activo, caso=caso.pk)
                tareas = Tareas.objects.filter(usuario__estado_caso__cuaderno__caso=c.caso.pk)
                horas = tareas.aggregate(Sum('horas'))['horas__sum']
                c.horas = horas
                c.save()
                a = Anotacion(tarea=tarea, usuario=usuario_activo, fecha=datetime.today(), comentario='Se ha finalizado la tarea contabilizando ' + str(ho) + ' de trabajo', tipo='hecho')
                a.save()
                messages.success(request, f'Tarea fue finalizada exitosamente con fecha {date.today()} y contabilizo {ho} horas de trabajo')
                return redirect('paralegapp:detalle_tarea', pkt=pkt)
        else:
           form = NotaForm()
           form2 = HorasForm()
           return render(request, 'casos/detalle_tarea.html',
                         {'tarea': tarea, 'mi_estado': mi_estado, 'anotaciones': anotaciones, 'colaboradores':colaboradores, 'usuario_activo':usuario_activo,
                          'estado': estado, 'caso': caso, 'cuaderno': cuaderno, 'form': form, 'form2': form2, 'invitados':invitados, 'mi_caso':mi_caso, 'usuario':usuario})
    else:
        return redirect('paralegapp:login')

def borrar_nota(request, pkn, pkt):
    n = Anotacion.objects.get(pk=pkn)
    n.delete()
    return redirect('paralegapp:detalle_tarea', pkt=pkt)

def iniciar_tarea(request, pkt):
    usuario_activo = request.user
    tarea = Tareas.objects.get(pk=pkt)
    usuario_tarea = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea=tarea)
    if usuario_tarea.count() > 0:
        tarea.estado = 'En proceso'
        tarea.save()
        a = Anotacion(tarea=tarea, usuario=usuario_activo, fecha=datetime.today(), comentario= 'Se ha dado inicio a la tarea', tipo='hecho')
        a.save()
        messages.success(request, f'Tarea fue iniciada exitosamente con fecha {hoy}')
        return redirect('paralegapp:detalle_tarea', pkt=pkt)

def reiniciar_tarea(request, pkt):
    usuario_activo = request.user
    tarea = Tareas.objects.get(pk=pkt)
    usuario_tarea = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea=tarea)
    if usuario_tarea.count() > 0:
        tarea.estado = 'En proceso'
        tarea.save()
        a = Anotacion(tarea=tarea, usuario=usuario_activo, fecha=datetime.today(), comentario= 'Se ha Reiniciado la tarea', tipo='hecho')
        a.save()
        messages.success(request, f'Tarea fue reiniciada exitosamente con fecha {hoy}')
        return redirect('paralegapp:detalle_tarea', pkt=pkt)

def invitar_a_tarea(request, pkt, pku):
    usuario_activo = request.user
    tarea = Tareas.objects.get(pk=pkt)
    usuario_tarea = Tareas_invitado.objects.filter(invitado=usuario_activo, tarea=tarea)
    if usuario_tarea.count() > 0:
        obj = Tareas.objects.get(pk=pkt)
        use = User.objects.get(pk=pku)
        t = Tareas_invitado(fecha_invitacion=datetime.today(), tarea=obj, invitado=use)
        t.save()
        messages.success(request, f'Usuario {use.first_name} invitado exitosamente')
        return redirect('paralegapp:detalle_tarea', pkt=pkt)

#agregar casos
def agregar_casos(request):
   usuario_activo = request.user
   if request.method == 'POST':
      form = CasoForm(request.POST)
      usuario_activo = request.user
      tribs = Tribunal.objects.all()
      miscasos = Usuario_t_caso.objects.filter(usuario=usuario_activo).order_by('-fecha_inicio')[:10]
      if form.is_valid():
         #usuario_activo = request.user
         rol = form.cleaned_data['rol']
         numero = form.cleaned_data['numero']
         year = form.cleaned_data['year']
         tribunal = form.cleaned_data['tribunal']
         if rol and numero and year and tribunal:
             caso, created = Caso.objects.get_or_create(rol=rol, numero=numero, year=year, tribunal=tribunal)
             if created:
                #not there so create and follow
                caso.save()
                ctc = Usuario_t_caso(caso=caso, usuario=usuario_activo, fecha_inicio=datetime.today())
                ctc.save()
             else:
                try:
                   obj = Usuario_t_caso.objects.get(caso=caso, usuario=usuario_activo)
                   messages.warning(request, f'Ya sigues este caso desde {obj.fecha_inicio}')
                except:
                   obj = Usuario_t_caso(caso=caso, usuario=usuario_activo, fecha_inicio=datetime.today())
                   obj.save()
   else:
      form = CasoForm()
      tribs = Tribunal.objects.all()
      miscasos = Usuario_t_caso.objects.filter(usuario=usuario_activo).order_by('-fecha_inicio')[:10]
   return render(request, 'casos/agregar_caso.html', {'form': form ,'tribs': tribs, 'miscasos': miscasos})


