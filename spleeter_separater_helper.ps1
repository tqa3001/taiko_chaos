$env:AUDIO_IN = ".\example"
$env:AUDIO_OUT = ".\output"
$env:MODEL_DIRECTORY = ".\spleeter_models"

# Make sure the directories exist (create if missing)
if (-not (Test-Path $env:AUDIO_IN)) { New-Item -ItemType Directory -Path $env:AUDIO_IN }
if (-not (Test-Path $env:AUDIO_OUT)) { New-Item -ItemType Directory -Path $env:AUDIO_OUT }
if (-not (Test-Path $env:MODEL_DIRECTORY)) { New-Item -ItemType Directory -Path $env:MODEL_DIRECTORY }

# Join audio file names with space for multiple files
$audioFiles = "vocaloid.mp3" # ,"audio_2.mp3"
$inputFiles = $audioFiles | ForEach-Object { "/input/$($_)" } | Out-String
$inputFiles = $inputFiles -replace "\s+", ""  # clean up spaces

# Run Docker command with volume mounts and environment variable for model path
docker run `
    -v "${env:AUDIO_IN}:/input" `
    -v "${env:AUDIO_OUT}:/output" `
    -v "${env:MODEL_DIRECTORY}:/model" `
    -e MODEL_PATH=/model `
    deezer/spleeter:3.6-5stems `
    separate $inputFiles -p spleeter:5stems -o /output
