# TechPCInfo – versão PHP (Etapa 2)

Versão em **PHP + SQLite** do inventário TechPCInfo (mesmo frontend HTML/JS/CSS do site original, API reescrita em PHP).

## Requisitos

- PHP 8.1+ com extensão **pdo_sqlite**
- Apache (mod_rewrite) **ou** servidor embutido do PHP

### Verificar SQLite

```bash
php -m | grep -i pdo_sqlite
```

No Ubuntu/Debian: `sudo apt install php-sqlite3`

## Como executar

### Opção A – servidor embutido (desenvolvimento)

```bash
cd pc-inventory-php
php -S 0.0.0.0:8080 router.php
```

Abra: http://localhost:8080

### Opção B – Apache / XAMPP

1. Copie a pasta para `htdocs/pc-inventory-php` (ou virtual host).
2. Ative `mod_rewrite` e permita `.htaccess`.
3. Abra `http://localhost/pc-inventory-php/`

## Contas demo

| Email | Password | Papel |
|-------|----------|--------|
| admin@admin.pt | admin123 | Admin |
| tecnico@tech.pt | trab123 | Técnico |
| maria@escola.pt | user123 | Utilizador |

## API (compatível com o frontend existente)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/health` | Estado + caminho da BD |
| POST | `/api/login` | Login (+ demo 2FA) |
| POST | `/api/login/2fa` | Validar 2FA |
| POST | `/api/register` | Registo |
| GET/POST | `/api/pcs` | Listar / criar equipamentos |
| GET/PUT/DELETE | `/api/pcs/{id}` | Ficha / atualizar / arquivar |
| POST | `/api/pcs/{id}/manutencoes` | Nova manutenção |
| GET | `/api/logs` | Atividade |
| GET/POST | `/api/wallpapers` | Wallpapers custom |
| GET | `/api/users` | Lista utilizadores |
| PUT | `/api/profile` | Perfil |

Base de dados: `data/inventory.db` (criada automaticamente).

## Funcionalidades herdadas do site original

- Login / 2FA / registo / papéis (admin, worker, user)
- Dashboard, admin, ficha com QR, scan
- **Câmara QR só em telemóvel**
- **PWA** + secção «Obter a app» Android/iOS
- Mesma API → PC e telemóvel partilham inventário

Projeto PAP – TechPCInfo – Martim Aníbal Costa Ferreira (8610) e Rodrigo Loureiro (8613).
