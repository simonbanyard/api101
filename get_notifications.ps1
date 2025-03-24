# Set the base URL and API paths
$baseUrl = "https://api.services.mimecast.com"
$authPath = "/oauth/token"
$rPath = "/api/account/get-dashboard-notifications"

# Retrieve credentials from environment variables
$clientId = $env:MIME_ID
$clientSecret = $env:MIME_SECRET

# Prepare the payload for the authentication request
$authPayload = "client_id=$clientId&client_secret=$clientSecret&grant_type=client_credentials"
$authHeaders = @{
    "Content-Type" = "application/x-www-form-urlencoded"
}

# Make the authentication request to get the bearer token
$authResponse = Invoke-RestMethod -Method 'POST' -Uri ($baseUrl + $authPath) -Headers $authHeaders -Body $authPayload
$bearerToken = $authResponse.access_token

# Create the headers for the main request
$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("Content-Type", "application/json")
$headers.Add("Authorization", "Bearer $bearerToken")

# # Make the request to retrieve dashboard notifications
$response = Invoke-RestMethod -Method 'POST' -Uri ($baseUrl + $rPath) -Headers $headers

# # Convert the response to JSON string with formatting and output it
$response | ConvertTo-Json -Depth 10 | Set-Content -Path dash_notifications_ps.json
