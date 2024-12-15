<?php
// Include the database connection
require_once 'db.php';

// Allow Cross-Origin requests
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

// Check if the request is POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Decode JSON data sent by Svelte
    $input = json_decode(file_get_contents('php://input'), true);

    // Sanitize and validate inputs
    $username = filter_var($input['username'] ?? '', FILTER_SANITIZE_STRING);
    $email = filter_var($input['email'] ?? '', FILTER_SANITIZE_EMAIL);
    $password = $input['password'] ?? '';
    $role = filter_var($input['role'] ?? '', FILTER_SANITIZE_STRING);

    if (!$username || !$email || !$password || !$role) {
        echo json_encode(['status' => 'error', 'message' => 'All fields are required.']);
        exit;
    }

    try {
        // Check if email already exists
        $checkStmt = $pdo->prepare("SELECT user_id FROM user WHERE email = :email");
        $checkStmt->bindParam(':email', $email, PDO::PARAM_STR);
        $checkStmt->execute();

        if ($checkStmt->rowCount() > 0) {
            echo json_encode(['status' => 'error', 'message' => 'Email already exists.']);
            exit;
        }

        // Hash the password
        $hashedPassword = password_hash($password, PASSWORD_DEFAULT);

        // Insert new user into the database
        $stmt = $pdo->prepare("INSERT INTO user (username, email, password, role) VALUES (:username, :email, :password, :role)");
        $stmt->bindParam(':username', $username, PDO::PARAM_STR);
        $stmt->bindParam(':email', $email, PDO::PARAM_STR);
        $stmt->bindParam(':password', $hashedPassword, PDO::PARAM_STR);
        $stmt->bindParam(':role', $role, PDO::PARAM_STR);

        if ($stmt->execute()) {
            echo json_encode(['status' => 'success', 'message' => 'Signup successful!']);
        } else {
            echo json_encode(['status' => 'error', 'message' => 'Signup failed. Please try again.']);
        }
    } catch (PDOException $e) {
        echo json_encode(['status' => 'error', 'message' => 'Database error: ' . $e->getMessage()]);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Invalid request method.']);
}
?>
