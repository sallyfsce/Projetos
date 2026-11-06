"""
app.py — CAMADA DE INTEGRAÇÃO (Flask)
Recebe as requisições da interface web, chama as funções de sistema.py
(onde está a lógica em Python) e devolve o resultado em JSON.

Fluxo:  Interface (navegador) -> rota Flask -> sistema.py -> JSON -> Interface

Como rodar:
    pip install flask
    python app.py
    (abra http://127.0.0.1:5000 no navegador)
"""

from flask import Flask, jsonify, request
import sistema

app = Flask(__name__, static_folder="static", static_url_path="/static")


def log(msg):
    """Mostra no terminal o que o backend Python está fazendo."""
    print(f"[BACKEND] {msg}")


@app.errorhandler(ValueError)
def erro_de_validacao(erro):
    # Qualquer ValueError levantado em sistema.py vira resposta 400 com a mensagem
    return jsonify({"erro": str(erro)}), 400


@app.route("/")
def pagina_inicial():
    return app.send_static_file("index.html")


@app.route("/api/sessoes", methods=["GET"])
def listar():
    log(f"listar_sessoes -> {len(sistema.sessoes)} sessão(ões)")
    return jsonify([s.para_dict() for s in sistema.sessoes])


@app.route("/api/sessoes", methods=["POST"])
def cadastrar():
    d = request.get_json()
    nova = sistema.cadastrar_sessao(
        d.get("usuario"), d.get("veiculo"), d.get("tipo_carregador"),
        d.get("tipo_usuario"), d.get("tempo"), d.get("energia"), d.get("hora"))
    log(f"cadastrar_sessao -> ID {nova.id}, tarifa R$ {nova.tarifa}/kWh, custo R$ {nova.custo}")
    return jsonify(nova.para_dict()), 201


@app.route("/api/sessoes", methods=["DELETE"])
def limpar():
    sistema.limpar_sessoes()
    log("limpar_sessoes -> lista vazia")
    return jsonify({"ok": True})


@app.route("/api/exemplo", methods=["POST"])
def exemplo():
    sistema.carregar_exemplos()
    log(f"carregar_exemplos -> total agora: {len(sistema.sessoes)}")
    return jsonify({"total": len(sistema.sessoes)})


@app.route("/api/buscar/<int:id_procurado>")
def buscar(id_procurado):
    indice, comparacoes = sistema.busca_sequencial(sistema.sessoes, id_procurado)
    log(f"busca_sequencial(ID {id_procurado}) -> índice {indice}, {comparacoes} comparações")
    sessao = sistema.sessoes[indice].para_dict() if indice != -1 else None
    return jsonify({"sessao": sessao, "indice": indice, "comparacoes": comparacoes,
                    "total": len(sistema.sessoes)})


@app.route("/api/ordenar")
def ordenar():
    campo = request.args.get("campo", "id")
    decrescente = request.args.get("ordem") == "desc"
    lista, comparacoes, trocas = sistema.ordenar_sessoes(campo, decrescente)
    log(f"bubble_sort(campo={campo}) -> {comparacoes} comparações, {trocas} trocas")
    return jsonify({"sessoes": [s.para_dict() for s in lista],
                    "comparacoes": comparacoes, "trocas": trocas})


@app.route("/api/estatisticas")
def estatisticas():
    log("calcular_estatisticas")
    return jsonify(sistema.calcular_estatisticas())


@app.route("/api/relatorio")
def relatorio():
    log("gerar_relatorio")
    return jsonify(sistema.gerar_relatorio())


@app.route("/api/complexidade")
def complexidade():
    log("analisar_complexidade")
    return jsonify(sistema.analisar_complexidade())


if __name__ == "__main__":
    print("Servidor Python iniciado em http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
