# Rodando o projeto
#### h4 primeiro no prompt insira o seguinte comando:

```
git clone https://github.com/franciscogneto/RapidTransportBack.git
```

instalando os pacotes para ser possível a execução:
-> acesse o diretório gerado pelo git clone através do prompt
-> execute o seguinte comando:


```
pip install -r requirements.txt
```

Aplicando as migrations necessárias:
-> acesse o diretório "rapidtransport" e execute o seguinte comando:

```
python manage.py migrate
```

Rodando o servidor:

```
python manage.py runserver
```

acesse o seguinte link para abrir o projeto: 


[localhost](http:127.0.0.1:8000)
