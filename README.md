# TechPCInfo – PAP 1.0

**Sistema local de inventário de equipamentos** (PCs e dispositivos) com códigos QR, manutenções, perfis de utilizador e base de dados.

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
| **0** | Análise inicial | Análise dos documentos da PAP e documentação técnica; regras de trabalho | 2026-10-21 |
| **1** | Protótipo / exemplo da app | App funcional de demonstração: login, dashboard, ficha+QR, scan (câmara só em mobile), admin; ideias da PAP incorporadas | 2026-10-22 |

Cada commit e pasta usa numeração de etapa.

---

## Protótipo (Etapa 1)

Pasta [`etapa-1-prototipo/`](etapa-1-prototipo/):

```bash
cd etapa-1-prototipo
python server.py
# http://localhost:5500
```

Contas demo: `admin@admin.pt` / `admin123` · `tecnico@tech.pt` / `trab123` · `maria@escola.pt` / `user123`

**Ideias já aplicadas:**
- Câmara QR **apenas** em smartphone/tablet (não aparece em PC desktop)
- SQLite no protótipo; schema pronto para PostgreSQL
- Logins e equipamentos de exemplo pré-carregados

---

## Documentação Etapa 0

[`docs/etapa-0-analise/`](docs/etapa-0-analise/)

---

*Projeto em desenvolvimento contínuo. Alterações registadas por etapas numeradas.*
