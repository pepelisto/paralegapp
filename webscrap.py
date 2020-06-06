from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import getpass
import datetime
from datetime import datetime, date
import os
import time
import shutil
username = getpass.getuser()

from django.conf import settings
import django
from project.settings import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()
from Paralegapp.models import *

fecha = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
fecha2 = datetime.now()
casos = Caso.objects
#poner condicion de solo casos activos

if casos.count() > 0:
      options = webdriver.ChromeOptions()
      #options.add_experimental_option('prefs', {
        #"download.default_directory": path4,  # Change default directory for downloads
        #"download.prompt_for_download": False,  # To auto download the file
        #"download.directory_upgrade": True,
        #"plugins.always_open_pdf_externally": True,  # It will not show PDF directly in chrome
       # "profile.default_content_settings.popups": 0
      #})
      browser = webdriver.Chrome(executable_path=r'C:\\Users\\' + username + '\\Desktop\\chromedriver\\chromedriver.exe', options=options)
      #---------------open casos pagina
      browser.get('https://civil.pjud.cl/CIVILPORWEB/')
      # esperar que carge
      wait = WebDriverWait(browser, 120)
      wait.until(EC.presence_of_element_located((By.XPATH, '/html/frameset/frameset/frame[2]')))
      #----------------------- cambiar al inner HTML
      bframe = browser.find_element_by_xpath('/html/frameset/frameset/frame[2]')
      browser.switch_to.frame(bframe)
      main = browser.current_window_handle
      cuenta = 0
      cambios = 0
 # css : body > form > table:nth-child(10) > tbody > tr > td:nth-child(2) > a:nth-child(2) > img      xpath:  /html/body/form/table[6]/tbody/tr/td[2]/a[2]/img
      try:
          wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > form > table:nth-child(10) > tbody > tr > td:nth-child(2) > a:nth-child(2) > img')))
          pos = str(10)
      except:
          wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > form > table:nth-child(9) > tbody > tr > td:nth-child(2) > a:nth-child(2) > img')))
          pos = str(9)
      #----------------------recorre todos los casos para actualizarlos
      for caso in casos.all():
            cuenta = cuenta + 1
            if cuenta == 41:
                #------------- open casos pagina
                browser.close()
                browser.quit()
                browser = webdriver.Chrome(executable_path=r'C:\\Users\\' + username + '\\Desktop\\chromedriver\\chromedriver.exe', options=options)
                browser.get('https://civil.pjud.cl/CIVILPORWEB/')
                #----------- esperar que carge
                wait.until(EC.presence_of_element_located((By.XPATH, '/html/frameset/frameset/frame[2]')))
                #----------- cambiar al inner HTML
                bframe = browser.find_element_by_xpath('/html/frameset/frameset/frame[2]')
                browser.switch_to.frame(bframe)
                main = browser.current_window_handle
                cuenta = 0
            tipo = caso.rol
            rol = caso.numero
            ano = caso.year
            tribunal = caso.tribunal
            try:# css : body > form > table:nth-child(10) > tbody > tr > td:nth-child(2) > a:nth-child(2) > img      xpath:  /html/body/form/table[6]/tbody/tr/td[2]/a[2]/img
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > form > table:nth-child(' + pos + ') > tbody > tr > td:nth-child(2) > a:nth-child(2) > img')))
            except:
                # open casos pagina
                browser.close()
                browser.quit()
                browser = webdriver.Chrome(executable_path=r'C:\\Users\\' + username + '\\Desktop\\chromedriver\\chromedriver.exe', options=options)
                browser.get('https://civil.pjud.cl/CIVILPORWEB/')
                #--------------- esperar que carge
                wait.until(EC.presence_of_element_located((By.XPATH, '/html/frameset/frameset/frame[2]')))
                #-------------- cambiar al inner HTML
                bframe = browser.find_element_by_xpath('/html/frameset/frameset/frame[2]')
                browser.switch_to.frame(bframe)
                main = browser.current_window_handle
                cuenta = 0
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > form > table:nth-child(9) > tbody > tr > td:nth-child(2) > a:nth-child(2) > img')))
            #insertar datos del caso para buscar y click en buscar
            browser.find_element_by_css_selector('body > form > table:nth-child(' + pos + ') > tbody > tr > td:nth-child(2) > a:nth-child(2) > img').click()
            browser.find_element_by_css_selector('#RUC > select').send_keys(tipo)
            browser.find_element_by_css_selector('#RUC > input:nth-child(3)').send_keys(rol)
            browser.find_element_by_css_selector('#RUC > input:nth-child(4)').send_keys(ano)
            ##
            browser.find_element_by_css_selector('#tribUno > select').send_keys(tribunal)
            browser.find_element_by_css_selector('body > form > table:nth-child(' + pos + ') > tbody > tr > td:nth-child(2) > a:nth-child(1) > img').click()
            Err = 0
            #click en doc encontrado, si no lo encuentra anota "no encontrado" y pasa al proximo
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#contentCellsAddTabla > tbody > tr > td:nth-child(1) > a')))
                browser.find_element_by_css_selector('#contentCellsAddTabla > tbody > tr > td:nth-child(1) > a').click()
            #-------------espera que carge la pagina
            except:
                caso.last_chek_coment = 'no se encontro el caso'
                browser.execute_script("window.history.go(-1)")
                continue
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > form > table:nth-child(20) > tbody > tr:nth-child(1) > td:nth-child(1)')))
            if caso.dte_nombre == None:
                caso.dte_nombre = browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(1) > td:nth-child(2)').text
                #########arreglar fecha, importante
                ###caso.fecha_ingreso = datetime.strptime(browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(1) > td:nth-child(3)').text[9:len(browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(1) > td:nth-child(3)').text)], '%d/%m/%Y')
                ########
                caso.archivo = browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(4) > td:nth-child(2) > img').get_attribute("onclick")[18:len(browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(4) > td:nth-child(2) > img').get_attribute("onclick")) - 2]

            caso.est_adm = browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(2) > td:nth-child(1)').text[10:len(browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(2) > td:nth-child(1)').text)]
            caso.proc = browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(2) > td:nth-child(2)').text[7:len(browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(2) > td:nth-child(2)').text)]
            caso.ubicacion = browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(2) > td:nth-child(3)').text[11:len(browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(2) > td:nth-child(3)').text)]
            caso.etapa = browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(3) > td:nth-child(1)').text[7:len(browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(3) > td:nth-child(1)').text)]
            caso.last_chek = fecha2
            estado = browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(3) > td:nth-child(2)').text[13:len(browser.find_element_by_css_selector('body > form > table:nth-child(20) > tbody > tr:nth-child(3) > td:nth-child(2)').text)]
            #--------------------------------------ve si el estado del proceso cambio para actualizarlo
            R = 0
            if estado != caso.estproceso:
                caso.estprocnmenos1 = caso.estproceso
                caso.estproceso = estado
                caso.last_change = fecha2
                caso.last_chek_coment = 'cambio en el estado del proceso'
                R = 1
            #-------------------------------cheuqe cuantos cuaderdos tiene la causa
            mycuadernos = browser.find_element_by_css_selector('#TablaCuadernos > tbody > tr > td:nth-child(2) > select')
            mycuaderno = browser.find_element_by_css_selector('#TablaCuadernos > tbody > tr > td:nth-child(2) > select > option').text
            mycuadopc = mycuadernos.find_elements_by_css_selector('option').__len__()
            cuadernos = Casos_t_cuadernos.objects.filter(caso_id=caso.pk)
            cuadprev = cuadernos.count()
            #----------------------------- si algun cuaderno no esta creado entonces lo crea
            if cuadprev != mycuadopc:
                g = 1
                for cua in range(1, mycuadopc + 1):
                    ccc = browser.find_element_by_css_selector('#TablaCuadernos > tbody > tr > td:nth-child(2) > select > option:nth-child(' + str(g) + ')').text
                    existe = Casos_t_cuadernos.objects.filter(caso=caso, cuaderno=ccc).count()
                    g = g + 1
                    if existe == 0:
                        Cuade = Casos_t_cuadernos(caso=caso, numero=cuadprev + 1, cuaderno=ccc, fecha_creacion=fecha2)
                        Cuade.save()
                        cuadprev = cuadprev + 1
                cuadernos = Casos_t_cuadernos.objects.filter(caso=caso)
            #---------------------------recorre todos los cuadernos para revisar si tienen cambios
            for cua in cuadernos:
                Err = 1
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#Historia > table:nth-child(2)')))
                if cua.cuaderno != mycuaderno:
                    browser.find_element_by_css_selector('#TablaCuadernos > tbody > tr > td:nth-child(2) > select > option:nth-child(' + str(cua.numero) + ')').click()
                    browser.find_element_by_css_selector('#botoncuaderno > img').click()
                mytable = browser.find_element_by_css_selector('#Historia > table:nth-child(2)')
                filas = mytable.find_elements_by_css_selector('tr').__len__()
                if filas != cua.estado_n:
                    try:
                        nuevos = filas - cua.estado_n
                    except:
                        nuevos = filas
                    cua.estado_previo_n = cua.estado_n
                    cua.estado_n = filas
                    caso.last_change = fecha2
                else:
                    nuevos = 0
                #----------------------si el cuaderno tiene cambios entonces lo actualiza
                #if cambios == 1:
                b = 2
                c = str(b)
                G = 0
                for m in range(1, nuevos + 1):
                        fol = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(1)').text
                        try:
                            #downloadable = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(2) > img').text
                            element = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(2) > img').get_attribute("onclick")
                            if element.startswith(' ShowPDF'):
                                 srcarchivo = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(2) > img').get_attribute("onclick")
                                 src = srcarchivo[18:len(srcarchivo) - 2]
                                 srctype = "pdf"
                            elif element.startswith('ShowEsc'):
                                 srcarchivo = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(2) > img').get_attribute("onclick")
                                 src = srcarchivo[18:len(srcarchivo) - 2]
                                 srctype = 'folder'
                            else:
                                src = None
                                srctype = None
                        except:
                            src = None
                            srctype = None
                        try:
                            element2 = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(3) > img').get_attribute("onclick")
                            if element2.startswith(' ShowPDF'):
                                srcarchivo2 = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(3) > img').get_attribute("onclick")
                                src2 = srcarchivo2[18:len(srcarchivo2) - 2]
                                srctype2 = "pdf"
                            elif element2.startswith('ShowEsc'):
                                srcarchivo2 = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(3) > img').get_attribute("onclick")
                                src2 = srcarchivo2[18:len(srcarchivo2) - 2]
                                srctype2 = 'folder'
                            else:
                                src2 = None
                                srctype2 = None
                        except:
                            src2 = None
                            srctype2 = None
                        etapa = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(4)').text
                        tramite = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(5)').text
                        desc_t = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(6)').text
                        datedoc = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(7)').text
                        foja = browser.find_element_by_css_selector('#Historia > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(8)').text
                        archivo = str(fol) + '_' + tramite
                        Err = 2
                        #found = 0

                        ##quizas quitar esto
                        #estados = Estado.objects.filter(cuaderno__caso_id=caso.pk)
                        #if estados.count() != filas:
                        #    for estado in estados:
                        #        if estado.numero_archivo == m:
                        #            found = found + 1
                        #            break
                        #        else:
                        #            continue
                        #    Err = 3
                        #    if found == 0:
                                ####quitar hasta aca ya que cheque antes las filas del cuaderno

                        estnuevo = Estado(tramite=tramite, doc=archivo, etapa=etapa, desc_tramite=desc_t, folio=fol, cuaderno=cua, archivo=src,
                                          tipoarchivo=srctype, foja=foja, fecha_tramite=datedoc, archivo_2=src2, tipoarchivo_2=srctype2, numero_archivo=filas - G)
                        estnuevo.save()
                        try:
                            estprevio = Estado.objects.get(cuaderno=cua, numero_archivo=filas - G - 1)
                        except:
                            estprevio = None
                        G = G + 1
                        ##poner despues del loop y verificar si ya lo tienene caso los usuarios hayan dejado de seguirlo, no debiera ser necesario por el if que puse
                        uslotienen = Usuario_t_caso.objects.filter(caso=caso)
                        for u in uslotienen:
                            usuario = u.usuario
                            if u.fecha_fin == None:
                               if G == 1 and estprevio == None:
                                   Ute = Usuario_T_estado(usuario=usuario, estado_caso=estnuevo, fecha_ingreso=fecha2, caso_activo=True)
                               else:
                                   if estprevio == None:# and G > 2:
                                       estarriba = Estado.objects.get(cuaderno=cua, numero_archivo=filas - G + 2)
                                       if estnuevo.folio != estarriba.folio:
                                           Ute = Usuario_T_estado(usuario=usuario, estado_caso=estnuevo, fecha_ingreso=fecha2, caso_activo=True, estado_estado= 'previo')
                                       else:
                                           Ute = Usuario_T_estado(usuario=usuario, estado_caso=estnuevo, fecha_ingreso=fecha2, caso_activo=True)
                                   else:
                                       Uteprevio = Usuario_T_estado.objects.get(usuario=usuario, estado_caso=estprevio)
                                       Ute = Usuario_T_estado(usuario=usuario, estado_caso=estnuevo, fecha_ingreso=fecha2, caso_activo=True)
                                       if Uteprevio.estado_estado != 'Terminado' and Uteprevio.estado_caso.fecha_tramite != Ute.estado_caso.fecha_tramite:  ## pner que la diferencia de fechas no sea mayor a un dia
                                           Uteprevio.estado_estado = 'sinfinalizar'
                                           Uteprevio.save()
                               Ute.save()



                            #else:
                                #### esto parece que hay q sacar ya que el usuario no debe recibir notificaciones
                               #Ute = Usuario_T_estado(usuario=usuario, estado_caso=estnuevo, fecha_ingreso=date.today(), caso_activo=False)
                           # Ute.save()
                            #if D == 1:
                            #    Uteprevio = Usuario_T_estado(usuario=usuario, estado_caso=estnuevo)
                        if R == 0:
                           caso.last_chek_coment = 'Estado Nuevo'
                        elif R == 1:
                           caso.last_chek_coment = 'Estado Nuevo y cambio en el estado'
                        b = b + 2
                        c = str(b)
                if nuevos != 0:
                    cua.save()

            LitActuales = Litigante.objects.filter(caso=caso).count()
            mytableLit = browser.find_element_by_css_selector('#Litigantes > table:nth-child(2)')
            filasLit = mytableLit.find_elements_by_css_selector('tr').__len__()
            if LitActuales != filasLit:
                browser.find_element_by_css_selector('#tdDos').click()
                b = 2
                c = str(b)
                for t in range(1, filasLit):
                    part = browser.find_element_by_css_selector('#Litigantes > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(1)').text
                    rut = browser.find_element_by_css_selector('#Litigantes > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(2)').text
                    persona = browser.find_element_by_css_selector('#Litigantes > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(3)').text
                    nombre = browser.find_element_by_css_selector('#Litigantes > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(4)').text
                    if LitActuales != 0:
                        LitActualesList = Litigante.objects.filter(caso=caso)
                        found2 = 0
                        for l in LitActualesList:
                             if l.rut == rut and l.participante == part:
                                 found2 = 1
                                 break
                        if found2 == 0:
                            newLit = Litigante(caso=caso, participante=part, rut=rut, persona=persona, nombre=nombre, fecha_creacion=fecha2)
                            newLit.save()
                    else:
                        newLit = Litigante(caso=caso, participante=part, rut=rut, persona=persona, nombre=nombre, fecha_creacion=fecha2)
                        newLit.save()
                    b = b + 2
                    c = str(b)


            notiactuales = Notificacion_caso.objects.filter(caso=caso).count()
            mytableNot = browser.find_element_by_css_selector('#Notificaciones > table:nth-child(2)')
            filasnot = mytableNot.find_elements_by_css_selector('tr').__len__()
            if notiactuales != filasnot:
                browser.find_element_by_css_selector('#tdTres').click()
                b = 2
                c = str(b)
                for t in range(1, filasnot):
                    Esta_not = browser.find_element_by_css_selector('#Notificaciones > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(1)').text
                    rol = browser.find_element_by_css_selector('#Notificaciones > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(2)').text
                    ruc = browser.find_element_by_css_selector('#Notificaciones > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(3)').text
                    fechtramite = browser.find_element_by_css_selector('#Notificaciones > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(4)').text
                    tippart = browser.find_element_by_css_selector('#Notificaciones > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(5)').text
                    nombre = browser.find_element_by_css_selector('#Notificaciones > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(6)').text
                    tramite = browser.find_element_by_css_selector('#Notificaciones > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(7)').text
                    obs = browser.find_element_by_css_selector('#Notificaciones > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(8)').text


                    if notiactuales != 0:
                        notiactualeslist = Notificacion_caso.objects.filter(caso=caso)
                        found2 = 0
                        for n in notiactualeslist:
                             if n.est_not == Esta_not and n.rol == rol and n.ruc == ruc and n.fectram == fechtramite and n.tip_part == tippart and n.nombre == nombre and n.tramite == tramite:
                                 found2 = 1
                                 break
                        if found2 == 0:
                            newnot = Notificacion_caso(est_not=Esta_not, rol=rol, ruc=ruc, fectram=fechtramite, tip_part=tippart, nombre=nombre, tramite=tramite, obs_fallido=obs, fecha_creacion= fecha2)
                            newnot.save()
                    else:
                        newnot = Notificacion_caso(est_not=Esta_not, rol=rol, ruc=ruc, fectram=fechtramite, tip_part=tippart, nombre=nombre, tramite=tramite, obs_fallido=obs, fecha_creacion= fecha2)
                        newnot.save()
                    b = b + 2
                    c = str(b)



            escactuales = Esc_por_resolver.objects.filter(caso=caso).count()
            mytableesc = browser.find_element_by_css_selector('#Escritos > table:nth-child(2)')
            filasesc = mytableesc.find_elements_by_css_selector('tr').__len__()
            if notiactuales != filasnot:
                browser.find_element_by_css_selector('#tdCuatro').click()
                b = 2
                c = str(b)
                for t in range(1, filasnot):
                    doc = browser.find_element_by_css_selector('#Escritos > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(1)').text
                    anexo = browser.find_element_by_css_selector('#Escritos > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(2)').text
                    fechaing = browser.find_element_by_css_selector('#Escritos > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(3)').text
                    tipo = browser.find_element_by_css_selector('#Escritos > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(4)').text
                    solicitante = browser.find_element_by_css_selector('#Escritos > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(5)').text
                    if escactuales != 0:
                        escactualeslist = Esc_por_resolver.objects.filter(caso=caso)
                        found2 = 0
                        for e in escactualeslist:
                            if e.doc == doc and e.anexo == anexo and e.fecha_ing == fechaing and e.tipo_escrito == tipo and e.solicitante == solicitante:
                                found2 = 1
                                break
                        if found2 == 0:
                            newesc = Esc_por_resolver(doc=doc, anexo=anexo, fecha_ing=fechaing, tipo_escrito=tipo, solicitante=solicitante, fecha_creacion=fecha2)
                            newesc.save()
                    else:
                        newesc = Esc_por_resolver(doc=doc, anexo=anexo, fecha_ing=fechaing, tipo_escrito=tipo, solicitante=solicitante, fecha_creacion=fecha2)
                        newesc.save()
                    b = b + 2
                    c = str(b)


            exactuales = Exohorto.objects.filter(caso=caso).count()
            mytableex = browser.find_element_by_css_selector('#Exhorto > table:nth-child(2)')
            filasex = mytableex.find_elements_by_css_selector('tr').__len__()
            if exactuales != filasex:
                browser.find_element_by_css_selector('#tdCinco').click()
                b = 2
                c = str(b)
                for t in range(1, filasnot):
                    rolor = browser.find_element_by_css_selector('#Exhorto > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(1)').text
                    tipoe = browser.find_element_by_css_selector('#Exhorto > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(2)').text
                    roldes = browser.find_element_by_css_selector('#Ehhorto > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(3)').text
                    fecord = browser.find_element_by_css_selector('#Ehhorto > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(4)').text
                    fecing = browser.find_element_by_css_selector('#Ehhorto > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(5)').text
                    tribdes = browser.find_element_by_css_selector('#Exhorto > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(6)').text
                    estex = browser.find_element_by_css_selector('#Exhorto > table:nth-child(2) > tbody > tr:nth-child(' + c + ') > td:nth-child(7)').text

                    if notiactuales != 0:
                        exactualeslist = Exohorto.objects.filter(caso=caso)
                        found2 = 0
                        for n in exactualeslist:
                            if n.rol_origen == rolor and n.tipo_exohorto == tipoe and n.rol_destino == roldes and n.fecha_ord_exohorto == fecord and n.fecha_ing_exohorto == fecing and n.tribunal_destino == tribdes and n.estado_exohorto == estex:
                                found2 = 1
                                break
                        if found2 == 0:
                            newex = Exohorto(rol_origen=rolor, tipo_exohorto= tipoe, rol_destino=roldes, fecha_ord_exohorto=fecord, fecha_ing_exohorto= fecing, tribunal_destino= tribdes, estado_exohorto=estex)
                            newex.save()
                    else:
                        newex = Exohorto(rol_origen=rolor, tipo_exohorto= tipoe, rol_destino=roldes, fecha_ord_exohorto=fecord, fecha_ing_exohorto= fecing, tribunal_destino= tribdes, estado_exohorto=estex)
                        newex.save()
                    b = b + 2
                    c = str(b)


            caso.last_chek = fecha2
            caso.save()
            #volver
            browser.execute_script("window.history.go(-2)")
            #sheet_obj.cell(row=k, column=16).value = len(os.listdir(path + idefolder))

#borrar carpeta temporal

#salir de browser
      browser.close()
      browser.quit()
