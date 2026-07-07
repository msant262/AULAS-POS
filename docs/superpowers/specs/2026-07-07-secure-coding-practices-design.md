# Secure Coding Practices + IA Assistida - Design

Data: 2026-07-07
Status: aprovado para especificacao, aguardando revisao do usuario antes da implementacao
Repositorio: `AULAS-POS`
Destino do artefato final: `SEC-COD-PRAT/secure-coding-practices.html`

## Objetivo

Criar uma nova aula interativa no modelo Okami, em um unico arquivo HTML autocontido, sobre praticas de codigo seguro e uso seguro de IA no desenvolvimento de software.

O guia deve complementar a aula `OWASP-CWE/owasp-cwe-guia.html`. A aula OWASP-CWE apresenta riscos e fraquezas; esta nova aula deve mostrar como transformar esses riscos em rotina de engenharia: requisitos, design, codigo, dependencias, CI/CD, containers, IaC, revisao, operacao e governanca de IA.

## Decisoes Aprovadas

- Pasta: `SEC-COD-PRAT`, irma de `OWASP-CWE` dentro do repo `AULAS-POS`.
- Formato: um unico arquivo `html + css + javascript`, autocontido e offline.
- Proporcao editorial: aproximadamente 60% fundamentos de secure coding e 40% seguranca no uso de IA para desenvolvimento.
- Stacks prioritarias: TypeScript/JavaScript, Python, Java, C#, CI/CD, Docker, IaC.
- Supply chain sera pilar proprio: npm, pip, NuGet, Maven/Gradle, lockfiles, SCA, SBOM, assinatura/proveniencia, typosquatting, dependency confusion, slopsquatting e Log4Shell.
- Labs principais serao simulados no HTML. Havera uma secao opcional com comandos reais para pratica local.
- IA sera uma camada transversal da aula, nao apenas uma secao isolada.
- Havera uma secao reservada de referencias, com links para os materiais usados na pesquisa.
- Dados e graficos das fontes devem aparecer ao longo da aula para enriquecer contexto e tomada de decisao.

## Tese Da Aula

IA ja faz parte do SDLC. O problema nao e usar IA para codar; o problema e usar IA sem threat model, revisao, testes, rastreabilidade, sandbox, permissoes e gates de seguranca.

A aula deve repetir esse raciocinio em cada camada:

- Como fazer sem IA.
- Como a IA ajuda.
- Como a IA quebra.
- Qual gate impede o dano.

## Publico E Tom

Publico: participantes de pos, mentoria, workshop tecnico e autoestudo em AppSec, DevSecOps e engenharia de software.

Tom:

- Neutro, tecnico e reutilizavel.
- Usar "neste guia", "nesta pagina", "voce", "Modo apresentacao", "Quiz de verificacao".
- Evitar cronograma, notas de instrutor, "modo aula", "material de aula", "roteiro", "disciplina", "alunos devem".

## Estrutura Do Guia

### 1. Intro / Estado Da Arte

Hero com tese da aula, fontes primarias e metricas sobre:

- Adocao de IA no desenvolvimento.
- Uso diario por profissionais.
- Percentual de codigo gerado ou assistido por IA.
- Risco de codigo gerado por IA.
- Crescimento de agentes de codigo.
- Gargalo de revisao, validacao e governanca.

Componentes:

- Barra de fontes primarias.
- Cards de metricas.
- Graficos de adocao e risco.
- Highlights editoriais com citacoes curtas e links.

### 2. Mapa SDLC Seguro + IA

Matriz clicavel cruzando etapas do SDLC com controles:

- Requisitos e threat model.
- Design e arquitetura.
- Codigo.
- Dependencias.
- Build e pipeline.
- Deploy, Docker e IaC.
- Operacao e resposta.
- Governanca de IA.

Cada celula deve mostrar:

- Controle humano esperado.
- Uso seguro de IA.
- Risco se automatizar demais.
- Gate recomendado.
- Fonte relacionada.

### 3. Hub De Praticas Fundamentais

Cards com botoes explicitos:

- `+ Info`: abre modal denso.
- `Simular`: leva ao lab relacionado quando houver.
- `Checklist`: abre lista pratica.

Praticas-base:

1. Threat modeling e requisitos de seguranca.
2. Validacao de entrada e output encoding.
3. Autenticacao, sessao e autorizacao.
4. Secrets, chaves e variaveis de ambiente.
5. Criptografia e protecao de dados.
6. Erros, logs e observabilidade segura.
7. APIs, uploads e parsing de arquivos.
8. Dependencias e supply chain.
9. CI/CD, Docker e IaC seguros.
10. Uso seguro de IA e agentes no SDLC.

