# Answers

## Everything begins in an ETL

Para iniciar esse processo, digite no terminal

```shell
docker-compose up
```

Após aparecer os logs:

```shell

python_1   | INFO:root:Iniciando unzip files
python_1   | INFO:root:Iniciando a concatenção dos json files, path originations
python_1   | INFO:root:Inserindo na raw
python_1   | INFO:root:Iniciando a concatenção dos json files, path payments
python_1   | INFO:root:Inserindo na raw
python_1   | INFO:root:Iniciando processo ingestão payments
python_1   | INFO:root:Inserindo na trusted
python_1   | INFO:root:Inserindo na refined
python_1   | INFO:root:Finalizando processo ingestão payments
python_1   | INFO:root:Iniciando processo ingestão originations
python_1   | INFO:root:Inserindo na trusted
python_1   | INFO:root:Inserindo na refined
python_1   | INFO:root:Finalizando processo ingestão originations
data-engineer-code-challenge_python_1 exited with code 0

```

Abre o endereço http://localhost:8090/ no navegador, ou utilize a ferramenta de visualização de bancos de dados da sua preferencial.

Logue no banco utilizando as credenciais. Username: **postgres** Password: **password** Database: **CODE_CHALLENGE**

Irá aparecer na listagem três tabelas *bad_payer_rules*, *originations* e *payments*

Os arquivos gerados podem ser vistos no diretorio .ingest-data que foi gerado no diretorio local

## Spark

Assim que processar a ingestão ele começa a processar o classificação dos clientes

O processo gera uma tabela no banco de dados chamada *bad_payer_rules*

E o parquet no diretorio .ingest-data/trusted/bad_payer

## What about Governance and Privacy?

Governancia de dados e privacidade, existem algumas ferramentas para trabalhar com isso. 

Normalmente se utiliza alguma ferramenta de catálago de dados como Glue Catalag da AWS, ou Data Catalag da GCP e controle de acessos com usuários e grupos.

Com essas ferramentas é possível fazer duas coisas importantes, classificar colunas como sensíveis e configurar Row-level security (RLS) por grupos de usuários.

A classificação de colunas é importante pois numa tabela você pode ter colunas que contem dados sensíveis e nem todas as pessoas
podem ter acesso a eles, então com o catálago de dados é possível definir que determinado grupo tem acesso a determinadas colunas. 

Row-level security (RLS) ou segurança em nível de linha é outra possibilidade de ocultação de dados por grupos, nesse caso
é possível configurar para exibir linhas específicas parar grupos de usuário assim grupos diferentes pode ter acesso
a dados diferentes na mesma tabela. 

Com classificação de colunas e RLS que o catálago de dados disponibiliza é possível ter um controle total de governanca e privacidade.

Outra forma de tratar os dados sem utilizar catálagos de dados é salvar diferentes arquivos em diferentes diretorios, 
alguns arquivos com colunas específicas e/ou linhas específicas e liberar o acesso desses diretorios especificos para grupos diferentes. 

Além de que é possível usar uma técnica de hash de dados ou embaralhamento que a coluna não é excluída mas os dados são alterados
utilizando uma função de hash como SHA-256 por exemplo, assim podendo ainda utilizar a coluna para fazer algum tipo de comparação ou 
ligação com outras tabelas mas sem ter acesso ao dado original.

A técnica de ter vários diretorios funciona mas acaba que a quantidade de dados armazenadas é maior porque basicamente está
sendo feita uma duplicação de dados, mas seria uma alternativa a utilização de um catálago de dados do mercado. Principalmente se as pessoas
que utilizam os dados tem acesso direto aos arquivos e não utiliza alguma ferramenta como o Athena/Presto ou o BigQuery para acesso a esses dados.


