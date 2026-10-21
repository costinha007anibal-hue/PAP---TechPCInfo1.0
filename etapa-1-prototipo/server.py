#!/usr/bin/env python3
"""
TechPCInfo – Protótipo (Etapa 1)
Servidor local com API + SQLite (estrutura preparada para PostgreSQL).
Uso:
  python server.py
  http://localhost:5500
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import sqlite3
import ssl
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "inventory.db"
PORT = 5500

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    display_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin','tecnico','utilizador')),
    photo TEXT,
    twofa_enabled INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    location TEXT,
    type TEXT,
    brand TEXT,
    model TEXT,
    cpu TEXT,
    ram TEXT,
    storage TEXT,
    os TEXT,
    serial TEXT,
    mac TEXT,
    ip TEXT,
    acquisition_date TEXT,
    status TEXT DEFAULT 'ativo',
    notes TEXT,
    photo TEXT,
    deleted INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS maintenances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    type TEXT CHECK(type IN ('preventiva','corretiva')),
    description TEXT,
    technician TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
"""

SEED_USERS = [
    ("admin@admin.pt", "admin123", "Administrador", "admin", 1),
    ("tecnico@tech.pt", "trab123", "Técnico Demo", "tecnico", 1),
    ("maria@escola.pt", "user123", "Maria Utilizadora", "utilizador", 0),
]

