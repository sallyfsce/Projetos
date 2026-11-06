"""
sistema.py — BACKEND (regras de negócio, estruturas de dados e algoritmos)
Sprint 4 — Estruturas de Dados e Algoritmos em Python

Aqui fica TUDO o que é avaliado: a classe Sessao, a lista de sessões, a
tarifação, a busca sequencial, o Bubble Sort, as estatísticas e a análise
de complexidade. A interface web (app.py + static/index.html) apenas chama
estas funções.

INTEGRANTES:
Guilherme Detta RM-569666
Igor Alves RM-574127
Henrique Bolfer RM-569514
Arthur Costa RM-569976
Rafaella Ferreira RM-571030
Aneliza Rondina RM-572977
"""

from datetime import datetime

# ---------------------------------------------------------------------------
# 1. ESTRUTURA DE DADOS DA SESSÃO
# ---------------------------------------------------------------------------


class Sessao:
    """Representa UMA sessão de recarga de veículo elétrico."""

    def __init__(self, id_sessao, usuario, tipo_usuario, veiculo,
                 tipo_carregador, tempo, energia, tarifa, custo,
                 data_hora, horario_pico=False, status="Concluída"):
        self.id = id_sessao                  # identificador único (automático)
        self.usuario = usuario               # nome de quem recarregou
        self.tipo_usuario = tipo_usuario     # "Comum" ou "Premium"
        self.veiculo = veiculo               # placa/modelo
        self.tipo_carregador = tipo_carregador  # "AC (lento)" ou "DC (rápido)"
        self.tempo = tempo                   # minutos
        self.energia = energia               # kWh
        self.tarifa = tarifa                 # R$/kWh efetivamente aplicada
        self.custo = custo                   # R$ total da sessão
        self.data_hora = data_hora           # "dd/mm/aaaa HH:MM"
        self.horario_pico = horario_pico     # True se pagou tarifa de pico
        self.status = status

    def para_dict(self):
        """Converte o objeto em dicionário, para virar JSON e ir à interface."""
        return dict(self.__dict__)


# ---------------------------------------------------------------------------
# 2. ARMAZENAMENTO DE MÚLTIPLAS SESSÕES
# ---------------------------------------------------------------------------

sessoes = []        # lista que guarda todos os objetos Sessao
proximo_id = 1      # contador: cada nova sessão recebe um ID diferente

# ---------------------------------------------------------------------------
# 3. TARIFAÇÃO
# ---------------------------------------------------------------------------

TARIFAS = {"Comum": 1.30, "Premium": 0.90}   # R$ por kWh
TIPOS_CARREGADOR = ["AC (lento)", "DC (rápido)"]
HORA_PICO_INICIO = 18
HORA_PICO_FIM = 22
ACRESCIMO_PICO = 0.25                        # +25% no horário de pico


def esta_em_horario_pico(hora):
    return HORA_PICO_INICIO <= hora <= HORA_PICO_FIM


def calcular_tarifa(tipo_usuario, hora):
    """Devolve (tarifa_por_kwh, em_pico). Tarifa de pico = base + 25%."""
    tarifa = TARIFAS[tipo_usuario]
    em_pico = esta_em_horario_pico(hora)
    if em_pico:
        tarifa = round(tarifa * (1 + ACRESCIMO_PICO), 3)
    return tarifa, em_pico


# ---------------------------------------------------------------------------
# 4. CADASTRO (com validação)
# ---------------------------------------------------------------------------


def _para_numero(valor, nome):
    """Aceita '12,5' ou '12.5' e devolve float; senão, levanta ValueError."""
    try:
        return float(str(valor).replace(",", "."))
    except ValueError:
        raise ValueError(f"{nome} inválido: digite um número.")


