# Análise Completa do Projeto TechPCInfo
**Etapa 0 – Análise inicial dos documentos e regras**  
Data: 2026-10-21  
Alunos: Martim Aníbal Costa Ferreira (n.º 8610) e Rodrigo Loureiro (n.º 8613)  
Curso: Técnico de Gestão de Equipamentos Informáticos – 3.º ano – 2026/2027  

---

## 1. Documentos analisados

| Ficheiro | Tipo | Conteúdo principal |
|----------|------|--------------------|
| `3Ano_TGEI_8610_8613_PAP.doc` | Anteprojeto da PAP | Identificação, título, objetivos, metodologias, recursos |
| `TechPCInfo-Projeto.pdf` | Documentação técnica | Funcionalidades, arquitetura, estrutura de pastas, execução, segurança |
| `AGENTS.md` | Regras do utilizador para o assistente | Download no fim de cada tarefa, descrição de alterações, GitHub, links e síntese de código |

---

## 2. Resumo do projeto

**Nome:** TechPCInfo – Gestão de Dispositivos Empresariais  

**Objetivo:** Sistema web local (rede LAN / Wi-Fi escolar ou empresarial) para inventariar, consultar e registar manutenções de PCs e equipamentos, usando códigos QR físicos, fotografias e perfis de utilizador com diferentes permissões.

**Stack tecnológica:**
- Frontend: HTML5, Tailwind CSS (CDN), JavaScript vanilla
- Backend: Python 3 (`server.py` – ThreadingHTTPServer ou Flask conforme documentos)
- Base de dados: SQLite (`data/inventory.db`)
- Bibliotecas: qrcodejs, html5-qrcode
- Acesso: PC e telemóvel na mesma rede; suporte HTTPS local para câmara

**Perfis de utilizador:**
1. **Administrador** (única conta: admin@admin.pt) – CRUD completo de equipamentos, gestão de contas, inventário
2. **Técnico** (email @tech.pt) – Consulta + registo de manutenções
3. **Utilizador** (outros emails) – Apenas visualização

**Funcionalidades principais:**
- Inventário de equipamentos com foto obrigatória (câmara ao vivo ou ficheiro)
- Geração de QR Code com URL direta à ficha (`/dispositivo/ID`)
- Histórico de manutenções (preventiva/corretiva)
- Temas claro/escuro e wallpapers personalizados
- Relatórios PDF/DOC
- Soft-delete com zona de eliminados + recuperação
- 2FA (código gerado no login; SMTP futuro)
- Assistente de ajuda “Tec”

**Estrutura de pastas prevista:**
```
pc-inventory/
├── server.py
├── index.html          (login + 2FA)
├── register.html
├── terms.html
├── dashboard.html
├── pc-detail.html
├── admin.html
├── scan.html
├── settings.html
├── js/  css/  assets/  data/inventory.db  reports/
```

---

## 3. Regras do utilizador (AGENTS.md) – cumprimento obrigatório

1. No fim de **cada tarefa** → disponibilizar download do produto editado + descrever as alterações feitas.
2. Guardar **cada chat ou ficheiro** enviado como ficheiro importante (já feito nesta pasta `analise_inicial/`).
3. Para tudo o que for implementado → indicar **links consultados** + **síntese das linhas de código** das principais funções.
4. Todos os trabalhos → gravados no repositório GitHub **[PAP---TechPCInfo1.0](https://github.com/costinha007anibal-hue/PAP---TechPCInfo1.0)**, com etapas numeradas e descrição no commit / README.

---

## 4. Estado atual e próximos passos

- Documentos oficiais e técnicos analisados e arquivados.
- Conta GitHub identificada: `costinha007anibal-hue` (Martim Ferreira).
- **Repositório criado e acessível:** [https://github.com/costinha007anibal-hue/PAP---TechPCInfo1.0](https://github.com/costinha007anibal-hue/PAP---TechPCInfo1.0)
- Permissões de push confirmadas.
- Esta análise (Etapa 0) foi enviada para o repositório.

**Próximo passo (Etapa 1):** criar a estrutura inicial do projeto (pastas, server.py base, páginas HTML esqueleto) e fazer commit numerado.

---

## 5. Síntese de funções principais previstas (para implementação futura)

| Função / Área | Descrição resumida | Ficheiros prováveis |
|---------------|--------------------|---------------------|
| Autenticação + 2FA | Login, registo em 2 passos, geração de código | `server.py`, `index.html`, `register.html` |
| CRUD Equipamentos | Criar/editar/eliminar/recuperar com foto e ID automático | `admin.html`, API em `server.py` |
| Geração QR | QR com URL base configurável → `/dispositivo/{id}` | `pc-detail.html` + qrcodejs |
| Scan QR | Leitura com câmara (html5-qrcode) | `scan.html` |
| Manutenções | Registo e histórico por equipamento | `pc-detail.html` + API |
| Temas / Wallpapers | Alternância claro/escuro + upload de imagens | `settings.html`, CSS |
| Relatórios | Exportação PDF/DOC da ficha + manutenções | `reports/` + biblioteca PDF |

---

**Fim da Etapa 0 – Análise completa.**  
Repositório ativo. Próximo passo: Etapa 1 – estrutura inicial do código.
