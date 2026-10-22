<?php
/**
 * TechPCInfo – ligação SQLite e schema (versão PHP)
 */
class Database
{
    private static ?PDO $pdo = null;

    public static function path(): string
    {
        return dirname(__DIR__) . '/data/inventory.db';
    }

    public static function pdo(): PDO
    {
        if (self::$pdo === null) {
            $dir = dirname(self::path());
            if (!is_dir($dir)) {
                mkdir($dir, 0755, true);
            }
            self::$pdo = new PDO('sqlite:' . self::path(), null, null, [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            ]);
            self::$pdo->exec('PRAGMA foreign_keys = ON');
            self::initSchema(self::$pdo);
        }
        return self::$pdo;
    }

    private static function initSchema(PDO $db): void
    {
        $db->exec(<<<'SQL'
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    name TEXT NOT NULL,
    two_factor_enabled INTEGER NOT NULL DEFAULT 0,
    two_factor_code TEXT DEFAULT '',
    created_at TEXT NOT NULL,
    avatar TEXT DEFAULT '',
    display_name TEXT DEFAULT '',
    terms_accepted_at TEXT DEFAULT '',
    gender TEXT DEFAULT 'neutro'
);
CREATE TABLE IF NOT EXISTS pcs (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    localizacao TEXT NOT NULL,
    tipo TEXT, marca TEXT, modelo TEXT, processador TEXT, ram TEXT,
    armazenamento TEXT, so TEXT, numero_serie TEXT, mac TEXT, ip TEXT,
    data_aquisicao TEXT, estado TEXT, observacoes TEXT, imagem TEXT,
    ultima_alteracao TEXT, alterado_por TEXT, deleted_at TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS manutencoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pc_id TEXT NOT NULL, data TEXT, tipo TEXT, descricao TEXT, tecnico TEXT,
    FOREIGN KEY (pc_id) REFERENCES pcs(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL, acao TEXT NOT NULL, mensagem TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS wallpapers (
    id TEXT PRIMARY KEY, name TEXT NOT NULL, filename TEXT NOT NULL,
    created_by TEXT, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pending_2fa (
    user_id INTEGER PRIMARY KEY, code TEXT NOT NULL, expires_at INTEGER NOT NULL
);
SQL);
        $n = (int) $db->query('SELECT COUNT(*) FROM users')->fetchColumn();
        if ($n === 0) {
            $now = gmdate('c');
            $stmt = $db->prepare(
                'INSERT INTO users (username, email, password, role, name, display_name, two_factor_enabled, two_factor_code, created_at, avatar, terms_accepted_at, gender)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
            );
            $stmt->execute(['admin@admin.pt', 'admin@admin.pt', 'admin123', 'admin', 'Administrador Sistema', 'Administrador Sistema', 1, '', $now, '', $now, 'neutro']);
            $stmt->execute(['tecnico@tech.pt', 'tecnico@tech.pt', 'trab123', 'worker', 'João Técnico', 'João Técnico', 1, '', $now, '', $now, 'neutro']);
            $stmt->execute(['maria@escola.pt', 'maria@escola.pt', 'user123', 'user', 'Maria Utilizadora', 'Maria Utilizadora', 0, '', $now, '', $now, 'neutro']);
            self::addLog($db, 'seed', 'Utilizadores de demonstração criados (PHP)');
        }
    }

    public static function addLog(PDO $db, string $acao, string $mensagem): void
    {
        $stmt = $db->prepare('INSERT INTO logs (data, acao, mensagem) VALUES (?,?,?)');
        $stmt->execute([gmdate('c'), $acao, $mensagem]);
    }
}
