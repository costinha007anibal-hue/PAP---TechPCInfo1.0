# Etapa 2 – Versão PHP do TechPCInfo

## Objetivo

Disponibilizar o sistema com backend em **PHP**, adequado a alojamento escolar (Apache/XAMPP), mantendo o frontend e a API compatíveis com a versão Python.

## Ficheiros principais

| Ficheiro | Função |
|----------|--------|
| `api/index.php` | Endpoints REST |
| `api/Database.php` | SQLite + schema + seed |
| `api/helpers.php` | JSON, users, PCs, imagens, 2FA |
| `router.php` | Servidor embutido PHP |

## Como testar

```bash
php -S 0.0.0.0:8080 router.php
curl http://localhost:8080/api/health
```