def cadastrar_sessao(usuario, veiculo, tipo_carregador, tipo_usuario,
                     tempo, energia, hora=None):
    """Valida os dados, calcula a tarifa e guarda a sessão na lista."""
    global proximo_id

    usuario = str(usuario or "").strip()
    if usuario == "":
        raise ValueError("O nome do usuário não pode ficar em branco.")

    veiculo = str(veiculo or "").strip() or "Não informado"

    if tipo_usuario not in TARIFAS:
        raise ValueError("Tipo de usuário inválido (use Comum ou Premium).")
    if tipo_carregador not in TIPOS_CARREGADOR:
        raise ValueError("Tipo de carregador inválido.")

    tempo = _para_numero(tempo, "Tempo")
    if tempo <= 0 or tempo != int(tempo):
        raise ValueError("O tempo deve ser um número inteiro de minutos maior que zero.")
    tempo = int(tempo)

    energia = _para_numero(energia, "Energia")
    if energia <= 0:
        raise ValueError("A energia deve ser maior que zero.")

    agora = datetime.now()
    if hora in (None, ""):
        hora = agora.hour
    else:
        hora = int(_para_numero(hora, "Hora"))
        if not 0 <= hora <= 23:
            raise ValueError("A hora deve estar entre 0 e 23.")
        agora = agora.replace(hour=hora)

    tarifa, em_pico = calcular_tarifa(tipo_usuario, hora)
    custo = round(energia * tarifa, 2)

    nova = Sessao(proximo_id, usuario, tipo_usuario, veiculo, tipo_carregador,
                  tempo, energia, tarifa, custo,
                  agora.strftime("%d/%m/%Y %H:%M"), horario_pico=em_pico)
    proximo_id += 1
    sessoes.append(nova)          # O(1): adiciona no fim da lista
    return nova


def limpar_sessoes():
    global proximo_id
    sessoes.clear()
    proximo_id = 1


# ---------------------------------------------------------------------------
# 5. BUSCA — Busca Sequencial (implementação própria)
# ---------------------------------------------------------------------------


def busca_sequencial(lista, id_procurado):
    """
    Percorre a lista posição por posição, comparando o ID de cada sessão
    com o ID procurado.
      - Termina quando ENCONTRA (devolve o índice) ou quando chega ao
        fim da lista sem achar (devolve -1).
      - Pior caso: o ID está no final ou não existe -> n comparações -> O(n).
    Devolve (indice, comparacoes) — o contador serve para demonstrar o O(n).
    """
    comparacoes = 0
    for i in range(len(lista)):
        comparacoes += 1
        if lista[i].id == id_procurado:
            return i, comparacoes
    return -1, comparacoes


# ---------------------------------------------------------------------------
# 6. ORDENAÇÃO — Bubble Sort (implementação própria)
# ---------------------------------------------------------------------------

CRITERIOS_ORDENACAO = {
    "id": lambda s: s.id,
    "energia": lambda s: s.energia,
    "custo": lambda s: s.custo,
    "tempo": lambda s: s.tempo,
}


def bubble_sort(lista, chave):
    """
    Bubble Sort: a cada passagem compara pares vizinhos e troca os que estão
    fora de ordem; assim o maior valor "borbulha" até o fim da lista.
    'chave' é uma função que diz QUAL campo comparar (ex.: o custo).
      - Dois laços aninhados -> ~n*n comparações -> O(n²).
      - Se uma passagem inteira não troca nada, a lista já está ordenada
        e o algoritmo para mais cedo.
    Ordena a própria lista e devolve (comparacoes, trocas).
    """
    n = len(lista)
    comparacoes = 0
    trocas = 0
    for i in range(n):
        trocou = False
        for j in range(n - 1 - i):
            comparacoes += 1
            if chave(lista[j]) > chave(lista[j + 1]):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocas += 1
                trocou = True
        if not trocou:
            break
    return comparacoes, trocas


def ordenar_sessoes(campo, decrescente=False):
    """Ordena uma CÓPIA da lista (a ordem de cadastro original é preservada)."""
    if campo not in CRITERIOS_ORDENACAO:
        raise ValueError("Critério de ordenação inválido.")
    copia = sessoes[:]
    comparacoes, trocas = bubble_sort(copia, CRITERIOS_ORDENACAO[campo])
    if decrescente:
        copia.reverse()
    return copia, comparacoes, trocas


# ---------------------------------------------------------------------------
# 7. ESTATÍSTICAS E RELATÓRIO FINAL
# ---------------------------------------------------------------------------


