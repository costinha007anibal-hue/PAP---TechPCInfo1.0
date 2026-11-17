# Etapa 4 — Protótipo Atualizado (MySQL + Backend Python)

Prototipo funcional atualizado do TechPCInfo.

## O que foi adicionado / alterado
- Backend Python (`server.py`) com suporte dual a **SQLite** e **MySQL**
- Camada de abstração de base de dados (`DbConn` / `DbCursor`)
- Scripts SQL MySQL:
  - `TechPCinfo_MySQL_API.sql` (schema compatível com a API)
  - `TechPCinfo_MySQL_criar_bd.sql` (schema normalizado)
- `config.json` para configurar o engine de BD
- Melhorias em emails, 2FA, wallpapers, etc.

## Como executar
```bash
pip install pymysql
python server.py
# Abre http://localhost:5500
```

Contas demo: admin/admin123, trabalhador/trab123, user/user123

## Ficheiros principais
- `server.py` — servidor + API REST
- `*.html` + `js/` + `css/` — frontend
- `data/*.sql` — schemas MySQL
- `config.json` — configuração

Este prototipo corresponde ao ficheiro `pc-inventory-alterado.zip` enviado.

**Data:** 2026-11-17
**Alunos:** Martim Aníbal Costa Ferreira (8610) e Rodrigo Loureiro (8613)
