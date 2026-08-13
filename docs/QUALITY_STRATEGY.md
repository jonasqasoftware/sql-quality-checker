# Estratégia de Qualidade

## Contexto

Sistemas de e-commerce podem manter dados tecnicamente válidos para o banco e, ainda assim, violar regras de negócio: pedidos pagos sem data de pagamento, clientes duplicados ou produtos indisponíveis para venda.

Este laboratório transforma regras declaradas em consultas SQL revisáveis. As tabelas e os dados são sintéticos; não representam clientes, faturamento ou incidentes reais.

## Riscos priorizados

| Risco | Impacto potencial | Verificação |
| --- | --- | --- |
| Pedido órfão | Relatórios e relacionamento de cliente incorretos | `orders_with_unknown_users.sql` |
| Valor não positivo | Distorção de faturamento | `invalid_order_values.sql` |
| Pagamento incompleto | Estado financeiro inconsistente | `paid_orders_without_payment_date.sql` |
| E-mail duplicado | Comunicação e identidade ambíguas | `duplicate_emails.sql` |
| Estoque indisponível | Experiência de compra incorreta | `products_without_stock_for_sale.sql` |
| Cliente ativo sem pedidos | Segmentação ou onboarding a investigar | `active_users_without_orders.sql` |

## Estratégia e evidências

- Cada consulta retorna o mesmo contrato de saída para permitir agregação de resultados.
- O executor recria o banco sintético a cada execução, evitando dependência de estado anterior.
- CSV favorece análise tabular; HTML oferece leitura rápida por pessoas.
- O pipeline executa os testes e publica os relatórios sintéticos como artefatos.

## Limitações e risco residual

- As verificações são exemplos de regras de negócio e precisam ser revisadas no contexto de cada produto.
- A ferramenta não acessa bancos reais, não aplica correções e não substitui controles transacionais.
- Um relatório aponta inconsistências encontradas nos dados consultados; não mede cobertura de dados nem garante ausência de outros problemas.
