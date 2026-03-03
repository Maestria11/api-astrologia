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
        nome_seguro = "MapaTeste"
        
        cliente = AstrologicalSubject(
            nome_seguro, dados.ano, dados.mes, dados.dia, dados.hora, dados.minuto, dados.cidade, "BR"
        )
        
        mapa_grafico = KerykeionChartSVG(cliente, chart_type="Natal", new_output_directory="/tmp")
        mapa_grafico.makeSVG()
        
        caminho_arquivo = f"/tmp/{nome_seguro} - Natal Chart.svg"
        
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo_svg = arquivo.read()
            
        os.remove(caminho_arquivo)

        # Pegamos exatamente o que importa e criamos um resumo limpo para o ChatGPT ler
        resumo_astrologico = (
            f"Sol em {cliente.sun.sign}, "
            f"Lua em {cliente.moon.sign}, "
            f"Ascendente em {cliente.first_house.sign}, "
            f"Mercúrio em {cliente.mercury.sign}, "
            f"Vênus em {cliente.venus.sign}, "
            f"Marte em {cliente.mars.sign}."
        )

        return {
            "sucesso": True,
            "cliente": dados.nome,
            "resumo_astros": resumo_astrologico, # Isso vai direto para a IA
            "imagem_svg": conteudo_svg
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao calcular: {str(e)}")
