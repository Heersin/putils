function Get-ComputerUptimeHistory {
    $q='
   <QueryList>
     <Query Id="0" Path="System">
       <Select Path="System">*[System[(EventID=6005 or EventID=6006)]]</Select>
     </Query>
   </QueryList>'
   $events = Get-WinEvent -FilterXml $q
   $i=-1
   while ( $i+1 -lt $events.length ) {
    if($i -eq -1)
    {
     [PSCustomObject]@{
     StartTime = $events[0].TimeCreated;
     StopTime = $null ;
     UpTime = [datetime]::Now - $events[0].TimeCreated
     }
    }
    else{
    [PSCustomObject]@{
     StartTime = $events[$i+1].TimeCreated;
     StopTime = $events[$i].TimeCreated ;
     UpTime = $events[$i].TimeCreated - $events[$i+1].TimeCreated
     }
    }
    $i += 2
   }
    
}

function get-powerHistory {
    param ([Switch]$detail)
    if($detail)
    {Get-ComputerUptimeHistory}
    else
    {Get-ComputerUptimeHistory |  Select-Object -First 2 | ft -AutoSize} 
}
