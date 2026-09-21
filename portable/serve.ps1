param([switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
$practiceRoot = $PSScriptRoot
$practiceHtml = Join-Path $practiceRoot 'index.html'
if (-not (Test-Path -LiteralPath $practiceHtml)) { throw 'Extract the ZIP first. index.html must be next to this script.' }
$practiceBytes = [System.IO.File]::ReadAllBytes($practiceHtml)
$practicePort = 8766
$practiceUrl = "http://127.0.0.1:$practicePort/"
$practiceListener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $practicePort)
try { $practiceListener.Start() } catch { Write-Host 'Port 8766 is already in use. Close the other practice window and try again.'; Read-Host 'Press Enter to close'; exit 1 }
$practiceChromePaths = @(
    (Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe'),
    (Join-Path ${env:ProgramFiles(x86)} 'Google\Chrome\Application\chrome.exe'),
    (Join-Path $env:LOCALAPPDATA 'Google\Chrome\Application\chrome.exe')
)
$practiceChrome = $practiceChromePaths | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $NoBrowser) {
    if ($practiceChrome) { Start-Process -FilePath $practiceChrome -ArgumentList $practiceUrl }
    else { Start-Process $practiceUrl; Write-Host 'Please open this address in Google Chrome for speech recognition.' }
}
Write-Host "OPIc practice: $practiceUrl"
Write-Host 'Keep this window open during the exam. Close it when finished.'
Write-Host 'No answer audio files are recorded. Transcripts stay in the browser until exported.'
try {
    while ($true) {
        $practiceClient = $practiceListener.AcceptTcpClient()
        try {
            $practiceClient.ReceiveTimeout = 5000
            $practiceClient.SendTimeout = 15000
            $practiceStream = $practiceClient.GetStream()
            $practiceReader = [System.IO.StreamReader]::new($practiceStream, [System.Text.Encoding]::ASCII, $false, 1024, $true)
            $practiceRequest = $practiceReader.ReadLine()
            $practiceHeaderBytes = 0
            while ($practiceLine = $practiceReader.ReadLine()) {
                $practiceHeaderBytes += $practiceLine.Length
                if ($practiceHeaderBytes -gt 16384) { throw 'Request too large.' }
            }
            if ($practiceRequest -match '^GET /(index\.html)?(\?[^ ]*)? HTTP/1\.[01]$') {
                $practiceBody = $practiceBytes
                $practiceStatus = '200 OK'
                $practiceContentType = 'text/html; charset=utf-8'
            } else {
                $practiceBody = [System.Text.Encoding]::UTF8.GetBytes('Not found')
                $practiceStatus = '404 Not Found'
                $practiceContentType = 'text/plain; charset=utf-8'
            }
            $practiceHeader = [System.Text.Encoding]::ASCII.GetBytes("HTTP/1.1 $practiceStatus`r`nContent-Type: $practiceContentType`r`nContent-Length: $($practiceBody.Length)`r`nCache-Control: no-store`r`nX-Content-Type-Options: nosniff`r`nConnection: close`r`n`r`n")
            $practiceStream.Write($practiceHeader, 0, $practiceHeader.Length)
            $practiceStream.Write($practiceBody, 0, $practiceBody.Length)
            $practiceStream.Flush()
        } catch { Write-Host 'A browser connection closed. You can refresh the page.' }
        finally { $practiceClient.Dispose() }
    }
} finally { $practiceListener.Stop() }
