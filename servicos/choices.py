from django.db.models import TextChoices

class ChoicesCategoriaManutencao(TextChoices):
    
    ELETRICA = 'ELE', 'Elétrica'
    MECANICA = 'MEC', 'Mecânica'
    HIDRAULICA = 'HID', 'Hidráulica'
    BALANCEAMENTO = 'BAL', 'Balanceamento'
    TROCA_PNEU = 'TRP', 'Troca de Pneus'
    
    # Revisões
    REVISAO_PREVENTIVA = 'REP', 'Revisão Preventiva'
    REVISAO_PROGRAMADA = 'RPR', 'Revisão Programada'
    
    # Funilaria e Pintura
    FUNILARIA = 'FUN', 'Funilaria'
    PINTURA = 'PIN', 'Pintura'
    
    # Sistemas específicos
    FREIOS = 'FRE', 'Freios'
    SUSPENSAO = 'SUS', 'Suspensão'
    CAMBIO = 'CAM', 'Câmbio'
    MOTOR = 'MOT', 'Motor'
    AR_CONDICIONADO = 'ARC', 'Ar Condicionado'
    ESCAPAMENTO = 'ESC', 'Escapamento'
    
    # Revisão de documentação
    VISTORIA = 'VIS', 'Vistoria'
    
    OUTROS = 'OUT', 'Outros'