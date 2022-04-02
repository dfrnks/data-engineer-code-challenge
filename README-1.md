# Everything begins in an ETL

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

Abre o endereço http://localhost:8090/ no navegador. 
Logue no banco utilizando as credenciais. Username: **postgres** Password: **password** Database: **CODE_CHALLENGE**

Irá aparecer na listagem duas tabelas *originations* e *payments* 
