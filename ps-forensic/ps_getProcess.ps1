function get-autoservice {
    gsv | Where-Object {$_.StartType -eq 'Automatic' -and -not $_.CanStop}    
}

function get-dll {
    param (
        $appname
    )
    Tasklist.exe /M /fi “IMAGENAME eq $appname”
}
