<?php
function json_out(int $status, $data): void {
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Authorization');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}
function read_json_body(): array {
    $raw = file_get_contents('php://input');
    if ($raw === false || $raw === '') return [];
    $data = json_decode($raw, true);
    return is_array($data) ? $data : [];
}
function role_from_email(string $email): string {
    $email = strtolower($email);
    if (str_ends_with($email, '@admin.pt') || $email === 'admin@admin.pt') return 'admin';
    if (str_ends_with($email, '@tech.pt') || str_ends_with($email, '@trab.pt')) return 'worker';
    return 'user';
}
function row_user(array $r): array {
    return [
        'id' => (int) $r['id'], 'username' => $r['username'], 'email' => $r['email'],
        'role' => $r['role'], 'name' => $r['name'],
        'displayName' => ($r['display_name'] ?? '') !== '' ? $r['display_name'] : $r['name'],
        'avatar' => $r['avatar'] ?? '',
        'twoFactorEnabled' => !empty($r['two_factor_enabled']),
        'twoFactorCode' => $r['two_factor_code'] ?? '',
    ];
}
function pc_from_row(array $r, array $manutencoes = []): array {
    return [
        'id' => $r['id'], 'nome' => $r['nome'], 'localizacao' => $r['localizacao'],
        'tipo' => $r['tipo'] ?? '', 'marca' => $r['marca'] ?? '', 'modelo' => $r['modelo'] ?? '',
        'processador' => $r['processador'] ?? '', 'ram' => $r['ram'] ?? '',
        'armazenamento' => $r['armazenamento'] ?? '', 'so' => $r['so'] ?? '',
        'numeroSerie' => $r['numero_serie'] ?? '', 'mac' => $r['mac'] ?? '', 'ip' => $r['ip'] ?? '',
        'dataAquisicao' => $r['data_aquisicao'] ?? '', 'estado' => $r['estado'] ?? '',
        'observacoes' => $r['observacoes'] ?? '', 'imagem' => $r['imagem'] ?? '',
        'ultimaAlteracao' => $r['ultima_alteracao'] ?? '', 'alteradoPor' => $r['alterado_por'] ?? '',
        'manutencoes' => $manutencoes, 'deletedAt' => $r['deleted_at'] ?? '',
    ];
}
function next_pc_id(PDO $db): string {
    $row = $db->query("SELECT id FROM pcs ORDER BY id DESC LIMIT 1")->fetch();
    if (!$row) return 'PC-0001';
    if (preg_match('/(\d+)\s*$/', $row['id'], $m)) {
        return 'PC-' . str_pad((string) ((int) $m[1] + 1), 4, '0', STR_PAD_LEFT);
    }
    return 'PC-0001';
}
function save_data_image(string $dataUrl, string $destDir, string $prefix): string {
    if (!preg_match('#^data:image/(png|jpe?g|webp|gif);base64,#i', $dataUrl, $m)) return '';
    $ext = strtolower($m[1]) === 'jpeg' ? 'jpg' : strtolower($m[1]);
    $bin = base64_decode(preg_replace('#^data:image/\w+;base64,#i', '', $dataUrl), true);
    if ($bin === false) return '';
    if (!is_dir($destDir)) mkdir($destDir, 0755, true);
    $name = $prefix . '_' . bin2hex(random_bytes(4)) . '.' . $ext;
    $path = rtrim($destDir, '/') . '/' . $name;
    file_put_contents($path, $bin);
    $root = dirname(__DIR__);
    return ltrim(str_replace('\\', '/', substr($path, strlen($root))), '/');
}
function issue_2fa(PDO $db, int $userId): string {
    $code = str_pad((string) random_int(0, 999999), 6, '0', STR_PAD_LEFT);
    $stmt = $db->prepare('INSERT OR REPLACE INTO pending_2fa (user_id, code, expires_at) VALUES (?,?,?)');
    $stmt->execute([$userId, $code, time() + 600]);
    return $code;
}
function verify_2fa(PDO $db, int $userId, string $code): bool {
    $stmt = $db->prepare('SELECT code, expires_at FROM pending_2fa WHERE user_id = ?');
    $stmt->execute([$userId]);
    $row = $stmt->fetch();
    if (!$row || (int) $row['expires_at'] < time() || $row['code'] !== $code) return false;
    $db->prepare('DELETE FROM pending_2fa WHERE user_id = ?')->execute([$userId]);
    return true;
}
function get_pc_full(PDO $db, string $id): ?array {
    $stmt = $db->prepare("SELECT * FROM pcs WHERE id = ? AND IFNULL(deleted_at,'') = ''");
    $stmt->execute([$id]);
    $r = $stmt->fetch();
    if (!$r) return null;
    $ms = $db->prepare('SELECT id, data, tipo, descricao, tecnico FROM manutencoes WHERE pc_id = ? ORDER BY id DESC');
    $ms->execute([$id]);
    $lista = [];
    foreach ($ms->fetchAll() as $m) {
        $lista[] = ['id' => (int) $m['id'], 'data' => $m['data'], 'tipo' => $m['tipo'], 'descricao' => $m['descricao'], 'tecnico' => $m['tecnico']];
    }
    return pc_from_row($r, $lista);
}
