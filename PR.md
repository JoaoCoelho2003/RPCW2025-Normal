# Descrição do Trabalho

## Criação da Ontologia

A estrutura da ontologia foi definida no Protégé, seguindo o método apresentado nas aulas. Foram criadas as classes, propriedades e relações necessárias para representar o domínio e o resultado final foi guardado no ficheiro `sapientia_base.ttl`.

## Povoamento da Ontologia

O povoamento da ontologia foi realizado utilizando o script `populate.py`. A única coisa diferente, quando comparado com o que fizemos nas aulas é que, para evitar repetição de código, foi implementada uma função auxiliar para adicionar os indivíduos.

O script também verifica se os indivíduos ou relações já existem antes de adicioná-los, evitando duplicações. Para executar o povoamento, basta rodar o seguinte comando:

```bash
python3 populate.py
```

A ontologia populada é guardada no ficheiro `sapientia_ind.ttl`.

## Queries sobre a Ontologia Populada
 
As queries SPARQL, tal como pedido no enunciado, estão no ficheiro sparql.txt.

## Script Python que cria a relação estudaCom

O script `estudaCom.py` calcula a relação estudaCom que é pedida no enunciado e, recorrendo ao insert, adiciona os novos triplos à ontologia. Para evitar modificar diretamente a ontologia populada, os resultados são inseridos num novo ficheiro TTL chamado `sapientia_ind_estudaCom.ttl`.

Para executar o script, utilize o seguinte comando:

```bash
python3 estudaCom.py
```

## Script Python que cria a relação daBasesPara

À semelhança do script anterior, o script `daBasesPara.py` calcula a relação daBasesPara pedida e insere os dados. Os resultados são guardados num ficheiro TTL chamado `sapientia_ind_daBasesPara.ttl`.

Para executar o script, utilize o seguinte comando:

```bash
python3 daBasesPara.py
```

## Organização dos Ficheiros

Para simplificar a organização dos ficheiros, foram criadas duas pastas: `ontologies` e `datasets`. A pasta `ontologies` contém os ficheiros relacionados com a ontologia (ficheiros .ttl), enquanto a pasta `datasets` contém os ficheiros relacionados com os datasets utilizados.

# Autor

João Coelho - PG55954