Campos de cada modal:

- Visao geral.
- Por que falha.
- Como detectar.
- Padrao vulneravel.
- Padrao seguro.
- Como pedir isso para uma IA sem induzir falha.
- Checklist de revisao.
- Referencias.

### 4. Cofre De Codigo

Tabs por contexto:

- TypeScript/JavaScript.
- Python.
- Java.
- C#.
- CI/CD.
- Docker.
- IaC.

Cada item:

- Trecho vulneravel.
- Trecho corrigido.
- Explicacao curta da falha.
- Controle correspondente.
- Teste ou gate que deveria pegar.
- Prompt ruim e prompt melhor para assistente de IA.

Exemplos previstos:

- SQL/NoSQL injection.
- XSS/output encoding.
- AuthZ quebrada/IDOR.
- Secrets em log ou variavel exposta.
- Crypto fraca ou implementacao caseira.
- Upload e path traversal.
- Erro verboso.
- Docker root e imagem inchada.
- IaC com bucket publico, security group aberto ou policy wildcard.
- GitHub Actions com token amplo, pull_request_target indevido ou secrets em contexto nao confiavel.

### 5. Supply Chain Lab

Simulador de decisao de biblioteca para npm, pip, NuGet e Maven/Gradle.

O aluno deve avaliar sinais:

- Nome e risco de typosquatting.
- Pacote inexistente sugerido por IA.
- Mantenedor e repositorio.
- Idade, atividade e releases.
- Downloads como sinal fraco, nao suficiente.
- Licenca.
- Lockfile.
- Dependencias transitivas.
- CVEs.
- SCA.
- SBOM.
- Assinatura/proveniencia.
- Possivel dependency confusion.
- Relacao com incidentes como Log4Shell.

Estados da decisao:

- Instalar.
- Bloquear.
- Investigar.
- Substituir.
- Isolar em sandbox.

### 6. IA No Desenvolvimento

Secao forte sobre IA como parte normal do trabalho de engenharia.

Topicos:

- Vibe coding como acelerador e risco.
- Assistentes inline, chat, agentes de terminal e agentes em PR.
- Agentes que leem repos, editam arquivos, rodam comandos, instalam dependencias e interagem com ferramentas externas.
- Prompt injection em arquivos do repositorio.
- Regras de projeto e arquivos de instrucao.
- MCP/plugins/conectores como superficie de ataque.
- Uso de contas pessoais e risco de dados sensiveis.
- Secrets, .env, tokens e credenciais.
- Sandboxing, permissoes, rede, aprovacao e telemetria.
- Rastreabilidade de codigo gerado por IA.
- Revisao humana e revisao automatizada.

Controles:

- Rodar agente em workspace isolado.
- Rede desligada por padrao ou allowlist.
- Permissao minima.
- Approval para rede, secrets, alteracao fora do workspace e comandos destrutivos.
- Nunca aceitar pacote sugerido por IA sem verificacao externa.
- Nunca colar segredo, log sensivel ou dado de cliente em ferramenta nao aprovada.
- Exigir testes e threat model no prompt.
- Exigir diff pequeno e reviewavel.
- Registrar origem/assistencia quando politica interna exigir.

### 7. PR Review Simulator

Um PR gerado por IA parece melhorar uma feature, mas contem problemas escondidos:

- AuthZ incompleta.
- Pacote suspeito ou inexistente.
- Log de segredo.
- Docker rodando como root.
- IaC com permissao ampla.
- Teste que cobre happy path, mas nao abuse case.
- Prompt ou comentario que tenta induzir o agente a ignorar regra.

Interacao:

- O aluno marca achados no diff.
- O simulador mostra severidade.
- O feedback conecta cada achado a uma pratica, gate e referencia.

### 8. Pipeline Gate Simulator

Pipeline visual com gates:

- Unit tests.
- Abuse tests.
- SAST.
- SCA.
- Secret scan.
- IaC scan.
- Container scan.
- SBOM.
- Assinatura/proveniencia.
- Review humano.
- Review assistido por IA.
- Approval para risco alto.

Interacao:

- O aluno liga/desliga gates.
- O simulador mostra quais riscos chegam a producao.
- O objetivo e mostrar que IA aumenta velocidade de criacao, entao feedback loops precisam ficar mais rapidos e mais fortes.

