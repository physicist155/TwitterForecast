import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
import pytz
import requests
from datetime import datetime
from pytz import timezone
import os

def hora_atual_brasilia():
    # Define o fuso horário de Brasília
    fuso_brasilia = pytz.timezone("America/Sao_Paulo")
    # Obtém o horário atual em Brasília
    horario_brasilia = datetime.now(fuso_brasilia)
    # Retorna apenas a hora
    return horario_brasilia.hour

def definir_cor_retangulos(valor, tipo):
    if tipo == "temperatura":
        return "limegreen" if valor < 25 else "orange" if valor < 30 else "red"
    elif tipo == "pressao":
        return "lightblue" if valor > 1013 else "orange" if valor > 1000 else "red"
    elif tipo == "umidade":
        return "lightblue" if valor > 0.7 else "orange" if valor > 0.5 else "red"

descricao_icones = {
    "01d": "Céu limpo (dia)",
    "01n": "Céu limpo (noite)",
    "02d": "Poucas nuvens (dia)",
    "02n": "Poucas nuvens (noite)",
    "03d": "Nublado",
    "03n": "Nublado (noite)",
    "04d": "Muito nublado",
    "04n": "Muito nublado (noite)",
    "09d": "Chuvas leves",
    "09n": "Chuvas leves (noite)",
    "10d": "Chuvas com sol",
    "10n": "Chuvas (noite)",
    "11d": "Trovoadas",
    "11n": "Trovoadas (noite)",
    "50d": "Névoa",
    "50n": "Névoa (noite)",
}


pontos_prefeituras = [
    {"nome": "Ilhas dos Frades", "coordenadas": (-38.638, -12.785)}, #Ilhas dos Frades
    {"nome": "Ilha de Maré", "coordenadas": (-38.525, -12.775)}, #Ilhas de Maré
    {"nome": "Barra", "coordenadas": (-38.51, -13.005)},
    {"nome": "Pituba", "coordenadas": (-38.458, -12.993)},
    {"nome": "Brotas", "coordenadas": (-38.495, -12.98)},
    {"nome": "Liberdade", "coordenadas": (-38.483, -12.945)},
    {"nome": "Cidade Baixa", "coordenadas": (-38.505, -12.931)},
    {"nome": "Cabula", "coordenadas": (-38.453, -12.949)},
    {"nome": "Pau da Lima", "coordenadas": (-38.423, -12.924)},
    {"nome": "Cajazeiras", "coordenadas": (-38.413, -12.894)},
    {"nome": "Valéria", "coordenadas": (-38.448, -12.874)},
    {"nome": "Platafoma", "coordenadas": (-38.479, -12.894)},#Subúrbio 1
    {"nome": "Paripe", "coordenadas": (-38.478, -12.824)},
    {"nome": "Lauro de Freitas", "coordenadas": (-38.373, -12.864)},
    {"nome": "Itapuã", "coordenadas": (-38.353, -12.934)},
    {"nome": "Pituaçu", "coordenadas": (-38.413, -12.959)}
]

brasilia = timezone("America/Sao_Paulo")
api_key = os.getenv('OW_API_KEY')

shapefile_path = 'shapefiles/Prefeituras_Bairro.shx'

# Lê o arquivo shapefile
gdf = gpd.read_file(shapefile_path)
gdf_4326 = gdf.to_crs(epsg=4326)


brasilia = timezone("America/Sao_Paulo")
icones_usados = {}
fig, ax = plt.subplots(figsize=(8,8), dpi=300)
gdf_4326.plot(ax=ax, color="mediumseagreen", edgecolor="black", linewidth=0.5)


indice_previsao = 0

hora_atual = hora_atual_brasilia()

if  hora_atual == 19:
    indice_previsao = 3

elif hora_atual == 8:
    indice_previsao = 1

elif hora_atual == 16:
    indice_previsao = 0

temperaturas = []
pressoes = []
umidades = []

