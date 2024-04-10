# Lacrei processo seletivo

Esse repositorio foi utilizado para realizar o desafio técnico da ONG [Lacrei Saúde](https://www.linkedin.com/company/lacrei-saude/).

## Stacks utilizadas

- Python
- Django
- Django rest framework
- Poetry
- Docker
- Docker compose
- PostgreSql

## Desafio

Criar uma api para cadastrar pessoas profissionais e agendar consultas com essas pessoas.

## Rotas

### Pessoa profissional

Cadastrar pessoa profissional:

```http
POST http://localhost:8000/professional
```

Encontrar pessoa profissional por seu id:

```http
GET http://localhost:8000/professional/<int:id>
```

Apagar pessoa profissional pelo id:

```http
DELETE http://localhost:8000/professional/<int:id>
```

Listar todas as pessoas profissionais cadastradas:

```http
GET http://localhost:8000/professional
```

### Consulta com pessoas profissionais

Agendar consulta com pessoa profissional

```http
POST http://localhost:8000/examination/professional/<int:id_da_pessoa_profissional>
```

Encontrar consultas pelo id da pessoa profissional

```http
GET http://localhost:8000/examination/professional/<int:id_da_pessoa_profissional>
```

Encontrar consulta pelo id

```http
GET http://localhost:8000/examination/<int:id>
```

Atualizar data ou profissional da consulta

```http
PATCH http://localhost:8000/examination/<int:id>
```

Buscar todas as consultas cadastradas

```http
GET http://localhost:8000/examination
```

## Como rodar o projeto

Primeiramente você precisa ter o Docker e o docker-compose instalados no seu sistema.

Com essas duas ferramentas instaladas você pode executar o comando a baixo:

```bash
docker compose up -d
```

Esse comando vai subir dois containers um rodando a api na porta `8000` e outro rodando o banco de dados na porta `5432`