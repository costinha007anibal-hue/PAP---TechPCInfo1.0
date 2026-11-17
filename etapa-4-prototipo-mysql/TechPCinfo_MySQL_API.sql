-- ============================================================
-- TechPCInfo — Schema MySQL COMPATÍVEL com o website (server.py)
-- Tabelas iguais às do SQLite da API: users, pcs, manutencoes, logs, wallpapers
-- Base: techpcinfo
--
-- mysql -u root -p < TechPCinfo_MySQL_API.sql
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS techpcinfo
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE techpcinfo;

DROP TABLE IF EXISTS manutencoes;
DROP TABLE IF EXISTS wallpapers;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS pcs;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(120) NOT NULL UNIQUE,
    email VARCHAR(180) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    name VARCHAR(160) NOT NULL,
    two_factor_enabled TINYINT(1) NOT NULL DEFAULT 0,
    two_factor_code VARCHAR(12) DEFAULT '',
    created_at VARCHAR(40) NOT NULL,
    avatar VARCHAR(255) DEFAULT '',
    display_name VARCHAR(160) DEFAULT '',
    terms_accepted_at VARCHAR(40) DEFAULT '',
    gender VARCHAR(20) DEFAULT 'neutro'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE pcs (
    id VARCHAR(40) PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    localizacao VARCHAR(200) NOT NULL,
    tipo VARCHAR(80) DEFAULT NULL,
    marca VARCHAR(80) DEFAULT NULL,
    modelo VARCHAR(120) DEFAULT NULL,
    processador VARCHAR(120) DEFAULT NULL,
    ram VARCHAR(60) DEFAULT NULL,
    armazenamento VARCHAR(80) DEFAULT NULL,
    so VARCHAR(80) DEFAULT NULL,
    numero_serie VARCHAR(80) DEFAULT NULL,
    mac VARCHAR(40) DEFAULT NULL,
    ip VARCHAR(40) DEFAULT NULL,
    data_aquisicao VARCHAR(40) DEFAULT NULL,
    estado VARCHAR(40) DEFAULT 'Operacional',
    observacoes TEXT,
    imagem TEXT,
    ultima_alteracao VARCHAR(40) DEFAULT NULL,
    alterado_por VARCHAR(120) DEFAULT NULL,
    deleted_at VARCHAR(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE manutencoes (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    pc_id VARCHAR(40) NOT NULL,
    data VARCHAR(40) DEFAULT NULL,
    tipo VARCHAR(40) DEFAULT NULL,
    descricao TEXT,
    tecnico VARCHAR(120) DEFAULT NULL,
    CONSTRAINT fk_man_pc FOREIGN KEY (pc_id) REFERENCES pcs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE logs (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    data VARCHAR(40) NOT NULL,
    acao VARCHAR(80) NOT NULL,
    mensagem TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE wallpapers (
    id VARCHAR(80) PRIMARY KEY,
    name VARCHAR(160) NOT NULL,
    filename TEXT NOT NULL,
    created_by VARCHAR(120) DEFAULT NULL,
    created_at VARCHAR(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_pcs_estado ON pcs(estado);
CREATE INDEX idx_pcs_localizacao ON pcs(localizacao);
CREATE INDEX idx_manutencoes_pc ON manutencoes(pc_id);
CREATE INDEX idx_users_email ON users(email);

SET FOREIGN_KEY_CHECKS = 1;

-- Seed
INSERT INTO users (username, email, password, role, name, two_factor_enabled, two_factor_code, created_at) VALUES
('admin@admin.pt', 'admin@admin.pt', 'admin123', 'admin', 'Administrador Sistema', 1, '123456', DATE_FORMAT(UTC_TIMESTAMP(), '%Y-%m-%dT%H:%i:%sZ')),
('tecnico@tech.pt', 'tecnico@tech.pt', 'trab123', 'worker', 'João Técnico', 1, '654321', DATE_FORMAT(UTC_TIMESTAMP(), '%Y-%m-%dT%H:%i:%sZ')),
('maria@escola.pt', 'maria@escola.pt', 'user123', 'user', 'Maria Utilizadora', 0, '', DATE_FORMAT(UTC_TIMESTAMP(), '%Y-%m-%dT%H:%i:%sZ')),
('costinha007anibal@gmail.com', 'costinha007anibal@gmail.com', 'admin', 'admin', 'Martim Aníbal', 1, '123456', DATE_FORMAT(UTC_TIMESTAMP(), '%Y-%m-%dT%H:%i:%sZ'));
