# Uses an existing process environment key, or the current Windows user's DPAPI file.
# Never writes the plaintext key to disk or the console. CLI still defaults to dry-run.
param(
    [string]$PythonPath = '',
    [string]$SecretFile = (Join-Path $env:USERPROFILE '.codex\secrets\tagproject-deepseek-api-key.dpapi'),
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$CliArguments
)
$ErrorActionPreference = 'Stop'
$tagPreviousKey = [Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY', 'Process')
$tagExitCode = 2
try {
    if (-not $tagPreviousKey) {
        if (Test-Path -LiteralPath $SecretFile -PathType Leaf) {
            $tagEncrypted = (Get-Content -LiteralPath $SecretFile -Raw -Encoding UTF8).Trim()
            $tagSecure = ConvertTo-SecureString -String $tagEncrypted
            $tagCredential = [System.Net.NetworkCredential]::new('', $tagSecure)
            [Environment]::SetEnvironmentVariable('DEEPSEEK_API_KEY', $tagCredential.Password, 'Process')
        }
    }
    if (-not $PythonPath) {
        $tagBundled = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
        if (Test-Path -LiteralPath $tagBundled -PathType Leaf) { $PythonPath = $tagBundled }
        else { $PythonPath = 'python' }
    }
    $tagEntry = Join-Path $PSScriptRoot 'deepseek_classify.py'
    & $PythonPath $tagEntry @CliArguments
    $tagExitCode = $LASTEXITCODE
}
catch {
    # Do not echo exception text: a secret or an HTTP body might be included.
    Write-Error 'DeepSeek launcher failed; check Python and current-user DPAPI access.' -ErrorAction Continue
}
finally {
    [Environment]::SetEnvironmentVariable('DEEPSEEK_API_KEY', $tagPreviousKey, 'Process')
    $tagCredential = $null
    $tagSecure = $null
    $tagEncrypted = $null
}
exit $tagExitCode