### 9. Lab Externo Opcional

Bloco opcional com comandos reais, sem ser requisito para usar o guia.

Comandos previstos:

```bash
npm audit
npm audit signatures
pip-audit
dotnet restore
dotnet list package --vulnerable
mvn org.owasp:dependency-check-maven:check
docker scout cves <image>
checkov -d .
gitleaks detect
```

Cada comando deve ter:

- O que detecta.
- Onde encaixa no pipeline.
- Limites e falsos positivos.
- Como transformar achado em acao de engenharia.

### 10. Quiz De Decisao

Perguntas de correlacao, nao memorizacao.

Cenarios:

- IA sugeriu pacote inexistente.
- Agente quer rodar script com rede.
- SCA achou CVE transitiva.
- PR passou testes, mas falhou threat model.
- Docker build funciona, mas roda como root.
- IaC passa deploy, mas abre bucket publico.
- Log ajuda debug, mas vaza PII.
- Prompt pede "codigo simples e rapido" e o modelo remove validacao.

### 11. Referencias E Materiais

Secao reservada no final, com links para os materiais usados na pesquisa.

Requisitos da secao:

- Cards por categoria: fundamentos, IA, agentes, supply chain, Docker/IaC, ferramentas.
- Filtro por tag.
- Link externo claro.
- Descricao curta do motivo de usar a fonte.
- Indicacao se a fonte e primaria, relatorio de mercado, paper ou documentacao de ferramenta.

Tambem deve haver referencias ao longo da aula:

- Highlights com fonte.
- Graficos com fonte visivel.
- Modais com lista de referencias.
- Cards de metricas clicaveis quando possivel.

## Graficos E Dados Planejados

### Grafico 1 - Adocao De IA No Desenvolvimento

Fontes:

- Stack Overflow Developer Survey 2025: 84% usam ou planejam usar IA no desenvolvimento; 50,6% dos profissionais usam diariamente.
- JetBrains State of Developer Ecosystem 2025: 85% usam IA regularmente para coding/dev; 62% usam assistente, agente ou editor com IA.
- GitHub Octoverse 2025: quase 80% dos novos devs no GitHub usam Copilot na primeira semana.

Visual:

- Barras comparativas.
- Legenda clicavel.
- Takeaway: IA virou parte normal do desenvolvimento, especialmente para novos devs e times profissionais.

### Grafico 2 - Codigo Assistido Por IA E Crescimento Esperado

Fonte:

- Sonar State of Code Developer Survey 2026: entre quem ja testou IA, 72% usa todo dia; desenvolvedores estimam 42% do codigo atual como gerado ou assistido por IA, com previsao de 65% em 2027.

Visual:

- Linha temporal 2023 -> 2027.
- Marcadores: 6%, 19%, 42%, 55%, 65%.
- Takeaway: o volume de codigo assistido cresce mais rapido que os processos de validacao tradicionais.

### Grafico 3 - Risco De Codigo Gerado Por IA

Fonte:

- Veracode 2025 GenAI Code Security Report: testes com mais de 100 LLMs em Java, Python, C# e JavaScript indicaram que 55% das tarefas resultaram em codigo seguro e 45% introduziram falhas conhecidas.

Visual:

- Donut seguro vs vulneravel.
- Barras por linguagem quando usadas: Python 62% pass rate, JavaScript 57%, C# 55%, Java 29%.
- Takeaway: funcional nao significa seguro.

### Grafico 4 - Gargalo De Revisao E Governanca

Fonte:

- GitLab AI Accountability / DevSecOps 2026: 91% das organizacoes usam duas ou mais ferramentas de IA para codigo; 85% veem gargalo migrar para revisao/validacao; 43% nao distinguem confiavelmente codigo gerado por IA de codigo humano.

Visual:

- Radar ou barras de gargalos.
- Takeaway: o controle precisa acompanhar a velocidade de geracao.

### Grafico 5 - Package Hallucination / Slopsquatting

Fonte:

- Paper "We Have a Package for You!" com 576.000 amostras de codigo; pelo menos 5,2% de pacotes alucinados em modelos comerciais e 21,7% em modelos open-source; 205.474 nomes unicos alucinados.

Visual:

- Barras comercial vs open-source.
- Fluxo: prompt -> pacote inexistente -> atacante registra -> instalacao -> compromise.
- Takeaway: dependencia sugerida por IA deve ser tratada como input nao confiavel.

