function Get-InstalledSoftwares
{
    #
    # Read registry key as product entity.
    #
    function ConvertTo-ProductEntity
    {
        param([Microsoft.Win32.RegistryKey]$RegKey)
        $product = '' | select Name,Publisher,Version
        $product.Name =  $_.GetValue("DisplayName")
        $product.Publisher = $_.GetValue("Publisher")
        $product.Version =  $_.GetValue("DisplayVersion")

        if( -not [string]::IsNullOrEmpty($product.Name)){
            $product
        }
    }

    $UninstallPaths = @(,
    # For local machine.
    'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
    # For current user.
    'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall')

    # For 32bit softwares that were installed on 64bit operating system.
    if([Environment]::Is64BitOperatingSystem) {
        $UninstallPaths += 'HKLM:SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
    }
    $UninstallPaths | foreach {
        Get-ChildItem $_ | foreach {
            ConvertTo-ProductEntity -RegKey $_
        }
    }
}

# Check if An app is installed
function IsAppExsits {
    param (
        [String]$appname
    )
    $result = Get-InstalledSoftwares | Where-Object {$_.Name -eq $appname}    
    
    if ($result -eq $null){
        echo " $appname is not installed "
    }
    else {
        echo " $appname installed "
    }
}


# check installed App and Uninstalled
function get-install{
    param ([Switch]$uninstall)
    $install_info_path="HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"
    $uninstall_info_path="HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    if($uninstall)
    {dir -Path $uninstall_info_path}
    else {dir -Path $install_info_path }
}

function get-recentfile {
    param ([String]$path, [String]$days)
    Get-ChildItem $path -file | 
    where {$_.CreationTime.Date -le (Get-Date).AddDays(-$days).Date -or $_.LastWriteTime.Date -le (Get-Date).AddDays(-$Nbdays).Date} 
}