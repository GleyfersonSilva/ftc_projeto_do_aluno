# O PROBLEMA DE NEGÓCIO
###  Contexto do Problema de Negócio
        Parabéns! Você acaba de ser contratado como Cientista de Dados da empresa
        Fome Zero, e a sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra
        a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer
        utilizando dados!
        A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
        business é facilitar o encontro e negociações de clientes e restaurantes. Os
        restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
        informações como endereço, tipo de culinária servida, se possui reservas, se faz
        entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
        dentre outras informações.
       
### Desafio
        
        O CEO Guerra também foi recém contratado e precisa entender melhor o negócio
        para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a
        Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da
        empresa e que sejam gerados dashboards, a partir dessas análises, para responder
        às seguintes perguntas:
        
### Geral
        1. Quantos restaurantes únicos estão registrados?
        2. Quantos países únicos estão registrados?
        3. Quantas cidades únicas estão registradas?
        4. Qual o total de avaliações feitas?
        5. Qual o total de tipos de culinária registrados?
### Países
        1. Qual o nome do país que possui mais cidades registradas?
        2. Qual o nome do país que possui mais restaurantes registrados?
        3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4
        registrados?
        4. Qual o nome do país que possui a maior quantidade de tipos de culinária
        distintos?
        5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
        6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem
        entrega?
        7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
        reservas?
        8. Qual o nome do país que possui, na média, a maior quantidade de avaliações
        registrada?
        9. Qual o nome do país que possui, na média, a maior nota média registrada?
        10. Qual o nome do país que possui, na média, a menor nota média registrada?
        11. Qual a média de preço de um prato para dois por país?
### Cidades
        1. Qual o nome da cidade que possui mais restaurantes registrados?
        2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
        4?
        3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de
        2.5?
        4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
        5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
        distintas?
        6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
        reservas?
        7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
        entregas?
        8. Qual o nome da cidade que possui a maior quantidade de restaurantes que
        aceitam pedidos online?
### Restaurantes
        1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
        2. Qual o nome do restaurante com a maior nota média?
        3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
        pessoas?
        4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
        média de avaliação?
        5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que
        possui a maior média de avaliação?
        6. Os restaurantes que aceitam pedido online são também, na média, os
        restaurantes que mais possuem avaliações registradas?
        7. Os restaurantes que fazem reservas são também, na média, os restaurantes que
        possuem o maior valor médio de um prato para duas pessoas?
        8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
        possuem um valor médio de prato para duas pessoas maior que as churrascarias
        americanas (BBQ)?
### Culinárias
        1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
        restaurante com a maior média de avaliação?
        2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
        restaurante com a menor média de avaliação?
        3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
        restaurante com a maior média de avaliação?
        4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
        restaurante com a menor média de avaliação?
        5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
        restaurante com a maior média de avaliação?
        6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
        restaurante com a menor média de avaliação?
        7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
        restaurante com a maior média de avaliação?
        8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
        restaurante com a menor média de avaliação?
        9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
        restaurante com a maior média de avaliação?
        10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
        restaurante com a menor média de avaliação?
        11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
        pessoas?
        12. Qual o tipo de culinária que possui a maior nota média?
        13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
        online e fazem entregas?
# PREMISSAS DO NEGÓCIO
    1. Foram utilizados dados de 6.942 restaurantes, em 15 países, 125 cidades e 166 culinárias distintas.
    2. Marketplace foi o modelo de negócio assumido.
    3. Foram consideradas 4 visões, Distribuição global, Visão por países, Visão por cidades e Visão por tipo de culinárias.
# ESTRATÉGIA DA SOLUÇÃO
    
    O painel estratégico foi desenvolvido utilizando métricas que refletem as 4 principais
    visões do modelo de negócio da empresa:
    
    1. Visão Global
    2. Visão Países
    3. Visão Cidades
    4. Visão Culinárias
### Visão Global
        1. Quantidade total de restaurantes cadastrados
        2. Quantidade total de países cadastrados
        3. Quantidade total de cidades cadastradas
        4. Quantidade total de culinárias cadastradas
        5. Quantidade total de avaliações cadastradas
        6. Distribuição global de restaurantes
### Visão Países
        1. Quantidade de restaurantes registrados por país
        2. Quantidade de cidades registradas por país
        3. Média de avaliações registaras por país
        4. Média do valor de um prato para duas pessoas por país
### Visão Cidades
        1. Top 10 cidades com mais restaurantes cadastrados
        2. Top 7 cidades com restaurantes com média de avaliação acima de 4.0
        3. Top 7 cidades com restaurantes com média de avaliação abaixo de 2.0
        4. Top 7 cidades com mais restaurantes com tipos de culinárias distintas
### Visão Culinárias
        1. Top 5 melhores restaurantes dos principais tipos culinários
        2. Top 5 piores restaurantes dos tipos de culinárias com menor média de avaliação
        3. Top 20 melhores restaurantes
        4. Top 20 piores restaurantes
        5. Top 20 melhores culinárias 
        6. Top 20 piores culinárias
# TOP 2 INSIGHTS DE DADOS
    1. A Indonésia é o país com maior custo de um prato para duas pessoas,
    possui 25% das avaliações registradas e 92% da média de avaliações dos restaurantes
    está acima de 4.0.
    2. O Brasil representa 55% dos top 20 restaurantes com menor avaliação registradas
    e é o país que possui o menor número de avaliações registradas.
# O PRODUTO FINAL DO PROJETO
    
    Painel online, hospedado em uma Cloud e disponível
    para acesso em qualquer dispositivo conectado a internet.
    
    O painel pode ser acessado através deste link:
    [https://gsilva-ftc-projeto-do-aluno.streamlit.app/](https://gsilva-ftc-projeto-do-aluno.streamlit.app/)
    
# CONCLUSÃO
    
    O objetivo desse projeto é criar um conjunto de gráficos e tabelas
    que exibam as métricas desejadas da melhor forma para o CEO.
    
    Da visão países e Cidades, podemos concluir que a Indonésia é o país que
    possui melhor performance de avaliações e de nível de avaliações.
    
# PRÓXIMOS PASSOS
    1. Criar novos filtros
    2. Categorizar os países por continentes
    3. Criar novas visões de negócio.
