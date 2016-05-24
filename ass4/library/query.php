<!DOCTYPE HTML>

<html>

<style>

body{
	background-image: url(images/congruent_pentagon.png);
	font: 100%/30px 'verdana', 'helvetica', 'arial', 'sans-serif';
	text-shadow: 0 1px 0 #fff;
	font-style: italic;
	/*text-align: center;*/
}

#header{
	text-align: center;
	margin: 0 auto;
	margin-top: 50px;
	height: 80px;
	font-size: 3em;
	color: #4f899f;
	/*text-decoration: underline;*/
	/*letter-spacing: 5px;*/
	/*word-spacing: 15px;*/
}

table {
	/*background: #f5f5f5;*/
	line-height: 12px;
	margin: 30px auto;
	text-align: left;
	font-weight: bold;
	width: 500px;
}	
td {
	padding: 10px 15px;
	position: relative;
}

img{
	margin-right: 100px;
	float: right;
	width:160px;
	height:200px;
	border-radius: 10px;
}
</style>

<body>
<?php
	
	$server = mysql_connect('localhost','root','');
	// $server = mysql_connect('mysql.hostinger.in','u642211610_admin','col362');

	if(!$server) die("Unable to connect to MySQL: " . mysql_error());	

	mysql_select_db('u642211610_lib');

	if(mysql_error()){
		echo mysql_error();
	}
	
	$entry_no = substr($_SERVER['QUERY_STRING'],strpos($_SERVER['QUERY_STRING'],"=")+1);
	
	$query = "SELECT * FROM students WHERE entry_no='$entry_no'";
	
	$result = mysql_query($query);
	if(mysql_error()){
		echo mysql_error();
	}
	
	$row=mysql_fetch_row($result);
	
	echo "
	<p id=\"header\"> Student Information </p>
	
	<img src=\"$row[8]\" />
	
	<table>
		<tr>
			<td> Student Name </td>
			<td> $row[1] </td>
		</tr>
		<tr>
			<td> Entry No. </td>
			<td> $row[0] </td>
		</tr>
		<tr>
			<td> Gender </td>
			<td> $row[2] </td>
		</tr>
		<tr>
			<td> DOB </td>
			<td> $row[3] </td>
		</tr>
		<tr>
			<td> Degree </td>
			<td> $row[4] </td>
		</tr>
		<tr>
			<td> Membership Upto </td>
			<td> $row[5] </td>
		</tr>
		<tr>
			<td> Mobile No. </td>
			<td> $row[6] </td>
		</tr>
		<tr>
			<td> Email </td>
			<td> $row[7] </td>
		</tr>
	</table>";
	
	mysql_close($server);
	?>
</body>
</html>