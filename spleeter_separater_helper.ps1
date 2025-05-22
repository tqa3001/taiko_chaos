param (
    [string]$track
)

$env:AUDIO_IN = ".\input"
$env:AUDIO_OUT = ".\output"
$env:MODEL_DIRECTORY = ".\spleeter_models"

# Make sure the directories exist (create if missing)
if (-not (Test-Path $env:AUDIO_IN)) { New-Item -ItemType Directory -Path $env:AUDIO_IN }
if (-not (Test-Path $env:AUDIO_OUT)) { New-Item -ItemType Directory -Path $env:AUDIO_OUT }
if (-not (Test-Path $env:MODEL_DIRECTORY)) { New-Item -ItemType Directory -Path $env:MODEL_DIRECTORY }

$inputFile = "/input/${track}"

if (Test-Path $env:AUDIO_IN) { Write-Host "Located ${inputFile}" }

# Run Docker command with volume mounts and environment variable for model path
docker run `
    -v "${env:AUDIO_IN}:/input" `
    -v "${env:AUDIO_OUT}:/output" `
    -v "${env:MODEL_DIRECTORY}:/model" `
    -e MODEL_PATH=/model `
    deezer/spleeter:3.6-5stems `
    separate $inputFile -p spleeter:5stems -o /output
