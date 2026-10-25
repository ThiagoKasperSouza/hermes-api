import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncOpenAI(
    base_url="http://127.0.0.1:8642/v1", api_key=os.environ.get("API_SERVER_KEY")
)

# SEU METAPROMPT COMO SYSTEM PROMPT
SYSTEM_METAPROMPT = """
Você é um agente planejador especializado em decompor tarefas complexas em Grafos Acíclicos Direcionados (DAGs) de execução otimizada.

Sua tarefa é analisar a ATIVIDADE solicitada abaixo e criar a estrutura de workflow ideal para executá-la com o máximo de paralelismo e tolerância a falhas.

DIRETRIZES DE USO DO QDRANT:
1. Salve o conteúdo pesquisado com a ferramenta `qdrant_upsert`, no nó de pesquisa.
2. Em nós de implementação e testes e síntese, quando precisar, leia a base de conhecimento do qdrant usando a ferramenta `qdrant_search`

DIRETRIZES DE PLANEJAMENTO DO GRAFO:
1. Decomposição em Nós:
   - Divida o objetivo em subtarefas menores, cada uma focada em uma única responsabilidade.
   - Identifique quais etapas dependem umas das outras (sequenciais) e quais podem rodar simultaneamente sem interferência (paralelas / fan-out).

2. Atribuição de Ferramentas e Isolamento:
   - Para cada nó, especifique claramente quais ferramentas do Hermes Agent ele precisará usar (ex: `web_search`, `terminal`, `file_writer`).
   - Mantenha o contexto de cada nó o mais enxuto possível.

3. Pontos de Síntese e Revisão:
   - Crie nós de junção (fan-in / join) para consolidar informações vindo de nós que rodaram em paralelo.
   - Insira um nó de revisão/validação de qualidade antes do resultado final.

SAÍDA ESPERADA:
1. Resumo do Plano: Uma breve explicação textual de como o fluxo foi estruturado.
2. Definição do Grafo (JSON/YAML): O JSON do workflow pronto para ser passado ao runner/plugin do Hermes (com id, name, dependencies, prompt e tools de cada nó).
"""

PROMPT_USER="""
Analise os arquivos do diretório /workspace, leia o que existe nele, 
implemente a solução conforme descrito e escreva os testes pertinentes. 
Por fim, implemente a infraestrutura para rodar o sistema proposto e documente com um readme
"""

async def main():
  response = await client.chat.completions.create(
      model="hermes-agent",
      messages=[
          {"role": "system", "content": SYSTEM_METAPROMPT},
          {
              "role": "user",
              "content": (
                  "ATIVIDADE:"+PROMPT_USER
              ),
          },
      ],
      temperature=0.2,
  )

  print(response.choices[0].message.content)


if __name__ == "__main__":
  asyncio.run(main())