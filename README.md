# Rodando o projeto
primeiro no prompt insira o seguinte comando:
# Markdown
```
git clone https://github.com/franciscogneto/RapidTransportBack.git
```

instalando os pacotes para ser possível a execução:
-> acesse o diretório gerado pelo git clone através do prompt
-> execute o seguinte comando:

# Markdown
```
pip install -r requirements.txt
```

Aplicando as migrations necessárias:
-> acesse o diretório "rapidtransport" e execute o seguinte comando:
# Markdown
```
python manage.py migrate
```

Rodando o servidor:
# Markdown
```
python manage.py runserver
```

acesse o seguinte link para abrir o projeto: 
# Markdown

[localhost](http:127.0.0.1:8000)