for ponto in pontos_prefeituras:
    lon,lat = ponto["coordenadas"]
    link_previsao_ponto = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'
    requisicao_previsao_ponto = requests.get(link_previsao_ponto)
    resultados_previsao_ponto = requisicao_previsao_ponto.json()
    icon = resultados_previsao_ponto['list'][indice_previsao]['weather'][0]['icon'] 
    img = mpimg.imread(f"iconesPrevisao/{icon}@2x.png")
    if icon not in icones_usados:
        icones_usados[icon] = descricao_icones.get(icon, "Descrição não encontrada")
    imagebox = OffsetImage(img, zoom=0.2, interpolation='bilinear')  
    ab = AnnotationBbox(imagebox, (lon,lat), frameon=False) 
    ax.add_artist(ab)
    nome = ponto['nome']
    ax.text(
        lon, lat + 0.007,  
        nome, fontsize=4, ha="center", color="black",
        bbox=dict(boxstyle="round,pad=0.2", edgecolor="none", facecolor="white")
    )
    temperaturas.append(resultados_previsao_ponto['list'][indice_previsao]['main']['temp'] - 273.15) #em celsius
    pressoes.append(resultados_previsao_ponto['list'][indice_previsao]['main']['pressure']) #em hPa
    umidades.append(resultados_previsao_ponto['list'][indice_previsao]['main']['humidity']/100) #em %

media_temperaturas = sum(temperaturas) / len(temperaturas)
media_pressoes = sum(pressoes) / len(pressoes)
media_umidades = sum(umidades) / len(umidades)


dt_brasilia = datetime.fromtimestamp(resultados_previsao_ponto['list'][indice_previsao]['dt'], tz=brasilia)

# Adicionar a legenda 
y_legenda = -13.015 # Posição vertical para a legenda
x_legenda = -38.66  # Posição horizontal para a legenda
dy = 0.02  # Espaçamento entre itens da legenda

for i, (icon, descricao) in enumerate(icones_usados.items()):
    img = mpimg.imread(f"iconesPrevisao/{icon}@2x.png")
    imagebox = OffsetImage(img, zoom=0.2)
    ab = AnnotationBbox(imagebox, (x_legenda, y_legenda + i * dy), frameon=False)
    ax.add_artist(ab)
    ax.text(
        x_legenda + 0.01, y_legenda + i * dy, descricao, fontsize=8, va="center", ha="left"
    )
# Coordenadas base para os retângulos dentro da borda
x_rect_start = 0.5  # Fração do eixo (percentual do tamanho)
y_rect_start = 0.9   # Fração do eixo
rect_width = 0.15     # Largura do retângulo (fração do eixo)
rect_height = 0.07   # Altura do retângulo (fração do eixo)
dx = 0.17            # Espaçamento horizontal (fração do eixo)

# Adicionar retângulos lado a lado
variaveis = [
    {"nome": "Temperatura\n", "valor": media_temperaturas, "tipo": "temperatura", "unidade": "°C"},
    {"nome": "Umidade\n", "valor": media_umidades * 100, "tipo": "umidade", "unidade": "%"},
    {"nome": "Pressão\n", "valor": media_pressoes, "tipo": "pressao", "unidade": "hPa"},
]

for i, var in enumerate(variaveis):
    # Determinar cor
    cor = definir_cor_retangulos(var["valor"], var["tipo"])
    
    # Coordenadas ajustadas para ficar na borda superior direita
    x_rect = x_rect_start + i * dx
    y_rect = y_rect_start

    # Desenhar o retângulo
    rect = Rectangle(
        (x_rect, y_rect),
        rect_width,
        rect_height,
        linewidth=1,
        edgecolor="none",
        facecolor=cor,
        transform=ax.transAxes,  # Posicionar em fração do eixo
        clip_on=False
    )
    ax.add_patch(rect)
    
    # Adicionar texto no centro do retângulo
    ax.text(
        x_rect + rect_width / 2,
        y_rect + rect_height / 2,
        f"{var['nome']} {var['valor']:.1f} {var['unidade']}",
        fontsize=8,
        ha="center",
        va="center",
        color="black",
        transform=ax.transAxes  # Posicionar em fração do eixo
    )
ax.set_aspect("equal")  
ax.set_title(f"Previsão do Tempo para {dt_brasilia.strftime('%d/%m/%Y às %H:%M:%S')}")

ax.set_xticks([])
ax.set_yticks([])
ax.set_facecolor("powderblue") 
# ax.axis('off')
plt.savefig('previsao.png', dpi=300,pad_inches=0.1, bbox_inches='tight')