### Grafico 6 - Impacto Organizacional Da IA

Fonte:

- DORA Impact of Generative AI in Software Development: aumento de 25% em adocao de IA associado a queda de 1,5% em throughput e 7,2% em estabilidade, quando feedback loops e governanca nao acompanham; politicas claras e tempo dedicado de aprendizado aumentam adocao.

Visual:

- Antes/depois ou matriz "AI speed vs delivery health".
- Takeaway: IA amplifica o sistema de engenharia existente.

## Fontes Principais

Fundamentos e AppSec:

- NIST SSDF SP 800-218 - https://csrc.nist.gov/pubs/sp/800/218/final
- OWASP Developer Guide - https://owasp.org/www-project-developer-guide/
- OWASP Secure Coding Practices Checklist - https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/stable-en/02-checklist/05-checklist
- OWASP Cheat Sheet Series - https://cheatsheetseries.owasp.org/
- OWASP ASVS - https://owasp.org/www-project-application-security-verification-standard/
- OWASP SAMM - https://owasp.org/www-project-samm/
- OWASP API Security Top 10 - https://owasp.org/www-project-api-security/
- CISA Secure by Design - https://www.cisa.gov/securebydesign

IA, agentes e codigo gerado:

- Stack Overflow Developer Survey 2025 - https://survey.stackoverflow.co/2025/ai/
- JetBrains State of Developer Ecosystem 2025 - https://blog.jetbrains.com/research/2025/10/state-of-developer-ecosystem-2025/
- GitHub Octoverse 2025 - https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
- DORA State of AI-assisted Software Development 2025 - https://dora.dev/research/2025/dora-report/
- DORA Impact of Generative AI in Software Development - https://dora.dev/ai/gen-ai-report/report/
- GitLab AI Accountability / DevSecOps 2026 - https://ir.gitlab.com/news/news-details/2026/GitLab-Research-Reveals-Organizations-Are-Generating-AI-Code-Faster-Than-They-Can-Control-It/default.aspx
- Veracode GenAI Code Security Report - https://www.veracode.com/blog/genai-code-security-report/
- OWASP Top 10 for LLM Applications - https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP AI Exchange - https://owasp.org/www-project-ai-security-and-privacy-guide/
- NIST AI RMF / GAI Profile - https://www.nist.gov/itl/ai-risk-management-framework
- MITRE ATLAS - https://atlas.mitre.org/
- OpenAI Running Codex Safely - https://openai.com/index/running-codex-safely/
- OpenAI Codex Agent Approvals & Security - https://developers.openai.com/codex/agent-approvals-security
- Claude Code Security - https://code.claude.com/docs/en/security
- Claude Code Permissions - https://code.claude.com/docs/en/permissions
- Claude Code Sandboxing - https://www.anthropic.com/engineering/claude-code-sandboxing

Supply chain e ferramentas:

- SLSA - https://slsa.dev/
- Sigstore - https://docs.sigstore.dev/about/overview/
- npm audit - https://docs.npmjs.com/cli/v9/commands/npm-audit
- npm package provenance - https://docs.npmjs.com/viewing-package-provenance/
- pip-audit - https://pypi.org/project/pip-audit/
- NuGet auditing - https://learn.microsoft.com/en-us/nuget/concepts/auditing-packages
- GitHub dependency review - https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review
- OWASP Dependency-Check - https://owasp.org/www-project-dependency-check/
- Docker build best practices - https://docs.docker.com/build/building/best-practices/
- Docker Scout - https://docs.docker.com/scout/
- OWASP Docker Security Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
- Kubernetes Pod Security Standards - https://kubernetes.io/docs/concepts/security/pod-security-standards/
- Checkov - https://www.checkov.io/1.Welcome/What%20is%20Checkov.html
- Package hallucination paper - https://arxiv.org/abs/2406.10279

## Design Visual

Reusar identidade Okami:

- Base dark.
- Tipografia Space Grotesk + JetBrains Mono.
- Acentos laranja, magenta e ciano.
- Cards com bordas finas e raio baixo.
- Toolbar fixa com busca, tema, modo apresentacao e exportar PDF.
- Sidebar com indices por grupo.
- Modais densos com tabs.
- Graficos em canvas sem dependencia externa.
- Highlights editoriais espalhados por secao.

A identidade visual deve seguir `OWASP-CWE/owasp-cwe-guia.html`, mas o tema desta aula deve ter personalidade propria:

