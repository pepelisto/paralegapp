from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CasoListView, CasoListViewTodos

app_name = 'paralegapp'
urlpatterns = [

    path('paralegapp/home/',             views.home,                name='home'),

    path('paralegapp/usuario/',          views.usuario,             name='usuario'),
    path('paralegapp/ayuda/',            views.ayuda,               name='ayuda'),

    path('paralegapp/login/',            auth_views.LoginView.as_view(template_name='casos/login.html'),   name='login'),
    path('paralegapp/logout/',           auth_views.LogoutView.as_view(template_name='casos/logout.html'), name='logout'),
    path('paralegapp/main/',             views.inicio,               name='inicio'),
    path('paralegapp/gestion/',          views.gestion,               name='gestion'),

    #lista de causas
    path('paralegapp/casos/',                              CasoListView.as_view(),          name='mis_casos'),
    path('paralegapp/casos/todos/',                        CasoListViewTodos.as_view(),     name='mis_casos_todos'),
    path('paralegapp/casos/favorito/<int:pkc>&<int:f>',    views.CasoFavorito,              name='caso_favorito'),
    path('paralegapp/casos/finalizar/<int:pkc>&<int:ac>',  views.FinalizarCausa,            name='caso_finalizar'),

    #para detalles de las causas
    path('paralegapp/casos/<int:pk>&<int:num>/',                views.casoDetail,         name='detalle_caso'),
    path('paralegapp/casos/<int:pk>&<int:num>/litigantes/',     views.casoLitigantes,     name='litigantes_caso'),
    path('paralegapp/casos/<int:pk>&<int:num>/notificaciones/', views.casoNotificaciones, name='notificaciones_caso'),
    path('paralegapp/casos/<int:pk>&<int:num>/esc/',            views.casoEsc,            name='esc_caso'),
    path('paralegapp/casos/<int:pk>&<int:num>/exohortos/',      views.casoExohortos,      name='exohortos_caso'),

    #para detalles y lista de actualizaciones por usuario
    path('paralegapp/estados/<slug:orden>&<int:can>/ordenar/', views.mis_estados,            name='mis_estados'),
    path('paralegapp/estados/<int:pka>/',                      views.detalleActualizacion,   name='detalle_actualizacion'),
    path('paralegapp/estados/<int:pk>/ir',                     views.iractualizacion,        name='ir_detalle_actualizacion'),
    path('paralegapp/estados/<int:pka>/tomar/',                views.TomarActualizacion,     name='tomar_actualizacion'),
    path('paralegapp/estados/<int:pka>/finalizar/',            views.FinalizarActualizacion, name='finalizar_actualizacion'),

    #para lista y detalles de tareas
    path('paralegapp/tareas/<slug:orden>/ordenar/',           views.mis_tareas,           name='mis_tareas'),
    path('paralegapp/tareasborrar/<int:pkn>&<int:pkt>/',      views.borrar_nota,          name='borrar_nota'),
    path('paralegapp/tareas/<int:pkt>/',                      views.detalle_tarea,        name='detalle_tarea'),
    path('paralegapp/tareas/<int:pkt>/iniciar',               views.iniciar_tarea,        name='iniciar_tarea'),
    path('paralegapp/tareas/<int:pkt>/reiniciar',             views.reiniciar_tarea,      name='reiniciar_tarea'),
    path('paralegapp/tareas/<int:pkt>/invitar/<int:pku>',     views.invitar_a_tarea,      name='invitar_a_tarea'),

    #path('paralegapp/estados/<int:pk>/',    name='detalle_estado'),
    path('paralegapp/agregar/',          views.agregar_casos,        name='agregar_casos'),

    path('paralegapp/register/',                    views.signup,               name='register'),
    path('paralegapp/activate/<uidb64>/<token>/',   views.activate,             name='activate'),

]
