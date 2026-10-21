# App móvel + sincronização com o site (Etapa 1.1)

## É possível?

**Sim.** O modelo correto é um único servidor e base de dados; site (PC) e app (telemóvel) usam a mesma API.

- Uma única base de dados no servidor (SQLite agora; PostgreSQL depois).
- Site e app não guardam inventário em separado: ambos pedem e gravam via `/api/...`.
- Qualquer alteração num lado reflete-se no outro ao atualizar a lista.

## O que foi implementado

1. **PWA** – manifest.json + sw.js + ícones; instalar no Android (Chrome) e iOS (Safari).
2. **Secção no site** «Obter a app no telemóvel» – login, dashboard e definições + `/downloads/android.html` e `ios.html`.
3. **Mesmos PCs dos dois lados** – GET/POST `/api/equipment`, etc.

## App nativa (APK / IPA) – fase seguinte

Com **Capacitor** pode gerar-se APK Android a partir deste HTML/JS, apontando para o IP do servidor na LAN. iOS exige conta Apple Developer.

## Resumo para o relatório

A solução prevê um backend único e clientes web (PC) e móvel (PWA instalável). As alterações são sincronizadas porque ambos os clientes consomem a mesma API REST e a mesma base de dados.
