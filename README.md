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
nome\Scripts\activate
```

#### instalando os pacotes para ser possível a execução:
##### -> acesse o diretório gerado pelo git clone através do prompt
##### -> execute o seguinte comando:


```
pip install -r requirements.txt
```
#### -> Vá para a o diretório rapidtransport
#### Rodando o servidor:
```
python manage.py runserver
```

#### acesse o seguinte link para abrir o projeto: 

[localhost](http:127.0.0.1:8000)
###### Aperte CLTR+C no prompt caso queira encerrar o servidor


##### -> desativando a venv:
######(no diretório onde se encontra a venv)
```
\nome\Scripts\deactivate
```
