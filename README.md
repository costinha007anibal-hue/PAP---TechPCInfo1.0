# TechPCInfo – PAP 1.0

**Sistema local de inventário de equipamentos** com códigos QR, manutenções e perfis.

**Autores:** Martim Aníbal Costa Ferreira (8610) · Rodrigo Loureiro (8613)  
Curso TGEI – 2026/2027

Repositório: https://github.com/costinha007anibal-hue/PAP---TechPCInfo1.0

## Etapas

| Etapa | Pasta | Descrição |
|-------|-------|-----------|
| 0 | `docs/etapa-0-analise/` | Análise inicial |
| 1 | `etapa-1-prototipo/` | Protótipo Python simples |
| 1.1 | site original | Câmara só mobile, PWA |
| **2** | **`etapa-2-php/`** | **Versão PHP + SQLite (API + frontend)** |

## Versão PHP (Etapa 2)

```bash
cd etapa-2-php
php -S 0.0.0.0:8080 router.php
# http://localhost:8080
```

Requer PHP com `pdo_sqlite`. Contas: `admin@admin.pt` / `admin123`

Pasta no GitHub: documentação + API PHP (`api/Database.php`, `api/helpers.php`, `router.php`).  
Pacote completo com HTML/JS/CSS/assets: usar o ZIP de entrega `pc-inventory-php.zip`.
