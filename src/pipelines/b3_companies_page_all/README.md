# **B3 Companies Page All**

![Vídeo demonstrativo](../../../assets/br_companies_page_all_terminal.gif)

Este pipeline extrai **todas as informações de todas as empresas listadas no site da B3**, sem depender de uma base prévia de nomes ou CNPJs.

### Vantagens em relação ao `b3_companies_page_search`

* Não precisa fornecer uma lista de empresas;
* Evita problemas de **seleção de bloco** que podem ocorrer quando o nome da empresa não bate exatamente com o exibido na B3;
* Permite coletar **todas as empresas**, mesmo aquelas sem balanço patrimonial disponível.

Caso o cliente queira, é possível aplicar **filtros posteriores** para selecionar apenas empresas com informações específicas.
