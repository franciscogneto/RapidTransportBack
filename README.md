# Rodando o projeto
#### primeiro no prompt insira o seguinte comando:

```
git clone https://github.com/franciscogneto/RapidTransportBack.git
```
#### Criando ambiente virtual:
##### -> dentro da pasta gerada a partir do prompt insira o seguinte comando:
```
pyhton -m venv nome_que_desejar
```
##### -> ativando a venv:
```
\nome\Scripts\activate
```

#### instalando os pacotes para ser possível a execução:
##### -> acesse o diretório gerado pelo git clone através do prompt
##### -> execute o seguinte comando:


```
pip install -r requirements.txt
```

#### Aplicando as migrations necessárias:
##### -> acesse o diretório "rapidtransport" e execute o seguinte comando:

```
python manage.py migrate
```

#### Rodando o servidor:

```
python manage.py runserver
```

#### acesse o seguinte link para abrir o projeto: 

[localhost](http:127.0.0.1:8000)
## Aperte CLTR+C no prompt caso queira incessar o servidor

##### -> desativando a venv:
```
\nome\Scripts\deactivate
```
