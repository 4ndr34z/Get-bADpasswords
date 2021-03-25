# A really simple PoC-script to generate lists with bad/weak passwords
#
# Find us here:
# - https://www.improsec.com
# - https://github.com/improsec
# - https://twitter.com/improsec
# - https://www.facebook.com/improsec
#
# Add your custom wordlist in custom.txt and run this script to create passwords.

$years = (0..9 | foreach{ $_ }) + (00..99 | foreach { $_.ToString("00") }) + (1950..2021 | foreach { $_.ToString() }) + @("123", "1234", "12345")
$permutations = @("", ".", "!", "?", "=", ".!", "..", "!!", "!.", "?.", ".=")

$strings = @(Get-Content custom.txt)
# =========================
# PERFORM GENERATION
# =========================

$filename = "weak-passwords-customlist.txt"
$count = $null
$count = 1
foreach ($string in $strings) {
    $count = $count+1
    Add-Content $filename "$string"
    
    Add-Content $filename "$($string.ToLower())"
    Add-Content $filename "$($string.ToUpper())"
    
    foreach ($year in $years) {
        foreach ($permutation in $permutations) {
            Add-Content $filename "$string$year$permutation"
            Add-Content $filename "$($string.ToLower())$year$permutation"
            Add-Content $filename "$($string.ToUpper())$year$permutation"
        }
    }
    write-host "Working on line: $($count)"
}

