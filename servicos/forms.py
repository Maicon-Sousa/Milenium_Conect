from django.forms import ModelForm, DateInput
from .models import Servico, CategoriaManutencao

class FormServico(ModelForm):
    class Meta:
        model = Servico
        exclude = ['finalizado', 'protocolo', 'identificador']
        widgets = {
            'data_inicio': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_entrega': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            if field not in ['data_inicio', 'data_entrega']:
                self.fields[field].widget.attrs.update({'placeholder': field})

        choices = list()
        for i, j in self.fields['categoria_manutencao'].choices:
            try:
                categoria = CategoriaManutencao.objects.get(titulo=j)
                choices.append((i.value, categoria.get_titulo_display()))
            except CategoriaManutencao.DoesNotExist:
                pass

        self.fields['categoria_manutencao'].choices = choices