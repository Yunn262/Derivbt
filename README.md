# Deriv Signal Desk (Streamlit)

Aplicação de sinais técnicos somente leitura para índices sintéticos Deriv. Não coloca ordens.

## Executar localmente
1. Instale Python 3.10+.
2. Na pasta do projeto:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
3. Crie um App ID no portal de desenvolvedor da Deriv e insira-o na barra lateral.
4. Pressione **Conectar e analisar**.

## Deploy no Streamlit Community Cloud
Suba os arquivos para um repositório GitHub e escolha `app.py` como entrada. O `requirements.txt` instala dependências.

## Segurança
- O token API é opcional e não é usado por esta versão.
- Não cole tokens com permissão de negociação.
- Este projeto é experimental: regras técnicas não garantem acerto, confiança é heurística, não probabilidade calibrada.
- Verifique os símbolos suportados na API da Deriv; a lista pode variar por ambiente.
