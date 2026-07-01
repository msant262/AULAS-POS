---
name: aula-interativa-okami
description: >
  Cria guias interativos em HTML único autocontido no modelo Okami: alta densidade
  de conteúdo, modais +Info, simuladores, gráficos, highlights editoriais, quiz,
  labs e exportação PDF pelo navegador. Use ao pedir nova aula, próximo módulo,
  material de graduação/mentoria/workshop, guia denso para compartilhar, ou
  publicar só o .html no GitHub msant262/AULAS-POS. Não é específico de OWASP —
  é o padrão de produto que qualquer tema pode reutilizar.
---

# Modelo Okami — guia interativo autocontido

Este documento descreve o **padrão de produto**, não um tema específico. A referência
de implementação vive em `Documents/Aulas/POS/OWASP` (tema AppSec), mas a próxima
aula pode ser API Security, Cloud, IA, compliance, etc. — mesma estrutura, outro conteúdo.

## O que o aluno recebe

Um único `.html` (~1–4 MB) dentro de uma pasta temática no GitHub (`TEMA-GUIA/arquivo.html`).

- Abre com **duplo clique** — sem Python, servidor ou instalação
- Funciona **offline** (CSS, JS, fontes e dados embutidos)
- **PDF:** botão *Exportar PDF* → `window.print()` → Salvar como PDF no navegador

## O que o autor mantém localmente

Código-fonte **não** vai no repo público de aulas (salvo pedido explícito). Fluxo:

1. Editar conteúdo e comportamento na máquina de desenvolvimento
2. Rodar o **gerador** → produz o HTML único
3. Commitar **só** `TEMA-GUIA/nome-guia.html` (+ `README.md` se necessário)

---

## Princípios do modelo

### 1. Densidade sem cronograma

O material é **referência rica para o participante**, não roteiro de instrutor.

- Nada de tempos (`0–5 min`, `40′`), notas de professor, “meta da disciplina”
- Conteúdo denso nos modais (aba **+ Info**), não em slides vazios
- Highlights editoriais espalhados **dentro** das seções, não concentrados num bloco só

### 2. Tom neutro e reutilizável

Serve graduação, pós, mentoria, workshop ou autoestudo. **Evitar:**

`pós-graduação`, `disciplina`, `desta aula`, `nesta aula`, `alunos devem`, `acadêmico`,
`Modo aula`, `Material de aula`, `roteiro`, `módulo assimilado`

**Preferir:** `neste guia`, `nesta página`, `Modo apresentação`, `Quiz de verificação`, `você`

### 3. HTML 100% autocontido

- CSS do design system inline
- JS do shell + módulos interativos inline (padrão inject/bundle)
- Fontes em base64 (cache local na primeira build)
- Dados em `<script type="application/json" id="data-*">` — sem `fetch`, sem `<script src>`

### 4. Exploração em camadas

O participante não precisa ler tudo linearmente. Oferecer **múltiplos pontos de entrada:**

| Camada | Função |
|--------|--------|
| **Hub de itens** | Cards do tema principal — visão geral + atalhos |
| **+ Info** | Guia denso por item (conceitos, causas, detecção, mitigação, reflexão) |
| **Simulador** | Exploit → impacto → fix (aprendizado ativo) |
| **Matriz / correlação** | Cruzamento entre eixos do tema (clique filtra a página) |
| **Highlights** | Citações, casos reais, discussão, dicas — **espalhados por seção** |
| **Gráficos** | Dados de mercado, ranking, tendências — canvas + legenda clicável |
| **Notícias / pesquisa** | Feed editorial com tags ligadas aos itens do hub |
| **Terminal / IDE** | Labs práticos opcionais (reprodução + correção) |
| **Cofre de código** | Padrão vulnerável ↔ correção, por linguagem ou contexto |
| **Quiz** | Verificação de correlação, não memorização de ranking |

### 5. Cards não abrem o modal inteiro

Cada card do hub tem botões explícitos:

- **+ Info** → modal na aba guia
- **Simulador** → scroll para o lab daquele item

Dentro do simulador: botão **+ Info** também, sem sair da seção.

---

## Anatomia da página (seções-tipo)

Adaptar IDs e títulos ao tema. Ordem sugerida:

```
#intro          → hero, lede, barra de fontes primárias, highlights iniciais
#contexto       → panorama do mercado / estado da arte (stats + gráficos)
#pesquisa       → hub de pesquisa, notícias, timeline de incidentes
#correlacao     → matriz ou mapa de cruzamento (se o tema tiver 2+ eixos)
#hub            → cards dos N itens principais do guia
#simuladores    → labs interativos (um bloco por item ou agrupados)
#terminal       → CLI didático (opcional)
#codigo          → cofre de padrões código (opcional)
#lab-externo     → setup de ambiente prático (Docker, clone, etc.) — opcional
#ide             → editor interativo com trechos editáveis — opcional
#quiz            → verificação final
```

Nem toda aula precisa de todas. O gerador e o menu lateral refletem o que existir.

---

## Como espalhar o conteúdo (padrão de dados)

Separar **papéis**, não nomes de arquivo fixos:

### A. Catálogo principal

