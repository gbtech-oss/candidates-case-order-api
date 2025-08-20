# order-api

## Descrição

Este projeto é uma API Django para gerenciamento de pedidos e itens, utilizando Django REST Framework e Poetry para gerenciamento de dependências.

## Entidades

### Pedido (Order)
- **id**: Identificador único do pedido.
- **client_name**: Nome do cliente (até 300 caracteres).
- **client_document**: CPF do cliente (apenas números).
- **delivery_date**: Data de entrega do pedido.
- **delivery_address**: Endereço de entrega associado ao pedido (opcional).
- **items**: Lista de itens associados ao pedido (opcional).
- **created_at**: Data/hora de criação do pedido.
- **updated_at**: Data/hora da última atualização do pedido.

### Item
- **id**: Identificador único do item.
- **order**: Referência ao pedido.
- **name**: Nome do item.
- **quantity**: Quantidade do item.
- **unit_price**: Preço unitário do item.

### Endereço de Entrega (DeliveryAddress)
- **id**: Identificador único do endereço.
- **street_name**: Nome da rua (até 255 caracteres).
- **number**: Número do endereço (até 20 caracteres).
- **complement**: Complemento (opcional, até 255 caracteres).
- **reference_point**: Ponto de referência (opcional, até 255 caracteres).

## Como rodar o projeto localmente

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd order-api
   ```

2. **Ative o ambiente Python desejado (opcional):**
   ```bash
   pyenv activate order-api
   ```

3. **Instale o Poetry (caso não tenha):**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   export PATH="$HOME/.local/bin:$PATH"
   ```

4. **Instale as dependências:**
   ```bash
   poetry install
   ```

5. **Aplique as migrações:**
   ```bash
   poetry run python manage.py migrate
   ```

6. **Rode o servidor de desenvolvimento:**
   ```bash
   poetry run python manage.py runserver
   ```


## Documentação da API

O projeto possui documentação interativa gerada automaticamente:

- **Swagger UI:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Redoc:** [http://localhost:8000/doc/](http://localhost:8000/doc/)

Nessas páginas você pode visualizar e testar todos os endpoints disponíveis de forma prática.

## O que é possível fazer com a API

- Criar um novo pedido (com ou sem itens e endereço de entrega)
- Incluir itens em um pedido já criado
- Atualizar apenas o endereço de entrega de um pedido
- Remover itens de um pedido
- Buscar pedidos por documento do cliente e/ou data de entrega
- Consultar detalhes de um pedido, incluindo o preço total

## Observações
- O projeto utiliza Django REST Framework para a criação dos endpoints.
- Os endpoints permitem criar, atualizar (adicionar itens) e consultar pedidos, incluindo o cálculo do preço total.
- Para customizações, consulte os arquivos em `order/models.py`, `order/serializers.py` e `order/views.py`.


## Banco de Dados

O projeto utiliza o banco de dados SQLite.

# Base de Conhecimento

A base de conhecimento para o case está localizada na pasta `knowledge_base` no arquivo `knowledge_base.sql`.