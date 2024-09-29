<h1 align="center"> Case Técnico Boticário </h1>

QUESTÃO 1

Para comparar as bases, subi os CSV no Dbeaver (onde todas as colunas foram como texto, a fim de não perder informações com transformações numéricas). 
Fiz uma query para contar quantas linhas, por cada coluna, estavam distintas de uma tabela para outra, realizando o join das tabelas pela coluna ID. Como o join retornou o valor exato da quantidade de linhas do CSV, abandonei hipótese de que essa coluna também poderia estar divergente. O resultado pode ser visto no print abaixo:

![img1](https://github.com/user-attachments/assets/36bd055e-1f8d-428e-9041-51e771d06b22)

Com esse código, conseguimos saber quais colunas estão com divergências entre a tabela do GCP e a LOCAL.
Pegando as colunas que estão com divergências, fiz outra query para saber exatamente quais eram as divergências encontradas.
A coluna CODE_GENDER está como "MALE" e "FEMALE" no GCP. Ao passo que na base local estava como "M" ou "F".

![img2](https://github.com/user-attachments/assets/33800b1a-9b76-40f9-8bf8-6b7b99449f3a)

A variável AMT_INCOME_TOTAL está com zeros a mais no GCP antes do ponto.

![img3](https://github.com/user-attachments/assets/17e49e18-630c-4b6b-a8de-4f4717e18e16)

A variável DAYS_BIRTH está sem o sinal negativo, "-", no GCP.

![img4](https://github.com/user-attachments/assets/c14bf737-897f-4edf-99e5-17638b16c2c9)