Lista dos itens do hub: id, título, resumo, stats, tags, casos, links, labs associados.
É o esqueleto — cada item alimenta card, modal, filtro da matriz e busca.

### B. Guia denso por item (+ Info)

Um registro por item com campos como:

- visão geral, pontos-chave, conceitos
- cadeia de ataque / fluxo do problema
- causas raiz, detecção, mitigação
- prática sugerida, reflexão, referências

**Regra:** texto suficiente para o participante estudar sozinho; sem falas de instrutor.

### C. Highlights editoriais

Blocos curtos com `sections: [...]` indicando **onde** aparecem na página:

| type | Uso |
|------|-----|
| `quote` | Citação de fonte primária |
| `caso` | Incidente ou exemplo documentado |
| `highlight` | Destaque técnico com bullets |
| `aprendizado` | Dica de estudo / correlação |
| `pos` | Discussão (rótulo visível: **Discussão**) |
| `mencao` | Menção a autor ou referência clássica |

Espalhar 2–4 trechos por seção relevante — cria ritmo de leitura e profundidade sem inflar o hero.

### D. Feed de notícias / intel

Cards com data, fonte, resumo, corpo, bullets, stats, tags de item (`topic`, `subtopic`).
Clicar ou filtrar conecta ao hub e à matriz.

### E. Gráficos

Dados como arrays JSON; o shell renderiza canvas (barras, rosca, ranking, delta).
Cada gráfico: título, legenda, hint de interação, takeaway opcional.

### F. Simuladores

Config por item: cenário, input, presets, estados vulnerável/fix, saída do terminal simulado.
Lógica no módulo JS do simulador; config separada da prosa.

### G. Quiz

Perguntas que cruzam conceitos (não “qual é o #1 do ranking”). Feedback aponta para lab ou modal.

### H. Labs terminal / IDE

Comandos → respostas pré-definidas; fluxo reproduzir → entender → corrigir → validar.

---

## Pipeline de geração (papel dos componentes)

```
[design system CSS]     → aparência Okami (tokens, componentes)
[gerador]               → orquestra: fontes + CSS + template + dados + JS
[renderizadores]        → funções que montam HTML de cards, modais, rails, gráficos
[catálogo + guias]      → conteúdo estruturado (itens, +Info)
[highlights + notícias] → conteúdo editorial espalhado
[configs de sim/lab]    → comportamento interativo
[shell JS]              → navegação, tabs, busca, filtros, print, quiz, charts
        ↓
TEMA-GUIA/nome-guia.html   (único arquivo de distribuição)
```

**Gerador deve:** embutir fontes, inline CSS/JS, serializar JSON com escape seguro para `</script>`,
validar que não restam dependências externas.

---

## Checklist — nova aula com este modelo

### 1. Escopo

- Tema, público, fontes primárias, itens do hub (quantos? qual eixo?)
- Labs externos necessários? (opcional)
- Nome da pasta GitHub + nome do `.html`
- Quais seções-tipo usar (nem todas são obrigatórias)

### 2. Scaffold

- Copiar projeto de referência Okami ou criar pasta irmã em `Aulas/POS/<TEMA>/`
- Ajustar gerador: `OUT_DIR`, título, lede, seções do template, menu lateral
- Brand neutra na toolbar (`// domínio · tema`)

### 3. Conteúdo (prioridade)

1. Catálogo dos itens do hub
2. Guia denso (+ Info) por item
3. Highlights por seção (espalhar, não concentrar)
4. Contexto + gráficos com dados reais e fonte citada
5. Simuladores dos itens mais didáticos
6. Quiz cruzando conceitos
7. Notícias / timeline se houver material atual

### 4. UI

- Design system Okami; skill auxiliar `frontend-design` se precisar de direção visual
- Modais com abas; scroll reset ao trocar aba
- Busca global; matriz clicável filtra página inteira
- Modo apresentação (esconde chrome)

### 5. Validar

```bash
python3 <gerador>    # ou comando equivalente do projeto
```

- Sem `<link href=` / `<script src=` ativos
- Grep de linguagem proibida (tom acadêmico/contextual)
- Abrir HTML local: hub, +Info, sims, gráficos, quiz, Exportar PDF

### 6. Publicar

```bash
git add TEMA-GUIA/nome-guia.html
git commit -m "Adiciona guia <TEMA>"
git push origin main
```

Repo: `https://github.com/msant262/AULAS-POS.git` — atualizar tabela do `README.md`.

---

## O que NÃO fazer

- Não amarrar a skill a um tema (OWASP, CWE, Juice Shop) — são exemplos, não requisitos
- Não commitar fontes no repo público sem pedido
- Não pedir servidor local ao participante
- Não colocar o HTML na raiz do repo — sempre `PASTA/arquivo.html`
- Não trocar densidade por cronograma ou notas de instrutor

---

## Referência de implementação

O projeto **OWASP** nesta pasta é a **primeira instância** deste modelo (AppSec, matriz 10×25,
Juice Shop, etc.). Use-o como inspiração de densidade e de como os dados se distribuem — não
como lista de arquivos obrigatória.

Detalhes de seções e fluxo de modais: [references/architecture.md](references/architecture.md)

> **Sincronizar cópias:** este arquivo ↔ `.agents/skills/aula-interativa-okami/SKILL.md`