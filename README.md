# TechPCInfo – PAP 1.0

**Sistema local de inventário de equipamentos** (PCs e dispositivos) com códigos QR, manutenções, perfis de utilizador e base de dados SQLite.

Projeto de **Prova de Aptidão Profissional (PAP)**  
Curso: Técnico de Gestão de Equipamentos Informáticos – 3.º ano  
Ano letivo: 2026/2027  

**Autores:**  
- Martim Aníbal Costa Ferreira (n.º 8610)  
- Rodrigo Loureiro (n.º 8613)  

Repositório: [PAP---TechPCInfo1.0](https://github.com/costinha007anibal-hue/PAP---TechPCInfo1.0)

---

## Etapas do desenvolvimento

| Etapa | Nome | Descrição | Data |
|-------|------|-----------|------|
| **0** | Análise inicial | Análise dos documentos da PAP e documentação técnica; regras de trabalho; resumo do projeto | 2026-10-21 |
| 1 | (próxima) | Estrutura inicial do código (server.py, páginas HTML, pastas) | — |

Cada commit e pasta de documentação usa numeração de etapa para identificar claramente o que foi alterado.

---

## Documentação da Etapa 0

Na pasta [`docs/etapa-0-analise/`](docs/etapa-0-analise/):

- `00_Analise_Completa_Projeto_TechPCInfo.md` – análise completa do projeto e regras
- `PAP_Anteprojeto_texto.txt` – texto extraído do anteprojeto da PAP
- `TechPCInfo_Documentacao_Tecnica_texto.txt` – texto extraído da documentação técnica

---

## Stack prevista

- **Frontend:** HTML5, Tailwind CSS, JavaScript (vanilla)
- **Backend:** Python 3 (`server.py`)
- **Base de dados:** SQLite
- **Extras:** QR Codes, câmara no browser, temas, relatórios PDF/DOC

---

## Como executar (quando o código estiver disponível)

```bash
python server.py
# http://localhost:5500
# Na rede: http://IP-DO-PC:5500
# Com HTTPS (câmara no telemóvel): python server.py --https
```

---

*Projeto em desenvolvimento contínuo. Todas as alterações são registadas por etapas numeradas.*
