<!DOCTYPE html>
<html>
<head>
    <title>Historique candidature</title>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>

    <table data-sortable>
<thead>
    <tr>
    <th>Date</th>
    <th>Intitulé du poste</th>
    <th>Société</th>
    <th>Réponse</th>
    <th>Motif</th>
    </tr>
</thead>


<tbody>
<?php

//take last row first
$data = array_reverse(file("history.txt"));

foreach ($data as $element){
    echo "\n<tr><td>";
    $temp = explode(';', $element);
    $temp = implode('</td><td>', $temp);
    $temp = $temp."</td></tr>\n";

    echo $temp;
}
?>
</tbody>
    </table>

</body>

<script src="sort.js"></script>
</html>

