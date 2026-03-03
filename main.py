import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kerykeion import AstrologicalSubject, KerykeionChartSVG

app = FastAPI()

# Estrutura dos dados que seu site vai enviar para cá
class DadosCliente(BaseModel):
    nome: str
    ano: int
    mes: int
    dia: int
    hora: int
    minuto: int
    cidade: str

@app.post("/gerar-mapa")
def gerar_mapa(dados: DadosCliente):
    try:
        # 1. O Kerykeion faz o cálculo matemático
        # Nota: Estamos usando "BR" como país padrão para facilitar
        cliente = AstrologicalSubject(
            dados.nome, dados.ano, dados.mes, dados.dia, dados.hora, dados.minuto, dados.cidade, "BR"
        )
        
        # 2. Gera o desenho do mapa (SVG) e salva temporariamente
        nome_arquivo = f"{dados.nome}Chart.svg"
        mapa_grafico = KerykeionChartSVG(cliente, chart_type="Natal", new_output_directory=".")
        mapa_grafico.makeSVG()
        
        # 3. Lê a imagem gerada para enviar de volta ao seu site
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo_svg = arquivo.read()
            
        # 4. Apaga o arquivo temporário para não pesar o servidor
        os.remove(nome_arquivo)

        # 5. Devolve tudo mastigado para o seu site (Bubble, v0, etc)
        return {
            "sucesso": True,
            "cliente": dados.nome,
            "planetas": cliente.planets_degrees_past,
            "casas": cliente.houses_degree_past,
            "imagem_svg": conteudo_svg
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao calcular: {str(e)}")
