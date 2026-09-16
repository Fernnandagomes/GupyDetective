# Gupy Detector

Ferramenta que monitora vagas publicadas na Gupy e avisa por e-mail. Feita porque acompanhar manualmente o portal de vagas todo dia é chato e fácil de esquecer.
<br> <br>  Link para cadastro: https://gupydetective-search.streamlit.app/

## Como funciona

1. A pessoa se cadastra em um formulário simples (Streamlit) informando e-mail, cargo de interesse, modelo de trabalho e cidade (opcionais os dois últimos).
2. O formulário envia esses dados via webhook para um fluxo no Power Automate, que grava o cadastro em uma planilha.
3. Todo dia às 8h, um segundo fluxo lê a planilha de cadastros, consulta a API pública da Gupy (`portal.gupy.io/api/job-search/jobs`) filtrando por cargo/cidade/modelo de cada pessoa, e separa só as vagas publicadas nos últimos 60 dias que ainda não foram enviadas antes.
4. Monta um e-mail com as vagas novas e envia. Sem duplicar vaga já enviada, sem spam.

## Stack

- **Front do cadastro:** Streamlit
- **Automação:** Power Automate (dois fluxos — recebimento do cadastro e envio diário)
- **Armazenamento:** planilha (Excel Online)
- **Fonte de dados:** API da Gupy

## Parâmetros da API da Gupy usados

```
jobName
city
state
workplaceType   (ex: remote)
limit / offset  (paginação)
```
Importante: são no singular e sem colchetes — diferente da URL de busca visual do site.

## Rodando localmente

```bash
pip install streamlit requests
streamlit run gupy_detector.py
```

Antes de rodar, cole a URL do webhook do Power Automate na variável `WEBHOOK_URL` no início do arquivo.

## Limitações atuais

- Depende do endpoint interno da Gupy continuar disponível como está (não é uma API pública documentada).
- Só cobre vagas da Gupy — não Indeed, InfoJobs ou LinkedIn.
- Sem autenticação no formulário: qualquer pessoa com o link pode se cadastrar.

## Próximos passos

- Deduplicação mais robusta de vagas já enviadas
- Página para a pessoa cancelar o próprio cadastro
- Testar filtro por múltiplos cargos por pessoa
