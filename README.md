# **Financial Data Pipelines**

* Python
* ETL
* OOP
* SQLite

Executa pipelines de extração, transformação e carga (ETL) de dados financeiros.

**Objetivo:**
Organizar e padronizar todos os dados financeiros brasileiros disponíveis.

---

## **Pipelines incluídos**

* **[Formulário de Informações Trimestrais](src/pipelines/cvm_formulario_informacoes_trismestrais/README.md)** — coleta do balanço patrimonial trimestral.

* **[B3 Companies Page Search](src/pipelines/b3_companies_page_search/README.md)** — busca informações no site da B3 sobre empresas com balanço patrimonial registrado na CVM.

* **[B3 Companies Page All](src/pipelines/b3_companies_page_all/README.md)** — coleta todas as informações disponíveis sobre todos os ativos listados no site da B3.


---

## **Como usar**

### **1. Clonar o repositório**

```bash
git clone https://github.com/rianlucascs/financial_data_pipelines.git
cd financial_data_pipelines
```

### **2. Criar e ativar o ambiente virtual**

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### **3. Instalar dependências**

```bash
pip install -r requirements.txt
```

### **4. Executar todos os pipelines**

O arquivo **run.bat** executa **todos os pipelines do projeto em sequência**.

```bash
run.bat
```

---

## **Contato**

[**WhatsApp**](https://wa.me/556199450747)


