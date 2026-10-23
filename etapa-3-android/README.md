# TechPCInfo – App Android (Etapa 3)

App Kotlin + WebView que abre o servidor TechPCInfo (PHP ou Python).

## Uso rápido

1. No PC: `php -S 0.0.0.0:8080 router.php` (ou `python server.py`)
2. Android Studio → Open pasta `techPCInfo-android` (ZIP de entrega) ou este código
3. Run no emulador
4. URL padrão: `http://10.0.2.2:8080`
5. Login: admin@admin.pt / admin123

## Ficheiros principais

- `MainActivity.kt` – WebView, câmara, reload
- `SettingsActivity.kt` – configurar URL do servidor
- `Prefs.kt` – guardar URL
- `AndroidManifest.xml` – INTERNET + CAMERA + cleartext HTTP

Pacote completo: `techPCInfo-android.zip` na entrega do projeto.
