# Solucionador de Quebra-Cabeças 8-Puzzle com Interface Gráfica

Uma aplicação de desktop desenvolvida em Python com a biblioteca **customtkinter** para resolver o clássico quebra-cabeças de 8 peças (ou qualquer variação em um tabuleiro 3x3). A ferramenta permite que o usuário defina visualmente tanto o estado inicial quanto o estado final do quebra-cabeças e encontra o caminho mais curto para a solução.

## Características

  * **Interface Gráfica Intuitiva**: Criada com `customtkinter` para uma aparência moderna e agradável, compatível com temas claro e escuro.
  * **Entrada de Matriz Flexível**: Permite ao usuário definir graficamente qualquer configuração inicial e objetivo para o quebra-cabeças através de um formulário visual.
  * **Solucionador Otimizado**: Utiliza o algoritmo de busca \**A* (A-Estrela)\*\* com a heurística da Distância de Manhattan para encontrar o caminho mais curto de forma eficiente.
  * **Validação Completa**:
      * Verifica se as peças nas matrizes inicial e objetivo são as mesmas.
      * Valida a entrada do usuário para garantir que apenas números válidos sejam inseridos.
  * **Verificação de Solubilidade**: Antes de tentar resolver, o programa determina se uma solução é matematicamente possível, comparando a paridade de inversões dos dois estados.
  * **Exibição Clara da Solução**: Se uma solução for encontrada, o número de passos é exibido na janela principal e o caminho completo, passo a passo, é mostrado em uma nova janela de resultados.

## Tecnologias Utilizadas

  * **Python 3**: Linguagem base da aplicação.
  * **customtkinter**: Biblioteca para a criação da interface gráfica moderna.
  * **heapq**: Módulo padrão do Python, utilizado para implementar a fila de prioridade do algoritmo A\*.

## Pré-requisitos

Antes de executar, certifique-se de ter o seguinte instalado:

  * Python (versão 3.7 ou superior)
  * A biblioteca `customtkinter`

## Instalação

1.  **Clone o repositório (ou salve o arquivo .py):**
    Se você estiver no Git, pode clonar o repositório. Caso contrário, apenas salve o código Python em um arquivo chamado `puzzle_gui.py`.

2.  **Instale as dependências:**
    Abra seu terminal ou prompt de comando e instale a única dependência necessária:

    ```sh
    pip install customtkinter
    ```

## Como Executar

1.  Navegue até o diretório onde você salvou o arquivo `puzzle_gui.py`.
2.  Execute o script através do terminal:
    ```sh
    python puzzle_gui.py
    ```

## Como Usar a Aplicação

1.  Após executar o programa, a janela principal aparecerá.
2.  Preencha os 9 campos da **"Matriz Inicial"** com a configuração de início do seu quebra-cabeças. Use o número `0` para representar o espaço vazio.
3.  Preencha os 9 campos da **"Matriz Objetivo"** com a configuração que você deseja alcançar.
4.  Clique no botão **"Resolver"**.
5.  A área de status na parte inferior informará se uma solução foi encontrada, se é impossível de resolver ou se houve algum erro na entrada.
6.  Se uma solução for encontrada, uma nova janela se abrirá mostrando todos os passos, do início ao fim.