SEED_PCS = [
    {
        "code": "PC-0001",
        "name": "Sala 12 – PC Professor",
        "location": "Sala 12",
        "type": "Desktop",
        "brand": "Dell",
        "model": "OptiPlex 7090",
        "cpu": "Intel i5-11500",
        "ram": "16 GB",
        "storage": "512 GB SSD",
        "os": "Windows 11 Pro",
        "serial": "DLL-7090-A1",
        "mac": "A4:BB:6D:12:34:56",
        "ip": "192.168.1.101",
        "acquisition_date": "2023-09-01",
        "status": "ativo",
        "notes": "PC principal da sala.",
    },
    {
        "code": "PC-0002",
        "name": "Laboratório A – Posto 3",
        "location": "Lab. Informática A",
        "type": "Desktop",
        "brand": "HP",
        "model": "ProDesk 400 G7",
        "cpu": "Intel i3-10100",
        "ram": "8 GB",
        "storage": "256 GB SSD",
        "os": "Windows 10 Education",
        "serial": "HP-400-G7-03",
        "mac": "B8:27:EB:AA:BB:CC",
        "ip": "192.168.1.115",
        "acquisition_date": "2022-03-15",
        "status": "manutencao",
        "notes": "Aguarda substituição de fonte.",
    },
    {
        "code": "PC-0003",
        "name": "Secretaria – Portátil",
        "location": "Secretaria",
        "type": "Portátil",
        "brand": "Lenovo",
        "model": "ThinkPad E14",
        "cpu": "AMD Ryzen 5 5500U",
        "ram": "16 GB",
        "storage": "512 GB SSD",
        "os": "Windows 11 Pro",
        "serial": "LNV-E14-SEC",
        "mac": "C0:3F:D5:11:22:33",
        "ip": "192.168.1.50",
        "acquisition_date": "2024-01-10",
        "status": "ativo",
        "notes": "",
    },
]


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_db()
    conn.executescript(SCHEMA)
    cur = conn.execute("SELECT COUNT(*) AS n FROM users")
    if cur.fetchone()["n"] == 0:
        for email, pwd, name, role, twofa in SEED_USERS:
            conn.execute(
                "INSERT INTO users (email, password, display_name, role, twofa_enabled) VALUES (?,?,?,?,?)",
                (email, pwd, name, role, twofa),
            )
        for pc in SEED_PCS:
            conn.execute(
                """INSERT INTO equipment
                   (code, name, location, type, brand, model, cpu, ram, storage, os,
                    serial, mac, ip, acquisition_date, status, notes)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    pc["code"], pc["name"], pc["location"], pc["type"], pc["brand"],
                    pc["model"], pc["cpu"], pc["ram"], pc["storage"], pc["os"],
                    pc["serial"], pc["mac"], pc["ip"], pc["acquisition_date"],
                    pc["status"], pc["notes"],
                ),
            )
        conn.execute(
            """INSERT INTO maintenances (equipment_id, date, type, description, technician)
               VALUES (2, '2026-09-20', 'corretiva', 'Fonte com ruído; pedido de substituição.', 'Técnico Demo')"""
        )
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES ('base_url', ?)",
            (f"http://localhost:{PORT}",),
        )
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES ('pdf_style', ?)",
            ("default",),
        )
        conn.commit()
        print("[DB] Dados de demonstração criados.")
    conn.close()


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)


class TechPCHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def log_message(self, fmt, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path.startswith("/api/"):
            self._handle_api_get(path, parse_qs(parsed.query))
            return
        if path == "/" or path == "/login":
            self.path = "/index.html"
        elif path.startswith("/dispositivo/"):
            self.path = "/pc-detail.html"
        elif path == "/dashboard":
            self.path = "/dashboard.html"
        elif path == "/admin":
            self.path = "/admin.html"
        elif path == "/scan":
            self.path = "/scan.html"
        elif path == "/settings":
            self.path = "/settings.html"
        elif path == "/register":
            self.path = "/register.html"
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            self._json({"error": "Not found"}, 404)
            return
        self._handle_api_post(parsed.path)

    def _handle_api_get(self, path, query):
        conn = get_db()
        try:
            if path == "/api/health":
                self._json({"ok": True, "version": "1.0-prototipo"})
                return
            if path == "/api/equipment":
                rows = conn.execute(
                    "SELECT * FROM equipment WHERE deleted = 0 ORDER BY code"
                ).fetchall()
                self._json([row_to_dict(r) for r in rows])
                return
            if path.startswith("/api/equipment/"):
                code_or_id = path.split("/")[-1]
                row = conn.execute(
                    "SELECT * FROM equipment WHERE (code = ? OR id = ?) AND deleted = 0",
                    (code_or_id, code_or_id),
                ).fetchone()
                if not row:
                    self._json({"error": "Equipamento não encontrado"}, 404)
                    return
                maint = conn.execute(
                    "SELECT * FROM maintenances WHERE equipment_id = ? ORDER BY date DESC",
                    (row["id"],),
                ).fetchall()
                data = row_to_dict(row)
                data["maintenances"] = [row_to_dict(m) for m in maint]
                self._json(data)
                return
            if path == "/api/settings":
                rows = conn.execute("SELECT key, value FROM settings").fetchall()
                self._json({r["key"]: r["value"] for r in rows})
                return
            if path == "/api/users":
                rows = conn.execute(
                    "SELECT id, email, display_name, role, twofa_enabled FROM users"
                ).fetchall()
                self._json([row_to_dict(r) for r in rows])
                return
            self._json({"error": "Endpoint não encontrado"}, 404)
        finally:
            conn.close()

    def _handle_api_post(self, path):
        data = self._read_json()
        conn = get_db()
        try:
            if path == "/api/login":
                email = (data.get("email") or "").strip().lower()
                password = data.get("password") or ""
                row = conn.execute(
                    "SELECT * FROM users WHERE email = ? AND password = ?",
                    (email, password),
                ).fetchone()
                if not row:
                    self._json({"error": "Credenciais inválidas"}, 401)
                    return
                token = secrets.token_hex(16)
                user = {
                    "id": row["id"],
                    "email": row["email"],
                    "display_name": row["display_name"],
                    "role": row["role"],
                    "twofa_enabled": bool(row["twofa_enabled"]),
                    "token": token,
                }
                if row["twofa_enabled"]:
                    code = f"{secrets.randbelow(1000000):06d}"
                    user["twofa_code"] = code
                    user["needs_2fa"] = True
                self._json(user)
                return
            if path == "/api/equipment":
                code = data.get("code") or self._next_code(conn)
                conn.execute(
                    """INSERT INTO equipment
                       (code, name, location, type, brand, model, cpu, ram, storage, os,
                        serial, mac, ip, acquisition_date, status, notes, photo)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        code, data.get("name", ""), data.get("location"), data.get("type"),
                        data.get("brand"), data.get("model"), data.get("cpu"), data.get("ram"),
                        data.get("storage"), data.get("os"), data.get("serial"), data.get("mac"),
                        data.get("ip"), data.get("acquisition_date"), data.get("status", "ativo"),
                        data.get("notes"), data.get("photo"),
                    ),
                )
                conn.commit()
                row = conn.execute("SELECT * FROM equipment WHERE code = ?", (code,)).fetchone()
                self._json(row_to_dict(row), 201)
                return
            if path == "/api/maintenance":
                conn.execute(
                    """INSERT INTO maintenances (equipment_id, date, type, description, technician)
                       VALUES (?,?,?,?,?)""",
                    (
                        data.get("equipment_id"),
                        data.get("date") or datetime.now().strftime("%Y-%m-%d"),
                        data.get("type", "corretiva"),
                        data.get("description"),
                        data.get("technician"),
                    ),
                )
                conn.commit()
                self._json({"ok": True}, 201)
                return
            self._json({"error": "Endpoint não encontrado"}, 404)
        except Exception as e:
            self._json({"error": str(e)}, 500)
        finally:
            conn.close()

    def _next_code(self, conn):
        row = conn.execute("SELECT code FROM equipment ORDER BY id DESC LIMIT 1").fetchone()
        if not row:
            return "PC-0001"
        try:
            num = int(row["code"].split("-")[-1]) + 1
        except ValueError:
            num = 1
        return f"PC-{num:04d}"


def main():
    parser = argparse.ArgumentParser(description="TechPCInfo protótipo")
    parser.add_argument("--https", action="store_true")
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()
    init_db()
    server = ThreadingHTTPServer(("0.0.0.0", args.port), TechPCHandler)
    if args.https:
        cert = BASE_DIR / "cert.pem"
        key = BASE_DIR / "key.pem"
        if cert.exists() and key.exists():
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ctx.load_cert_chain(cert, key)
            server.socket = ctx.wrap_socket(server.socket, server_side=True)
            print(f"HTTPS em https://0.0.0.0:{args.port}")
        else:
            print("Aviso: cert.pem/key.pem não encontrados – a correr em HTTP.")
    print(f"TechPCInfo protótipo → http://localhost:{args.port}")
    print("Contas demo: admin@admin.pt / admin123 | tecnico@tech.pt / trab123 | maria@escola.pt / user123")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor parado.")


if __name__ == "__main__":
    main()
