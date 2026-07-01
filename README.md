# AULAS-POS

Materiais interativos para ensino de segurança e temas correlatos. Cada aula vive em sua própria pasta com um **HTML único autocontido** — o aluno não precisa instalar nada.

## Materiais publicados

| Pasta | Arquivo | Descrição |
|-------|---------|-----------|
| [OWASP-CWE](./OWASP-CWE/) | [owasp-cwe-guia.html](./OWASP-CWE/owasp-cwe-guia.html) | OWASP Top 10:2025 + CWE TOP 25 — guia interativo com simuladores, labs, quiz e matriz de correlação |

## Para alunos e participantes

1. Baixe ou abra o `.html` (duplo clique no arquivo).
2. Use no Chrome, Firefox ou Safari — funciona **offline**, sem Python nem servidor.
3. **Exportar PDF:** botão *Exportar PDF* → na janela de impressão, escolha *Salvar como PDF*.

Nenhuma instalação, conta ou repositório é necessária.

## Para o autor (gerar ou atualizar uma aula)

O código-fonte desta aula (Python/JS/CSS) fica na máquina de desenvolvimento, **não** no GitHub público. Só o HTML final é versionado aqui.

```bash
# Na pasta do projeto da aula (ex.: OWASP/)
python3 generate_html.py
```

Saída: `OWASP-CWE/owasp-cwe-guia.html` (~2,8 MB, tudo embutido: CSS, JS, fontes, dados).

Publicar no GitHub (só o HTML):

```bash
git add OWASP-CWE/owasp-cwe-guia.html
git commit -m "Atualiza guia OWASP-CWE"
git push origin main
```

## O que o HTML inclui

- Navegação por seções, busca e matriz OWASP↔CWE clicável
- Modais com aba **+ Info** (conteúdo denso por item)
- Simuladores OWASP e CWE com exploit + correção
- Terminal interativo e IDE Juice Shop
- Gráficos, notícias, timeline de breaches, quiz de verificação
- Modo apresentação e exportação PDF via navegador

## Próximas aulas

Use a skill **[SKILL.md](./SKILL.md)** (`aula-interativa-okami`) ao criar a próxima aula — modelo genérico Okami (HTML autocontido, densidade de conteúdo, highlights, gráficos, simuladores). Cópia do agente em `.agents/skills/aula-interativa-okami/SKILL.md`. OWASP é só a primeira instância do padrão.

## Repositório

https://github.com/msant262/AULAS-POS