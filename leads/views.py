from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.views import generic
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.views.generic.base import View
from .models import Carrinho, OrderItem, Robos, User
from .forms import RobosForm, CustomUserCreationForm, ProfileForm
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
import requests
import random
import json

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(TemplateView):
    template_name = "landing.html"

def svgecor(retorno):
        if retorno == False:
            robos = Robos.objects.all()
            svgecor.svg, svgecor.cor = [], []
            for i in range(len(robos)):
                l = i * 2
                j = - i - i
                strfy = ' ' + str(l)
                strfy2 = ' ' + str(l - i - i)
                dummy = ('M'+  str(l) +  strfy2  + strfy + strfy2)
                first = ''
                r = lambda: random.randint(0,255)
                cores = '#%02X%02X%02X' % (r(),r(),r())
                if svgecor.svg == []:
                    svgecor.svg.append(first)
                    svgecor.cor.append(cores)
                if i > 0:
                    svgecor.svg.append(dummy + ' ' + svgecor.svg[i-1])
                    svgecor.cor.append(cores)


def robos_list(request):
    robos = Robos.objects.all()
    p = Paginator(robos, 8)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page * p.page(1)

    svgecor(False)
    svg = svgecor.svg
    cor = svgecor.cor  
    context = {
        "robos": page,
        "svg": svg,
        "cor": cor
    }
    return render(request, "leads/lead_list.html", context)


def lead_detail(request, pk):
    robos = Robos.objects.get(id=pk)
    contador = Robos.objects.all().count()
    i = 1

    while i < 3:
        recom1 = Robos.objects.order_by('?')[0]
        recom2 = Robos.objects.order_by('?')[0]
        recom3 = Robos.objects.order_by('?')[0]
        recom4 = Robos.objects.order_by('?')[0]
        recom5 = Robos.objects.order_by('?')[0]
        recom6 = Robos.objects.order_by('?')[0]

        list1 = set([recom1.nome, recom2.nome, recom3.nome])
        list2 = set([recom4.nome, recom5.nome, recom6.nome])

        c = bool(list1.intersection(list2))

        if contador < 6:
            i = 4
        elif c == True or len(list1) < 3 or len(list2) < 3:
            i = 2
        else:
            i = 4

    list = []
    if robos.reviews != None:
        for i in range(0, robos.reviews):
            list.append(i)

    svg=request.POST.get("svg", "")
    cor=request.POST.get("cor", "")
    svgecor(False)
    svgdummy = svgecor.svg
    cordummy = svgecor.cor

    if svg == "":
        svg = svgdummy[random.randrange(0, contador)]
        cor = cordummy[1]

    context = {
        "robos": robos,
        "recom1": recom1,
        "recom2": recom2,
        "recom3": recom3,
        "recom4": recom4,
        "recom5": recom5,
        "recom6": recom6,
        "list": list,
        "svg": svg,
        "cor": cor,
        "svgdummy": svgdummy,
        "cordummy": cordummy,
    }
    return render(request, "leads/lead_detail.html", context)


def carrinho(request, slug):
    item = get_object_or_404(Robos, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )   
    order_qs = Carrinho.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantidade += 1
            order_item.save()
            messages.info(request, "Carrinho atualizado.")
            return redirect("leads:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Adicionado ao carrinho.")
            return redirect("leads:order-summary")
    else:
        ordered_date = timezone.now()
        order = Carrinho.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Adicionado ao carrinho.")
        return redirect("leads:order-summary")


def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Robos, slug=slug)
    order_qs = Carrinho.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantidade > 1:
                order_item.quantidade -= 1
                order_item.save()
            else:
                order_item.delete()
                messages.info(request, "Você está sem itens no carrinho")
                return redirect("leads/lead_list")
        else:
            messages.info(request, "Isso não estava no seu carrinho")
            return redirect("leads/lead_list.html")
    else:
        messages.info(request, "Você não tem nenhum item no carrinho")
        return redirect("leads/lead_list.html")


