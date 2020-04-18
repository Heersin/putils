function get-forensic-help {
    param ($script_name)
    if($script_name -eq "ps_getDev")
    {
        echo "Cmd Set -- getDev"
        echo "[1]get-netInterfaces [--virtual] [--bingding] [--all]"
        echo "   --virtual : virtual Cards"
        echo "   --binding : show the binding relationship"
        echo "   --all : show the hidden network adapter"
        echo "[2]get-hardware [--gui] => display in GUI?"
        echo "[3]get-disk [--physical] => default display logical disk, set to display physical disk"
        echo "[4]get-usb => usb records, //TODO"
        echo "[5]get-wifi [--report] [--profile]"
        echo "    --report : Generate Wlan Report"
        echo "    --profile : check wifi profile rather than history"
        return
    }
    if($script_name -eq "ps_getFile")
    {
        echo "Cmd Set -- getFile "
        echo "[1]IsAppExsits --appname name"
        echo "[2]get-install [--uninstall] => show uninstalled only"
        echo "[3]get-recentfile --path [path] --days [ndays]"
        echo "     --path : The Folder To check"
        echo "     --days : recent n days"
        return
    }
    if($script_name -eq "ps_getPower")
    {
        echo "CMd Set -- getPower"
        echo "[1]get-powerHistory [--detail] => Set to show all history, default show last only"
        return
    }
    if($script_name -eq "ps_getProcess")
    {
        echo "Cmd Set -- ps_getProcess"
        echo "[1]get-autoservice => List Process with autostart option and cannot stop"
        echo "[2]get-dll --appname [name] => list application's dll"
        return
    }
    if($script_name -eq "ps_getSysinfo")
    {
        echo "Cmd Set -- get-Sysinfo"
        echo "[1]get-SystemInfo [--ComputerName [name]] => show info"
        echo "[2]get-UserList [--verbose] => show detail"
        echo "[3]get-Env => show environment"
        return
    }

    echo "No Command"
}

# ========== Test ===================
$inited = Test-Path .\venv
$inited = 1
# ==========Python env init===========
if ($inited) {
    echo "[*]Inited -- Skip Virtual environment"
}
else {
    mkdir .\venv
    virtualenv.exe venv
    pip install -r requirements.txt
}

# ==========Help Info=================
echo "Forensic Tools, This Suite support following functions"
echo "[1] ps_getDev -- Info about your device"
echo "    Support => General Hardware/wifi/usb/network Adapter/disk"
echo "    CmdSet => get-hardware/get-usb/get-wifi/get-disk/get-netInterfaces"
echo ""
echo "[2] ps_getPower -- Info about power on and off records"
echo "    Support => Power's history"
echo "    CmdSet => get-powerHistory"
echo ""
echo "[3] ps_getProcess -- Info about process"
echo "    Support => auto start service/process dll"
echo "    CmdSet => get-autoservice/get-dll"
echo ""
echo "[4] ps_getFile -- Info about File"
echo "    Support => Installed/Uninstalled Application/Application exist/recent-file"
echo "    CmdSet => IsAppExsits/get-install/get-recentfile"
echo ""
echo "[5] ps_getSysinfo -- Info about this system"
echo "    Support => user list/environment/General system info"
echo "    CmdSet => get-SystemInfo/get-UserList/get-Env"
echo ""
echo "[6] py_exif -- exif tool"
echo ""
echo "[7] py_explorer -- extract explorer info"
echo "    Support => password / history / download / keyword "
echo ""
echo "[8] py_hash -- python tool for hashing "
echo "    Support => csv output / md5/sha1/sha256"
echo ""
echo "[9] py_search -- python tool for searching string in A file"
echo "    Support => keyword_list / Similar Word Match"
echo "================================== Examples ============================================"
echo "[!] How To Use this tool ?"
echo "[!] Example : If I want to use ps_getPower CmdSet"
echo "      powershell>>  . .\ps_getPower.ps1"
echo "      powershell>>  get-powerHistory"
echo "      Follow the help instruction of these scripts or type this command for more information"
echo "      powershell>> get-forensic-help [script_name]"
echo "[!] How To Use Python script ?"
echo "[!] Example : Extract Exif "
echo "      powershell>> .\venv\Scripts\activate"
echo "      powershell>> python py_exif [filename]"
echo "      help with -h option~"