def calcular_estatisticas():
    """Um único laço pela lista -> O(n)."""
    total = len(sessoes)
    if total == 0:
        return None

    energia_total = 0.0
    faturamento = 0.0
    maior = sessoes[0]
    menor = sessoes[0]
    em_pico = 0

    for s in sessoes:
        energia_total += s.energia
        faturamento += s.custo
        if s.energia > maior.energia:
            maior = s
        if s.energia < menor.energia:
            menor = s
        if s.horario_pico:
            em_pico += 1

    return {
        "total_sessoes": total,
        "energia_total": round(energia_total, 2),
        "faturamento": round(faturamento, 2),
        "ticket_medio": round(faturamento / total, 2),
        "maior_consumo": maior.energia,
        "menor_consumo": menor.energia,
        "sessoes_em_pico": em_pico,
    }


def gerar_relatorio():
    """Resumo final: estatísticas + quebra por tipo de usuário e carregador."""
    est = calcular_estatisticas()
    if est is None:
        return None

    por_usuario = {}
    por_carregador = {}
    mais_cara = sessoes[0]
    for s in sessoes:
        for grupo, chave in ((por_usuario, s.tipo_usuario),
                             (por_carregador, s.tipo_carregador)):
            item = grupo.setdefault(chave, {"sessoes": 0, "energia": 0.0, "faturamento": 0.0})
            item["sessoes"] += 1
            item["energia"] = round(item["energia"] + s.energia, 2)
            item["faturamento"] = round(item["faturamento"] + s.custo, 2)
        if s.custo > mais_cara.custo:
            mais_cara = s

    return {
        "resumo": est,
        "por_tipo_usuario": por_usuario,
        "por_tipo_carregador": por_carregador,
        "sessao_mais_cara": mais_cara.para_dict(),
    }


# ---------------------------------------------------------------------------
# 8. ANÁLISE DE COMPLEXIDADE (mede os algoritmos de verdade)
# ---------------------------------------------------------------------------


def analisar_complexidade(tamanhos=(10, 20, 40, 80, 160)):
    """
    Para cada tamanho n, monta n sessões FICTÍCIAS (não entram na lista real),
    roda os dois algoritmos no PIOR CASO e conta as comparações:
      - busca: procura um ID que não existe        -> n comparações
      - bubble: lista em ordem decrescente de custo -> n(n-1)/2 comparações
    """
    resultado = []
    for n in tamanhos:
        # custos decrescentes = pior caso do Bubble Sort
        fake = [Sessao(i + 1, "Teste", "Comum", "-", "AC (lento)", 10,
                       float(n - i), 1.3, float(n - i), "-") for i in range(n)]
        _, comp_busca = busca_sequencial(fake, -1)
        comp_bubble, _ = bubble_sort(fake, lambda s: s.custo)
        resultado.append({"n": n, "comparacoes_busca": comp_busca,
                          "comparacoes_bubble": comp_bubble})
    return resultado


# ---------------------------------------------------------------------------
# DADOS DE EXEMPLO (para agilizar a demonstração no vídeo)
# ---------------------------------------------------------------------------

EXEMPLOS = [
    ("Marcos Silva",    "Tesla Model 3",  "DC (rápido)", "Premium", 35, 28.4, 10),
    ("Patrícia Gomes",  "BYD Dolphin",    "AC (lento)",  "Comum",  120, 18.0, 14),
    ("Roberto Alves",   "Nissan Leaf",    "AC (lento)",  "Comum",   90, 12.5, 19),
    ("Fernanda Costa",  "Renault Zoe",    "DC (rápido)", "Premium", 25, 20.0, 8),
    ("Lucas Pereira",   "Volvo EX30",     "DC (rápido)", "Premium", 40, 35.7, 20),
    ("Juliana Rocha",   "JAC E-JS1",      "AC (lento)",  "Comum",  150, 9.8, 12),
    ("Carlos Lima",     "BMW iX1",        "DC (rápido)", "Comum",   30, 42.0, 21),
    ("Beatriz Nunes",   "Peugeot e-208",  "AC (lento)",  "Premium", 60, 15.3, 16),
]


def carregar_exemplos():
    for dados in EXEMPLOS:
        usuario, veiculo, carregador, tipo, tempo, energia, hora = dados
        cadastrar_sessao(usuario, veiculo, carregador, tipo, tempo, energia, hora)
