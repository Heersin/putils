function get-netInterfaces {
    param ([Switch]$virtual, [Switch]$binding, [Switch]$all)
    if($binding)
    {
        if($virtual){
            echo "[x]Cannot Set Virtual For binding"
            exit(-1)
        }
        if($all){ Get-NetAdapterBinding -Name "*" -IncludeHidden}
        else{ Get-NetAdapterBinding -Name "*" }
    }
    else {
        if($virtual){
            if($all){ Get-NetAdapter -Name "*"  -IncludeHidden}
            else{ Get-NetAdapter -Name "*"}
        }
        else{
            if($all){ Get-NetAdapter -Name "*" -Physical -IncludeHidden }
            else{ Get-NetAdapter -Name "*" -Physical }
        }
    }
}

function  get-hardware{
    param ([Switch]$gui)
    if($gui){
        Get-WmiObject -Class CIM_LogicalDevice |
        Select-Object -Property __Class, Description |
        Sort-Object -Property __Class -Unique |
        Out-GridView
    }else{
        Get-WmiObject -Class CIM_LogicalDevice |
        Select-Object -Property __Class, Description |
        Sort-Object -Property __Class -Unique 
    }
}

function get-disk {
    param (
        [Switch]
        $physical)
    if($physical)
    {Get-PhysicalDisk}
    else {
            $DiskCount = ((Get-WmiObject -Class Win32_DiskDrive).Caption).count
            #获取磁盘分区大小
            $DiskInfo = Get-WmiObject -Class Win32_LogicalDisk 
            echo "-------------------------Disk Status-------------------------------"
            echo "    No.    Name    Partition Space    Free Space     FileSystem    "
            foreach ($Drivers in $DiskInfo) 
            {
                $PartitionID = $Drivers.DeviceID
                $PartitionSize = "{0:N2}GB" -f ($Drivers.Size/1GB)
                $PartitionFreeSize = "{0:N2}GB" -f ($Drivers.FreeSpace/1GB)
                $PartitionName = $Drivers.VolumeName
                $PartitionFS = $Drivers.FileSystem
                echo "    $PartitionID        $PartitionName    $PartitionSize        $PartitionFreeSize        $PartitionFS    "    
            }
        }
}


function get-usb {
    param ()
    $usb_path="HKLM:\SYSTEM\CurrentControlSet\Enum\USB\*\*"
    Get-ItemProperty -Path $usb_path | 
    Select-Object -Property FriendlyName, CompatibleIDs, Mfg
}

# ============== Wifi Issue =============================
function Convert-16bytestoTime($timebytes)
{
	$year=[BitConverter]::ToInt16($timebytes,0).ToString()
	$month=[BitConverter]::ToInt16($timebytes,2).ToString()
	$day=[BitConverter]::ToInt16($timebytes,6).ToString()
	$hour=[BitConverter]::ToInt16($timebytes,8).ToString()

	return $year+'/'+$month+'/'+$day+' Hour:'+ $hour
} 
function get-wifi {
    param ([Switch]$report, [Switch]$profile)
    if($report)
    {
        echo "Connected Wifi"
        netsh wlan show wlanreport
    }
    else {
        if($profile){netsh wlan show profile name="*" key=clear}
        else{
            $key_path = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles\"
            $count = 0
            foreach($ap in Get-ChildItem -Path $key_path)
            {
                echo "========== $count ============"
                echo $ap.GetValue("ProfileName")
                $time_bytes = $ap.GetValue("DateLastConnected")
                $time_str = Convert-16bytestoTime($time_bytes)
                echo $time_str
                $count += 1
            }
        }
    }
}
