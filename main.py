import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kerykeion import AstrologicalSubject, KerykeionChartSVG

app = FastAPI()

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
        # Fixamos um nome padrão sem espaços ou acentos para evitar qualquer erro
        nome_seguro = "MapaTeste"
        
        cliente = AstrologicalSubject(
            nome_seguro, dados.ano, dados.mes, dados.dia, dados.hora, dados.minuto, dados.cidade, "BR"
        )
        
        # O Kerykeion salva na pasta temporária (/tmp) do Render
        mapa_grafico = KerykeionChartSVG(cliente, chart_type="Natal", new_output_directory="/tmp")
        mapa_grafico.makeSVG()
        
        # Agora sim! Buscamos EXATAMENTE o padrão de nome que o log nos mostrou que ele cria
        caminho_arquivo = f"/tmp/{nome_seguro} - Natal Chart.svg"
        
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo_svg = arquivo.read()
            
        # Limpamos o arquivo logo após ler
        os.remove(caminho_arquivo)

        return {
            "sucesso": True,
            "cliente": dados.nome,
            "planetas": cliente.planets_degrees_past,
            "casas": cliente.houses_degree_past,
            "imagem_svg": conteudo_svg
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao calcular: {str(e)}")
