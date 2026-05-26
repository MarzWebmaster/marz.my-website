<?php
/**
 * Marz Technology & Trading — Contact Form Handler
 * Security: Honeypot, rate limiting, input sanitization, MySQL + JSON log
 */

// Optional: load config if files exist
$config_paths = [
    '/etc/marztech-config/db.php',
    '/etc/marztech-config/security.php',
];
foreach ($config_paths as $p) {
    if (file_exists($p)) { require_once $p; }
}

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

// === RATE LIMITING: max 3 submissions per 10 minutes per IP ===
$rate_file = sys_get_temp_dir() . '/rate_' . md5($_SERVER['REMOTE_ADDR'] ?? 'unknown');
$rate_data = file_exists($rate_file) ? (json_decode(file_get_contents($rate_file), true) ?? []) : [];
// Remove entries older than 10 minutes
$rate_data = array_values(array_filter($rate_data, function($t) { return $t > (time() - 600); }));
if (count($rate_data) >= 3) {
    http_response_code(429);
    echo json_encode(['success' => false, 'message' => 'Too many submissions. Please try again later.']);
    exit;
}
$rate_data[] = time();
file_put_contents($rate_file, json_encode($rate_data), LOCK_EX);

// === INPUT SANITIZATION ===
$name    = strip_tags(trim($_POST['name'] ?? ''));
$email   = filter_var(trim($_POST['email'] ?? ''), FILTER_VALIDATE_EMAIL);
$phone   = strip_tags(trim($_POST['phone'] ?? ''));
$subject = strip_tags(trim($_POST['subject'] ?? ''));
$message = strip_tags(trim($_POST['message'] ?? ''));

if (!$name || !$email || !$subject || !$message) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Please fill in all required fields.']);
    exit;
}

// === HONEYPOT CHECK (if security.php loaded) ===
if (function_exists('security_validate')) {
    $sec_errors = security_validate();
    if (!empty($sec_errors)) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Invalid request.']);
        exit;
    }
}

// === HONEYPOT CHECK (standalone) ===
if (!empty($_POST['website'])) {
    // Bot filled hidden field — silently accept but don't save
    echo json_encode(['success' => true, 'message' => 'Thank you! Your message has been sent successfully.']);
    exit;
}

// === SAVE TO MYSQL (if DB config available) ===
if (defined('DB_HOST') && defined('DB_NAME') && defined('DB_USER') && defined('DB_PASS')) {
    try {
        $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . (defined('DB_CHARSET') ? DB_CHARSET : 'utf8mb4');
        $pdo = new PDO($dsn, DB_USER, DB_PASS, [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
        $stmt = $pdo->prepare("INSERT INTO contact_inquiries (inquiry_id, name, email, phone, subject, message, ip_address, user_agent, created_at, source_url) VALUES (UUID(), :name, :email, :phone, :subject, :message, :ip, :ua, NOW(), :source)");
        $stmt->execute([
            ':name'    => $name,
            ':email'   => $email,
            ':phone'   => $phone,
            ':subject' => $subject,
            ':message' => $message,
            ':ip'      => $_SERVER['REMOTE_ADDR'] ?? '',
            ':ua'      => $_SERVER['HTTP_USER_AGENT'] ?? '',
            ':source'  => 'https://marz.my/contact.html',
        ]);
    } catch (PDOException $e) {
        error_log("Marz.my contact form DB error: " . $e->getMessage());
    }
}

// === JSON LOG BACKUP ===
$log_dir = __DIR__ . '/submissions/';
if (!is_dir($log_dir)) { mkdir($log_dir, 0755, true); }
$entry = [
    'id'        => uniqid('msg_'),
    'timestamp' => date('Y-m-d H:i:s'),
    'name'      => $name,
    'email'     => $email,
    'phone'     => $phone,
    'subject'   => $subject,
    'message'   => $message,
    'ip'        => $_SERVER['REMOTE_ADDR'] ?? '',
];
$log_file = $log_dir . date('Y-m-d') . '.json';
$subs = file_exists($log_file) ? (json_decode(file_get_contents($log_file), true) ?? []) : [];
$subs[] = $entry;
file_put_contents($log_file, json_encode($subs, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);

// === EMAIL NOTIFICATION ===
$email_body = "New inquiry from marz.my contact form:\n\nName: $name\nEmail: $email\nPhone: $phone\nSubject: $subject\n\nMessage:\n$message";
@mail('sales@marz.my', "New Contact Form: $subject from $name", $email_body, "From: noreply@marz.my\r\nReply-To: $email");
@mail('marzcomputer@gmail.com', "New Contact Form: $subject from $name", $email_body, "From: noreply@marz.my\r\nReply-To: $email");

echo json_encode(['success' => true, 'message' => 'Thank you! Your message has been sent successfully.']);
