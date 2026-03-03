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
        # Usamos um nome fixo internamente para NUNCA dar erro de arquivo
        nome_arquivo_interno = "Mapa"
        
        cliente = AstrologicalSubject(
            nome_arquivo_interno, dados.ano, dados.mes, dados.dia, dados.hora, dados.minuto, dados.cidade, "BR"
        )
        
        # Usamos a pasta /tmp que é sempre liberada para escrita no Render
        mapa_grafico = KerykeionChartSVG(cliente, chart_type="Natal", new_output_directory="/tmp")
        mapa_grafico.makeSVG()
        
        # O arquivo sempre se chamará /tmp/MapaChart.svg, independente do cliente
        caminho_arquivo = "/tmp/MapaChart.svg"
        
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo_svg = arquivo.read()
            
        os.remove(caminho_arquivo)

        return {
            "sucesso": True,
            "cliente": dados.nome, # Devolvemos o nome real que o cliente digitou
            "planetas": cliente.planets_degrees_past,
            "casas": cliente.houses_degree_past,
            "imagem_svg": conteudo_svg
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao calcular: {str(e)}")
