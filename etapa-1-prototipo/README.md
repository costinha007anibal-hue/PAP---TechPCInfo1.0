# TechPCInfo – Protótipo (Etapa 1)

Exemplo funcional para validar a ideia da PAP antes de desenvolver tudo.

## Ideias incorporadas nesta etapa

1. **Câmara QR só em dispositivos móveis**  
   Em computador/desktop a opção de scan com câmara **não aparece**.  
   Só é mostrada quando o browser é detetado como smartphone/tablet (UA + touch).  
   Serve para quando não há leitor de QR físico.

2. **Base de dados**  
   - Protótipo usa **SQLite** (`data/inventory.db`) para correr sem instalação extra.  
   - Schema e dados seed preparados para migração futura para **PostgreSQL**.  
   - Conteúdo seed: logins padrão, 3 PCs de exemplo, 1 manutenção, definições (base_url, pdf_style).

3. **App de exemplo**  
   Login (com 2FA simulado), dashboard, ficha com QR, pesquisa, admin (criar PC), definições.

## Como executar

```bash
cd etapa-1-prototipo
python server.py
```

- Neste PC: http://localhost:5500  
- Na rede: http://IP-DO-PC:5500  

### Contas de demonstração

| Email | Password | Papel |
|-------|----------|--------|
| admin@admin.pt | admin123 | Admin |
| tecnico@tech.pt | trab123 | Técnico |
| maria@escola.pt | user123 | Utilizador |

## Estrutura

```
etapa-1-prototipo/
├── server.py          # HTTP + API + SQLite
├── index.html         # Login
├── dashboard.html
├── pc-detail.html     # Ficha + QR
├── scan.html          # Pesquisa + câmara (só mobile)
├── admin.html
├── settings.html
├── register.html
├── js/app.js
├── css/app.css
├── data/              # inventory.db (criada ao arrancar)
├── assets/
└── reports/
```

## Nota sobre PostgreSQL

O protótipo corre em SQLite para ser imediato. O schema (tabelas `users`, `equipment`, `maintenances`, `settings`) é a base para PostgreSQL numa etapa seguinte.

## Síntese das funções principais (server.py)

| Função | Papel |
|--------|--------|
| `init_db()` | Cria tabelas + seed (logins, PCs, manutenção) |
| `TechPCHandler.do_GET/POST` | Serve HTML e API REST |
| `/api/login` | Autenticação + código 2FA de demo |
| `/api/equipment` | Listar / criar equipamentos |
| `/api/equipment/{id}` | Ficha + manutenções |
| `_next_code()` | Gera IDs automáticos PC-0001, PC-0002… |

| Função (js/app.js) | Papel |
|--------------------|--------|
| `isMobileDevice()` / `canUseCameraScan()` | Decide se mostra câmara QR |
| `requireAuth(roles)` | Protege páginas por papel |
| `apiGet` / `apiPost` | Chamadas à API |

## Links consultados / referências

- Documentação interna do projeto (PDF TechPCInfo + anteprojeto PAP)
- [html5-qrcode](https://github.com/mebjas/html5-qrcode) – leitura de QR no browser
- [qrcodejs](https://github.com/davidshimjs/qrcodejs) – geração de QR
- Tailwind CSS CDN – estilo rápido no protótipo
