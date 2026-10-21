# Alterações aplicadas no código (até Etapa 1.1)

## 1. Câmara QR só em smartphone
- `js/app.js` → isMobileDevice(), canUseCameraScan()
- `scan.html` → camera só se mobile; desktop mostra aviso
- `css/app.css` → .camera-only-mobile

## 2. Base de dados
- `server.py` → SQLite + seed (logins, PCs, manutenções, settings)
- Preparado para PostgreSQL na etapa seguinte

## 3. App móvel + sincronização
- PWA: manifest.json, sw.js, ícones
- Site e telemóvel → mesma API → mesmos PCs
- Secção «Obter a app» no login, dashboard e definições
- `/downloads/android.html` e `ios.html`

## Como correr
```bash
cd etapa-1-prototipo && python server.py
```
Contas: admin@admin.pt / admin123
