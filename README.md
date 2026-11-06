# Sprint 4 — Sistema de Gerenciamento de Estação de Recarga EV

Interface **Web** (HTML) + backend **Python (Flask)**.
Evolução direta do projeto da Sprint 3 (`sistema_de_gerenciamentoDSA.py`).

## Como rodar
```
pip install -r requirements.txt
python app.py
```
Abra **http://127.0.0.1:5000** no navegador. (Deixe o terminal visível no vídeo:
ele mostra as linhas `[BACKEND] ...` a cada ação, provando a integração.)

## Arquivos
| Arquivo | Papel |
|---|---|
| `sistema.py` | **Backend**: classe `Sessao`, lista `sessoes`, tarifação, busca sequencial, Bubble Sort, estatísticas, relatório, análise de complexidade |
| `app.py` | Rotas Flask: recebe a requisição, chama `sistema.py`, devolve JSON |
| `static/index.html` | Interface web (só tela; nenhuma regra de negócio) |

## Onde está cada item da Sprint 4
| Requisito | Onde |
|---|---|
| Estrutura de dados da sessão | `class Sessao` em `sistema.py` |
| Armazenamento de múltiplas sessões | lista `sessoes` + contador `proximo_id` |
| Tarifação | `calcular_tarifa()` (Comum R$1,30 / Premium R$0,90; pico 18h–22h = +25%) |
| Busca | `busca_sequencial()` — O(n) |
| Ordenação própria | `bubble_sort()` — O(n²) (não usa `sort()`/`sorted()`) |
| Estatísticas / relatório | `calcular_estatisticas()` / `gerar_relatorio()` |
| Análise de complexidade | `analisar_complexidade()` (aba "Complexidade") |
| Integração | `app.py` (rotas `/api/...`) + função `chamarApi()` no `index.html` |

## Mudanças em relação à Sprint 3
- Menu de texto → interface web; a lógica continua em Python.
- Busca e Bubble Sort agora também devolvem a **contagem de comparações** (para demonstrar Big-O).
- A ordenação trabalha numa **cópia** da lista (a ordem de cadastro é preservada).
- Campo opcional "hora" para demonstrar a tarifa de pico a qualquer momento.
- A tarifa de pico passou a usar 3 casas decimais (ex.: 0,90 × 1,25 = R$ 1,125) para evitar arredondamento do Python (`round(1.125, 2)` dá 1.12).
- Novos: relatório final e análise de complexidade medida.
- Dados ficam em memória (somem ao fechar o servidor) — persistência é uma evolução futura.
