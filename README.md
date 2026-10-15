# SQL Quality Checker

<p align="center">
  <img src="docs/brand/social-preview.png" alt="Jonas Davila: engenharia de qualidade com evidência, clareza e método" width="100%">
</p>

[![CI](https://github.com/jonasqasoftware/sql-quality-checker/actions/workflows/quality.yml/badge.svg)](https://github.com/jonasqasoftware/sql-quality-checker/actions/workflows/quality.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-1e2024.svg)](LICENSE) [![Jonas Davila](https://img.shields.io/badge/portfolio-jonasdavila.com.br-a8432f.svg)](https://jonasdavila.com.br/en/)

> **In English:** A Quality Engineering lab that runs e-commerce business rules as SQL against a synthetic SQLite database and produces CSV and HTML inconsistency reports. Python standard library only.

> Projeto de automação de validações de qualidade de dados usando SQL. Simula regras de negócio de um e-commerce e identifica inconsistências que podem afetar clientes, faturamento e relatórios.

O SQL Quality Checker é um laboratório de Engenharia de Qualidade que executa regras de negócio diretamente em um banco SQLite sintético e produz relatórios CSV e HTML revisáveis. Ele demonstra como SQL pode transformar riscos de dados em verificações automáticas, sem afirmar que os dados ou os resultados representam um ambiente de produção.

## O que este projeto demonstra

- regras de negócio legíveis e independentes em SQL;
- validação de integridade, faturamento, pagamento, estoque e identidade de clientes;
- execução determinística em Python, sem dependências externas;
- relatórios para análise técnica e comunicação de inconsistências;
- CI no GitHub Actions com artefatos gerados a partir do cenário sintético.

## Regras verificadas

| Verificação | Risco de negócio |
| --- | --- |
| Usuário `ACTIVE` sem pedidos | Segmentação, onboarding ou dados de pedido a investigar. |
| Pedido com valor negativo ou zero | Faturamento incorreto. |
| Pedido `PAID` sem data de pagamento | Estado financeiro incompleto. |
| Cliente duplicado por e-mail | Comunicação e identidade ambíguas. |
| Produto sem estoque disponível para venda | Venda de item indisponível. |
| Pedido com usuário inexistente | Integridade referencial quebrada. |

## Arquitetura

```text
schema SQL + seed sintético + consultas SQL
                 |
                 v
       executor Python determinístico
                 |
                 v
     relatório CSV + relatório HTML + artefato de CI
```

```text
sql-quality-checker/
├── database/       # esquema e dados sintéticos
├── checks/         # uma regra de negócio por consulta SQL
├── src/            # executor e geradores de relatório
├── tests/          # testes do executor e dos relatórios
├── reports/        # saídas locais ignoradas pelo Git
└── .github/        # pipeline de validação e artefato
```

## Como executar

Requer Python 3.10 ou superior. Não há dependências externas.

```bash
python -m unittest discover -s tests -v
python src/run_checks.py --reports-dir reports
```

A execução recria o banco SQLite sintético e gera:

- `reports/quality-report.csv`
- `reports/quality-report.html`

Por padrão, o cenário contém inconsistências intencionais e termina com código `0` para que o relatório possa ser gerado no CI. Para usar a ferramenta como um gate em outro cenário, habilite:

```bash
python src/run_checks.py --reports-dir reports --fail-on-findings
```

Também é possível gravar o banco de laboratório para inspeção local:

```bash
python src/run_checks.py --database reports/lab.db --reports-dir reports
```

## Estratégia de Qualidade

As regras, riscos priorizados, evidências e limites estão documentados em [Estratégia de Qualidade](docs/QUALITY_STRATEGY.md).

Cada consulta deve retornar as colunas `finding_id`, `severity`, `entity_type`, `entity_id`, `rule` e `details`. Esse contrato mantém os relatórios consistentes e deixa cada regra fácil de revisar separadamente.

## CI e evidências

O GitHub Actions executa os testes unitários, gera os dois relatórios do cenário sintético e os publica como artefato do workflow. O artefato comprova apenas a execução daquele workflow; ele não é evidência de dados reais nem aprovação de release.

## Limitações

- O banco e os dados são sintéticos e reinicializados a cada execução.
- A ferramenta detecta inconsistências, mas não altera dados.
- Regras de negócio devem ser validadas com produto, dados e contexto operacional antes de serem adotadas em um sistema real.
- Ausência de findings não prova qualidade total dos dados.

## Licença

[MIT](LICENSE)
