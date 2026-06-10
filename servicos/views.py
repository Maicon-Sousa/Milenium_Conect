from django.shortcuts import render, get_object_or_404
from .forms import FormServico
from  django.http import HttpResponse, FileResponse
from .models import Servico
from fpdf import FPDF
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
from .models import Servico

def novo_servico(request):
    if request.method == "GET":
        form = FormServico()
        return render(request, 'servicos/novo_servico.html', {'form': form})
    elif request.method == "POST":
        form = FormServico(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_servico')
        else:
            return render(request, 'servicos/novo_servico.html', {'form': form}) 
        
def listar_servico(request):
    if request.method == "GET":
        servicos = Servico.objects.all()
        return render(request, 'servicos/listar_servico.html', {'servicos': servicos})
    
def servico(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)
    return render(request, 'servicos/servico.html', {'servico': servico})

def gerar_os(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)
    
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font('Arial',  'B', 12)
    
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(35, 10, 'Cliente:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.cliente.nome}', 1, 1, 'L', 1)
    
    pdf.cell(35, 10, 'Manutenções:', 1, 0, 'L', 1)
    
    categorias_manutencao = servico.categoria_manutencao.all()
    for i, manutencao in enumerate(categorias_manutencao):
        pdf.cell(0, 10, f' - {manutencao.get_titulo_display()}', 1, 1, 'L', 1)
        if not i == len(categorias_manutencao) - 1:
            pdf.cell(35, 10, '', 0, 0)
        
    pdf.cell(35, 10, 'Data de inicio:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.data_inicio}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Data de entrega:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.data_entrega}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Protocolo:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.protocolo}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Valor Total:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'R$ {servico.preco_total():.2f}', 1, 1, 'L', 1)
    
    pdf_content = pdf.output(dest='S').encode('latin1')
    pdf_bytes = BytesIO(pdf_content)
    
    return FileResponse(pdf_bytes, as_attachment=True, filename=f'OS_{servico.protocolo}.pdf')

#def servico_adicional(request):
    identificador_servico = request.POST.get('identificador_servico')
    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    preco = request.POST.get('preco')

    servico_adicional = ServicoAdicional(titulo=titulo,descricao=descricao,preco=preco)
    
    servico_adicional.save()

    servico = Servico.objects.get(identificador=identificador_servico)
    servico.servicos_adicionais.add(servico_adicional)
    servico.save()

    return HttpResponse("Salvo")

def finalizar_servico(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)
    servico.finalizado = True
    servico.save()
    return redirect('listar_servico')

def historico(request):
    servicos = Servico.objects.filter(finalizado=True).order_by('-id')
    return render(request, 'servicos/historico.html', {'servicos': servicos})

def agenda(request):
    servicos = Servico.objects.filter(finalizado=False).order_by('data_entrega')
    hoje = date.today()
    contexto = {
        'servicos': servicos,
        'hoje': hoje,
    }
    return render(request, 'servicos/agenda.html', contexto)


