# Get-bADpasswords
[![License](https://img.shields.io/badge/License-BSD%203--Clause-orange.svg)](https://opensource.org/licenses/BSD-3-Clause) ![PowerShell 3 | 4 | 5](https://img.shields.io/badge/PowerShell-3%20|%204%20|%205-0000FF.svg) ![Windows Server 2008 R2 | 2012 R2 | 2016 | 2019](https://img.shields.io/badge/Windows%20Server-2008%20R2%20|%202012%20R2%20|%202016-007bb8.svg) ![.NET Framework 4.5.1+](https://img.shields.io/badge/.NET%20Framework-4.5.1%2B-007FFF.svg) ![Visual Studio 2017](https://img.shields.io/badge/Visual%20Studio-2017-383278.svg)

Get insights into the actual strength and quality of passwords in Active Directory. 

## Introduction
This module is able to compare password hashes of enabled Active Directory users against bad/weak/non-compliant passwords (e.g. hackers first guess in brute-force attacks).
* Performs comparison against one or multiple wordlist(s).
  * This script does not transform input from the wordlists (such as transforming between upper/lower case). Each input from the wordlist is used as-is. Use other tools to generate more specialized wordlists if necessary. A PoC-script has been included (New-bADpasswordLists_EN.ps1) for basic wordlist generation.
* Performs additional comparison against publicly leaked passwords, see acknowledgements below.
* Performs password comparison against 'null' in the Active Directory (i.e. finds empty/null passwords).
* Performs password comparison between users in the Active Directory (i.e. finds shared passwords).
* Requires 'Domain Admin' privileges or similar, e.g. 'Domain Controller' or delegated Domain-level permissions for both	"Replicating Directory Changes" and "Replicating Directory Changes All", to succesfully fetch passwords from the Active Directory database.
* Choose a Domain Controller or a member server (will become a Tier 0 system) for executing the script, e.g. as a Scheduled Task.

## Additions in this fork
The following additions are done in this fork
* Added optional actions for when weak passwords are detected, so you can mitigate the problem right away
  * Reset password - Resets the users password to a random strong password
  * Untick "Password never expires" in user properties
  * Ticks "User must change password at next logon"
* Added extended SMTP functions
  * Authentication 
  * SMTP portnumber
  * Enable SSL
  * SMTP credentials are stored encrypted
* Added a Norwegian wordlist
* Python-script for converting HIBP-hashes to binary

![picture](https://github.com/4ndr34z/Get-bADpasswords/blob/master/Image.png)

## Dependencies

### Microsoft Visual C++ Redistributable Package
Microsoft Visual C++ Redistributable Package is required by our PSI DLL. This DLL is reponsible for parsing the leaked-password binary file and performing comparisons against it. The source code for the DLL can be found [here](./Source).

##### Installation step-by-step
* Go to [Microsoft Latest Supported Visual C++ Download](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads).
* Download and install the Visual Studio 2017 version of the Visual C++ Redistributable Package for your target platform:
  * For 32-bit systems: vc_redist.x86.exe
  * For 64-bit systems: vc_redist.x64.exe (recommended)
* No restart required.

### Microsoft .NET Framework 4.5.1+
Microsoft .NET Framework 4.5.1+ is required by the DSInternals 3.0 PowerShell module by Michael Grafnetter.

##### Installation step-by-step
* Go to [Microsoft .NET Framework 4.5 Download](https://www.microsoft.com/en-us/download/details.aspx?id=30653).
* Download and install the .NET Framework 4.5 in your preferred language.
* Might require a restart.

## Prerequisites

### Active Directory module: RSAT-AD-PowerShell
This module is needed to set user options in AD. 
"Password must be changed at next login" and unticking of "Password never expires"

```
Import-Module ServerManager
Add-WindowsFeature -Name "RSAT-AD-PowerShell" –IncludeAllSubFeature
```


### DSInternals 3.0 PowerShell Module
This module is used to query the Active Directory and fetch user information (SAM Account Name, E-mail, Password Hash, etc.). The source code for this module can be found [here](https://github.com/MichaelGrafnetter/DSInternals).



##### Installation step-by-step
* Go to [DSInternals 3.0 PowerShell Module Download](https://www.powershellgallery.com/packages/DSInternals/3.0).
* Download and install the DSInternals 3.0 PowerShell Module.
* No restart required.

Alternatively, you can install DSInternals 3.0 through PowerShellGet by running the following PowerShell command:
```powershell
PS> Install-Module -Name DSInternals -Scope AllUsers
```


### Leaked password list
Must be collected from Have I Been Pwned

##### Installation step-by-step
* Download using [haveibeenpwned-downloader](https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader) (remember -n for NTLM-hashes)
  * ```haveibeenpwned-downloader pwnedpasswords -o -p 64 -n ```
* Convert the downloaded file using the script convert.py
  * ```python3 convert.py to-bin pwnedpasswords.txt pwnedntlm.bin```
* Place the file in the `./Accessible/PasswordLists/` folder.

## Installation
Installing this framework is as simple as downloading the entire respository. However, you have to manually configure the following:
* Open 'Get-bADpasswords.ps1':
  * Navigate to the configuration-section and modify the variables to fit your needs, at least:
     * $domain_name
     * $naming_context
     * $mail_smtp
     * $mail_recipient
* (Optional) Modify the wordlists at `./Accessible/PasswordLists/*.txt` to your own liking.

## Usage
Since the desired options has already been selected during the configuration part of the install-section, you can go ahead and run the script:
```powershell
PS> ./Get-bADpassword.ps1
```

## Authors

* [**Jakob H. Heidelberg**](https://github.com/ZilentJack) - *Initial work* - 
* [**Valdemar Carøe**](https://github.com/st4ckh0und) - *Script improvement & PSI-module development* - 
* **Nichlas Falk** - *Script improvement* - 
* **Andreas Finstad** - Improved SMTP-support, added useraccount actions, added Python convert-script


## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Michael Grafnetter](https://github.com/MichaelGrafnetter) for the amazing [DSInternals](https://github.com/MichaelGrafnetter/DSInternals) framework
* [Troy Hunt](https://github.com/troyhunt) for the amazing [PwnedPasswords](https://haveibeenpwned.com/Passwords) list
