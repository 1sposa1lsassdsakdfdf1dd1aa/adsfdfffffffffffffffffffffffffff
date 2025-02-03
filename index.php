<?php

// Extract the channel ID from the URL path
if (isset($_SERVER['PATH_INFO'])) {
    $pathInfo = trim($_SERVER['PATH_INFO'], '/'); // Remove leading and trailing slashes
    $pathParts = explode('.', $pathInfo); // Split by the period to separate "channel" and "m3u8"

    // Validate and extract the channel ID
    if (count($pathParts) === 2 && $pathParts[1] === 'm3u8') {
        $base_id = $pathParts[0]; // The first part is the channel ID
    } else {
        echo "Invalid URL format. Use /channel.m3u8.";
        exit;
    }
} else {
    echo "No channel specified. Use /channel.m3u8.";
    exit;
}

// Construct the play URL with the stream ID
$play_url = "https://secureplayer.sportstvn.com/token.php?stream=" . $base_id;

// Initialize cURL to fetch the token from the URL
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $play_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Referer: https://sportstvn.com/" // Hardcoded Referer header
]);

$response = curl_exec($ch);

// Check if cURL request was successful
if (curl_errno($ch)) {
    echo 'cURL Error: ' . curl_error($ch);
    exit;
}

// Close the cURL session
curl_close($ch);

// Extract the token from the response using regex
if (preg_match('/token=([a-f0-9\-]+)/', $response, $matches)) {
    $token = $matches[1]; // Extract token

    // Construct the M3U8 URL with the token
    $m3uUrl = "https://cdn.sturls.com/" . $base_id . "/index.m3u8?token=" . urlencode($token);

    // Redirect the user to the M3U8 URL
    header("Location: $m3uUrl");
    exit;
} else {
    echo "Token not found in the response.";
    exit;
}
?>
