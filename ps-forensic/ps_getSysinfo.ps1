function get-SystemInfo
{
    param([String]$ComputerName = $env:COMPUTERNAME)
    $header = 'Hostname','OSName','OSVersion','OSManufacturer','OSConfiguration','OS Build Type','RegisteredOwner','RegisteredOrganization','Product ID','Original Install Date','System Boot Time','System Manufacturer','System Model','System Type','Processor(s)','BIOS Version','Windows Directory','System Directory','Boot Device','System Locale','Input Locale','Time Zone','Total Physical Memory','Available Physical Memory','Virtual Memory: Max Size','Virtual Memory: Available','Virtual Memory: In Use','Page File Location(s)','Domain','Logon Server','Hotfix(s)','Network Card(s)'
    systeminfo.exe /FO CSV /S $ComputerName | Select-Object -Skip 1 |
    ConvertFrom-CSV -Header $header
}

function get-UserList {
    param ([Switch]$verbose)
    if($verbose){
        Get-WmiObject -Class Win32_UserAccount
    }
    else {
        Get-WmiObject -Class Win32_UserAccount | Select-Object Name
    }
}


function get-Env {
    Get-ChildItem env:
}