- Laranja: controles fundamentais.
- Ciano: dados, telemetria, pipeline.
- Magenta: riscos de IA, agentes e supply chain.
- Verde: gates aprovados e controles efetivos.
- Amarelo: warnings, risco residual e revisao manual.

## Arquitetura Do HTML

O arquivo final deve conter:

- CSS inline, incluindo tokens Okami.
- JS inline.
- Dados em JSON embutido ou objetos JS locais.
- Fontes embutidas ou fallback local, sem dependencias externas ativas.
- Links externos apenas como referencias clicaveis, nao como assets necessarios.

Nao deve conter:

- `<script src=...>` ativo.
- `<link href=...>` externo ativo.
- `fetch()` para carregar dados obrigatorios.
- Dependencia de servidor local.

## Busca E Filtros

Busca global deve filtrar:

- Praticas.
- Trechos de codigo.
- Simuladores.
- Referencias.
- Fontes.
- Tags de IA, supply chain, CI/CD, Docker, IaC, linguagem e controle.

Filtros previstos:

- Fundamento.
- IA.
- Supply chain.
- Pipeline.
- Docker/IaC.
- TypeScript.
- Python.
- Java.
- C#.
- Ferramentas.
- Fonte primaria.
- Relatorio.
- Paper.

## Estados E Persistencia

Persistir no `localStorage` apenas preferencias nao sensiveis:

- Tema claro/escuro.
- Sidebar recolhida.
- Ultimo filtro selecionado.
- Progresso do quiz, se simples.

Nao persistir:

- Conteudo inserido pelo usuario em labs.
- Segredos.
- Dados pessoais.

## Acessibilidade E Responsividade

- Layout responsivo para desktop e mobile.
- Botao explicito para abrir modais.
- Foco visivel.
- Fechar modal com Escape.
- Labels claros em controles.
- Tabelas e graficos acompanhados de resumo textual.
- Texto sem sobreposicao.
- Sem fontes escaladas por viewport de forma instavel.

## Validacao Antes De Concluir

Comandos/checagens:

```bash
python3 <gerador>
rg "<script src=|<link href=|fetch\\(" SEC-COD-PRAT/secure-coding-practices.html
rg "pós-graduação|disciplina|desta aula|nesta aula|alunos devem|Modo aula|Material de aula|roteiro|módulo assimilado" SEC-COD-PRAT/secure-coding-practices.html
```

Verificacao manual/browser:

- Abrir HTML por duplo clique ou `file://`.
- Busca global.
- Modais `+ Info`.
- Matriz SDLC.
- Cofre de codigo.
- Graficos.
- Supply Chain Lab.
- PR Review Simulator.
- Agent Permission Lab.
- Pipeline Gate Simulator.
- Quiz.
- Tema claro/escuro.
- Modo apresentacao.
- Exportar PDF.
- Links da secao de referencias.

## Riscos De Implementacao

- Conteudo pode ficar grande demais se todos os modais forem escritos como artigos completos. Mitigacao: usar densidade alta, mas dividir em cards, tabs e checklists.
- Graficos podem virar decoracao se nao houver takeaway claro. Mitigacao: cada grafico deve ter fonte, interpretacao e acao recomendada.
- IA pode roubar o foco dos fundamentos. Mitigacao: todo topico de IA deve mapear para um controle classico ou gate.
- Exemplos de codigo podem ficar superficiais. Mitigacao: cada stack precisa ter pelo menos exemplos vulneravel -> seguro e criterio de review.
- Referencias podem virar lista passiva. Mitigacao: referencias tambem aparecem nos highlights e modais, e a secao final tem filtros.

## Fora De Escopo

- Criar aplicacao multi-arquivo para entrega publica.
- Exigir servidor local ao participante.
- Fazer laboratorio real obrigatorio.
- Substituir a aula OWASP-CWE.
- Cobrir todos os detalhes de cada linguagem, framework e cloud provider.
- Recomendar uma ferramenta de IA especifica como unica correta.

## Criterio De Sucesso

O resultado sera considerado bom se um participante conseguir:

- Entender por que secure coding continua sendo base mesmo com IA.
- Revisar codigo gerado por IA com criterio tecnico.
- Identificar riscos de dependencias, pacotes alucinados e supply chain.
- Saber onde colocar gates de SAST, SCA, secrets, IaC e container scan.
- Configurar mentalmente limites para agentes: sandbox, rede, permissoes, approvals e logs.
- Levar uma lista confiavel de referencias para estudo posterior.