def remove_from_cart(request, slug):
    item = get_object_or_404(Robos, slug=slug)
    order_qs = Carrinho.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Removido do carrinho.")
            return redirect("leads:order-summary")
        else:
            messages.info(request, "Este produto não está no seu carrinho.")
            return redirect("leads/lead_list.html")
    else:
        messages.info(request, "Você não tem um carrinho.")
        return redirect("leads/lead_list.html")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Carrinho.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'leads/carrinho.html', context)
        except ObjectDoesNotExist:
            messages.warning(
                self.request, "Você não tem nenhum item no carrinho.")
            return redirect("../../leads/mercado/")

class Pagamento(LoginRequiredMixin, View):
   def get(self, *args, **kwargs):
        try:
            order = Carrinho.objects.get(user=self.request.user, ordered=False)
            total_limpo = order.get_total()
            format_total = str(total_limpo).replace(',', '')
            total_nraw = str(format_total).replace('.', '')
            print(total_limpo)
            data = {"callback": f"http://127.0.0.1:8000/leads/pagamento/{order.id}","amount": total_limpo}
            headers = {"Content-Type": "application/json"}
            url = "http://127.0.0.1:13380/sales"
            response = requests.post(url, headers=headers, json=data)
            body = response.json()
            qr = body.get('url')
            context = {
                'valor': total_limpo,
                'qr': qr,
            }

            return render(self.request, 'leads/pagamento.html', context)

        except ObjectDoesNotExist:
            messages.warning(
                self.request, "Você não tem nenhum item no carrinho.")
            return redirect("/")
    
    


def gerenciar(request):
    if not request.user.is_authenticated:
        return redirect("../signup")
    robos = Robos.objects.filter(usuario=request.user)
    svgecor(2==1)
    svg = svgecor.svg
    cor = svgecor.cor
    context = {
        "robos": robos,
        "svg": svg,
        "cor": cor
    }
    return render(request, "leads/lead_list.html", context)


def PerfilView(request):
    if not request.user.is_authenticated:
        return redirect("../signup")
    user = User.objects.filter(username=request.user)
    context = {
        "users": user,
    }
    return render(request, "leads/perfil.html", context)


class PerfilDetailView(DetailView):
    template_name = "leads/perfil_detail.html"
    queryset = User.objects.all()
    context_object_name = "users"

    def form_valid(self, form):
        user = form.save(commit=True)
        user.save()
        return redirect('')


def create_robo(request):
    if not request.user.is_authenticated:
        return redirect("../../signup")
    form = RobosForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        nome = instance.nome
        if Robos.objects.filter(nome=nome).exists():
            messages.info(request, "Este nome já existe.")
            return redirect("../../leads/criar")
        instance.usuario = request.user
        instance.save()
        return redirect("/leads")
    context = {
        "form": form,
    }
    return render(request, "leads/robo_create.html", context)


def lead_update(request, pk):
    lead = User.objects.get(id=pk)
    form = ProfileForm(instance=lead)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form,
        "user": lead,
    }
    return render(request, "leads/perfil_update.html", context)


def robo_update(request, pk):
    robo = Robos.objects.get(id=pk)
    form = RobosForm(instance=robo)
    if request.method == "POST":
        form = RobosForm(request.POST, instance=robo)
        if form.is_valid():
            if len(request.FILES) != 0:
                robo.robopic = request.FILES['robopic']
        form.save()
        return redirect("../")
    context = {
        "form": form,
        "robo": robo,
    }
    return render(request, "leads/robo_update.html", context)


def lead_delete(request, pk):
    lead = User.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")

def robo_delete(request, pk):
    robo = Robos.objects.get(id=pk)
    robo.delete()
    return redirect("/leads")

"""
def lead_create(request):
    form = LeadForm()
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            sobrenome = form.cleaned_data['sobrenome']
            idade = form.cleaned_data['idade']
            agent = Agent.objects.first()
            Lead.objects.create(
                first_name=nome,
                last_name=sobrenome,
                age=idade,
                agent=agent
            )
            return redirect("/leads")
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)
"""

"""
def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadForm()
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            sobrenome = form.cleaned_data['sobrenome']
            idade = form.cleaned_data['idade']
            lead.nome = nome
            lead.sobrenome = sobrenome
            lead.idade = idade
            lead.save()
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "leads/lead_update.html", context)
"""

"""
def landing_page(request):
    return render(request, "landing.html")

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "leads/lead_list.html", context)

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)
"""
