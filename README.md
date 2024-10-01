<h1 align="center"> Case Técnico Boticário </h1>

# Índice 

* [Questão 1](#Questão-1)
* [Questão 2](#Questão-2)
* [Questão 3](#Questão-3)
* [Questão 4](#Questão-4)

Para os códigos em SQL, usei o SQL LITE por meio da plataforma DBeaver.

Para todos os programas em python, deixei um requirements.txt no repositório para mostrar as bibliotecas utilizadas.

## Questão 1

Para comparar as bases, subi os CSV no Dbeaver (onde todas as colunas foram como texto, por meio do "script_create", a fim de não perder informações com transformações numéricas). 

Dividi a query ("script_validate") em duas partes.
Na primeira, fiz uma validação se havia duplicados em cada tabela, e se fazendo um merge entre ambas pelo ID retornaria os mesmos valores. O GCP, aparentemente, não trouxe alguns registros e duplicou outros. 

![img 1 sql](https://github.com/user-attachments/assets/03d9c533-4c8b-4075-940d-289b6bd15d21)

Comparando os valores entre as colunas, dentro do merge, temos o seguinte resultado.

![img1](https://github.com/user-attachments/assets/36bd055e-1f8d-428e-9041-51e771d06b22)

Com esse código, conseguimos saber quais colunas estão com divergências entre a tabela do GCP e a LOCAL.
Pegando as colunas que estão com divergências, fiz outra query ("script_validate_2") para saber exatamente quais eram as divergências encontradas.
A coluna CODE_GENDER está como "MALE" e "FEMALE" no GCP. Ao passo que na base local estava como "M" ou "F".

![img2](https://github.com/user-attachments/assets/33800b1a-9b76-40f9-8bf8-6b7b99449f3a)

A variável AMT_INCOME_TOTAL está com zeros a mais no GCP antes do ponto.

![img3](https://github.com/user-attachments/assets/17e49e18-630c-4b6b-a8de-4f4717e18e16)

A variável DAYS_BIRTH está sem o sinal negativo, "-", no GCP.

![img4](https://github.com/user-attachments/assets/c14bf737-897f-4edf-99e5-17638b16c2c9)

A variável FLAG_WORK_PHONE está como decimal na GCP...

![img5](https://github.com/user-attachments/assets/3cea9013-6027-43ce-8923-b65d69dd9384)

...e ocorrem algumas inconsistências onde ela vem vazia.

![img6](https://github.com/user-attachments/assets/1c306216-8162-43de-b619-32ae120139a7)

E, por fim, a variável OCCUPATION_TYPE, quando está vazia na base local, vem como "Without Occupation" no GCP.

![img7](https://github.com/user-attachments/assets/06aceecb-f7c0-4804-ae1a-241f1b71ace0)

Também fiz um código python ('validate.py') que gera um txt com as mesmas informações explanadas acima. O txt ficou da seguinte forma: 

![txt report](https://github.com/user-attachments/assets/fa5891e3-ec91-4b55-ba38-9fe414a83eb2)


## Questão 2

Para resolver a segunda questão, visto que o sql requer a data em um formato específico, ao carregar os CSV, fiz um script simples, posteriormente, para tratar as colunas de data. 

![update](https://github.com/user-attachments/assets/b883fb7e-e024-4a82-ae0a-fd0216cae6a1)

O script que responde a questão está com o nome "script_engineering" na pasta correspondente.

## Questão 3

Para a visualização do KS, criei um software simples no python para realizar de forma mais automatizada.

Só é necessário, nele, preencher o separador do CSV analisado; decimal, se houver; coluna do evento (no caso, a coluna de marcação, que diz se o cliente é bom ou mau); coluna de probabilidade (coluna do score); valor do evento (no caso, o que desejamos, cliente ser bom, para o programa converter em "1"); e valor do não evento (no caso, o cliente ser mau).

![imagem ks](https://github.com/user-attachments/assets/6ace7b2c-b2c1-4a94-a282-fb295b67bccc)

Após isso, selecionamos o CSV e o gráfico é gerado. 

![figure ks](https://github.com/user-attachments/assets/31cb301e-a90f-4877-ab61-91c9e13a195f)

O indicador do KS, basicamente, mede o quão bem o modelo distingue entre duas categorias, o que para o mercado de crédito, geralmente, é se o cliente é bom ou mau. 
O modelo indicado deu um valor de 0.57 de KS, o que representa uma eficácia excelente para um modelo de crédito, que tem como norte ter 0.30 ou quiçá 0.40 na maioria dos casos.

## Questão 4

Para responder a quarta questão, criei um programa que baixa diretamente do site do governo o CSV correspondente de 2023 e 2024. 

Como a questão é explícita em citar que deseja apenas o produto de NCM = 33030010 no Estado de São Paulo, fiz esse filtro. Subi, então, a visualização para um dashboard no streamlit, permitindo que se possa ver pelo código do país exportador, pelas diferentes formas de se ver o preço por KG ( por exemplo, com adição do frete ou com seguro, ou sem ambos), e também com um filtro para ver em real ou dólar. Também há um botão para atualizar os dados, visto que utilizei dados em cache para não prejudicar o uso do dashboard.
É válido dizer que, devido ao tamanho considerável dos CSV baixados, o carregamento inicial do dashboard pode demorar um pouco.

O dashboard ficou da seguinte forma: 

![dash](https://github.com/user-attachments/assets/818d8586-323e-4092-959c-e9f27adcc501)

O painel pode ser acessado pelo seguinte link:

https://dashboardprecos-boti.streamlit.app/
