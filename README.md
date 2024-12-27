# 🌤️ Previsão do Tempo para Salvador

Este repositório contém um script que gera previsões meteorológicas para diferentes regiões de Salvador, Bahia. Ele utiliza a API do OpenWeather e o GitHub Actions para automatizar a execução e o upload de previsões atualizadas em horários específicos do dia.

## 📋 Funcionalidades

- Geração de mapas de previsão do tempo com informações visuais e detalhadas.
- Atualizações automáticas três vezes ao dia: **08:10**, **16:10** e **19:10** (horário de Brasília).
- Upload automático da previsão gerada para a branch principal.

## 🚀 Como funciona?

1. **Script Python**: O script `previsaoSSA.py` faz requisições à API do OpenWeather, processa os dados e gera um mapa com a previsão.
2. **GitHub Actions**: O workflow `previsao_clima.yml` executa o script nos horários agendados e faz commit automático da imagem gerada (`previsao.png`) na branch `main`.

## 📦 Requisitos

- Python 3.10+
- Dependências listadas no arquivo `requirements.txt`:
  - `geopandas`
  - `matplotlib`
  - `pytz`
  - `requests`

## 🛠️ Configuração

1. Obtenha uma chave da API do OpenWeather [aqui](https://openweathermap.org/api).
2. Configure a chave no repositório como um segredo:
   - Acesse **Settings** > **Secrets and variables** > **Actions**.
   - Adicione um segredo chamado `OW_API_KEY` com a sua chave da API.

## ⚙️ Execução Manual

Você pode executar o workflow manualmente na aba **Actions** do GitHub:
1. Vá até o workflow **Previsão do Tempo**.
2. Clique em **Run workflow**.

## 📂 Estrutura do Repositório

- `previsaoSSA.py`: Script principal.
- `requirements.txt`: Lista de dependências.
- `shapefiles/`: Arquivos de forma para a geração dos mapas.
- `iconesPrevisao/`: Ícones usados para representar as condições climáticas.
- `.github/workflows/previsao_clima.yml`: Configuração do GitHub Actions.

## 🗺️ Exemplo de Resultado

A previsão gerada será salva no arquivo `previsao.png` e estará disponível na branch principal.

---

💡 **Dica**: Use este repositório como base para automatizar previsões meteorológicas de outras localidades!
