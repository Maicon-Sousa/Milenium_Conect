from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Carro
import re
from django.core import serializers
import json
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from servicos.models import Servico
from django.contrib.auth.decorators import login_required

@login_required
def clientes(request):
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')

        cliente = Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'carros': zip(carros, placas, anos) })

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'carros': zip(carros, placas, anos)})

        cliente = Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )

        cliente.save()

        for carro, placa, ano in zip(carros, placas, anos):
            car = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente)
            car.save()

        return redirect('clientes')      

@login_required
def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id=id_cliente)
    carros = Carro.objects.filter(cliente=cliente[0])
    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']
    carros_json = json.loads(serializers.serialize('json', carros))
    carros_json = [{'fields': i['fields'], 'id': i['pk']} for i in carros_json]
    data = {'cliente': cliente_json, 'carros': carros_json, 'cliente_id': cliente_id}
    return JsonResponse(data)

@login_required
def excluir_carro(request, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        return redirect(reverse('clientes')+f'?aba=att_cliente&id_cliente={id}')
    except:
        return redirect(reverse('clientes')+f'?aba=att_cliente&id_cliente={id}')

@login_required
@csrf_exempt
def update_carro(request, id):
    nome_carro = request.POST.get('carro')
    placa = request.POST.get('placa')
    ano = request.POST.get('ano')

    carro = Carro.objects.get(id=id)
    list_carros = Carro.objects.exclude(id=id).filter(placa=placa)

    if list_carros.exists():
        return redirect(reverse('clientes') + '?erro=placa_existente')
        
    carro.carro = nome_carro
    carro.placa = placa
    carro.ano = ano
    carro.save()

    return redirect(reverse('clientes'))

@login_required
def update_cliente(request, id):
    body = json.loads(request.body)

    nome = body['nome']
    sobrenome = body['sobrenome']
    email = body['email']
    cpf = body['cpf']

    cliente = get_object_or_404(Cliente, id=id)
    try:
        cliente.nome = nome
        cliente.sobrenome = sobrenome
        cliente.email = email
        cliente.cpf = cpf
        cliente.save()
        return JsonResponse({'status': '200', 'nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf': cpf})
    except:
        return JsonResponse({'status': '500'})
    
@login_required
def add_carro_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    carro = request.POST.get('carro')
    placa = request.POST.get('placa')
    ano = request.POST.get('ano')
    
    cliente = get_object_or_404(Cliente, id=id_cliente)
    novo_carro = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente)
    novo_carro.save()
    
    return JsonResponse({'status': '200'})

@login_required
def dashboard(request):
    from servicos.models import Servico
    from datetime import date
    
    hoje = date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    total_clientes = Cliente.objects.count()
    total_carros = Carro.objects.count()
    servicos_abertos = Servico.objects.filter(finalizado=False).count()
    servicos_finalizados = Servico.objects.filter(finalizado=True).count()
    entregas_hoje = Servico.objects.filter(finalizado=False, data_entrega=hoje).count()
    ultimos_servicos = Servico.objects.order_by('-id')[:5]
    ultimos_clientes = Cliente.objects.order_by('-id')[:5]
    
    servicos_mes = Servico.objects.filter(finalizado=True, data_entrega__month=mes_atual, data_entrega__year=ano_atual)
    faturamento_mes = sum([s.preco_total() for s in servicos_mes])
    
    context = {
        'total_clientes': total_clientes,
        'total_carros': total_carros,
        'servicos_abertos': servicos_abertos,
        'servicos_finalizados': servicos_finalizados,
        'entregas_hoje': entregas_hoje,
        'ultimos_servicos': ultimos_servicos,
        'ultimos_clientes': ultimos_clientes,
        'faturamento_mes': faturamento_mes,
    }
    return render(request, 'dashboard.html', context)

@login_required
def servicos_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)
    servicos = Servico.objects.filter(cliente=cliente).order_by('-id')
    return render(request, 'servicos_cliente.html', {'servicos': servicos, 'cliente': cliente})

