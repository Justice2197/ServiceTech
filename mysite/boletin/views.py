from django.shortcuts import render
from .forms import RegModelForm, ContactForm
from .models import Registrado
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
# Create your views here.
def inicio(request):
    titulo = "Bienvenidos"
    if request.user.is_authenticated:
        titulo = "Bienvenido %s" %(request.user)
    form = RegModelForm(request.POST or None)
    context = {
        "titulo": titulo,
        "form": form,
    }
    if form.is_valid():
        instance = form.save(commit=False)
        nombre = form.cleaned_data.get("nombre")
        email = form.cleaned_data.get("email")
        if not instance.nombre:
            instance.nombre = "PERSONA"
        instance.save()
        context = {
            "titulo": "Gracias %s por registrarte!" %(nombre)
        }
        if not nombre:
            context = {
                "titulo": "Gracias %s por registrarte!" %(email)
            }
        print(instance)
        print(instance.timestamp)
        #form_data = form.cleaned_data
        #abc = form_data.get("email")
        #abc2 = form_data.get("nombre")
        #obj = Registrado.objects.create(email=abc,nombre=abc2)

    return render(request, "inicio.html", context)


def contact(request):
    titulo = "Contacto"
    form = ContactForm(request.POST or None)
    if form.is_valid():
        #for key, value in form.cleaned_data.items():
        #    print(key, value)
        form_email = form.cleaned_data.get("email")
        form_mensaje = form.cleaned_data.get("mensaje")
        form_nombre= form.cleaned_data.get("nombre")
        asunto = 'Form de contacto'
        email_from = settings.EMAIL_HOST_USER
        email_to = [email_from, 'otromail@gmail.com']
        email_mensaje = "%s: %s enviado por %s" %(form_nombre, form_mensaje, form_email)
        send_mail(asunto,
            email_mensaje,
            email_from,
            email_to,
            fail_silently=False
        )
        #print(email, mensaje, nombre)
    context = {
        "form": form,
        "titulo": titulo,
    }
    return render(request, "forms.html", context)

class SomosView(TemplateView):
    template_name = 'somos.html'

class ServicioView(TemplateView):
    template_name = 'servicios.html'


class FormularioView(TemplateView):
    template_name = 'formulario.html'


class RegistroView(TemplateView):
    template_name='registro.html'