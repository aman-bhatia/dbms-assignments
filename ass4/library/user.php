<!DOCTYPE HTML>
<head>
	<title>Library Management System</title>
	<link type="text/css" rel="stylesheet" href="css/stylesheet_user.css" />
	<link type="text/css" rel="stylesheet" href="jquery/css/ui-lightness/jquery-ui-1.10.4.custom.min.css" />
	<link href="js/fancybox/jquery.fancybox-1.3.4.css" rel="stylesheet" />

	<script src="js/jquery-1.7.2.min.js"></script>
	<script src="jquery/js/jquery-ui-1.10.4.custom.min.js" ></script>
	<script src="js/fancybox/jquery.fancybox-1.3.4.min.js"></script>
	<script>
		$(document).ready(function() {
			$('.iframe').fancybox({
				width : 850,
				height : 450
			});
			$("#dob").datepicker({
				changeMonth : true,
				changeYear : true
			});
		});
	</script>
</head>

<style>
footer {
	position: fixed;
	top:0;
	right:0;
	margin:10px;
}
</style>

<body>

	<br>
	<p id="header"> Library Management System , IIT Delhi </p>
	<div style="margin-top:130px;">
	
<?php
	session_start();
	$entry_no = substr($_SERVER['QUERY_STRING'],strpos($_SERVER['QUERY_STRING'],"=")+1);

	if (!($_SESSION['username'] == $entry_no)){
		header('Location: ./index.php');
	}

	$server = mysql_connect('localhost','root','');
	// $server = mysql_connect('mysql.hostinger.in','u642211610_admin','col362');

	if(!$server) die("Unable to connect to MySQL: " . mysql_error());	

	$res = mysql_select_db('u642211610_lib');
	
	if(mysql_error()){
			echo mysql_error();
	}
	
	$query = "SELECT * FROM students WHERE entry_no='$entry_no'";
	
	$result = mysql_query($query);
	if(mysql_error()){
		echo mysql_error();
	}
	
	$row=mysql_fetch_row($result);
	
	echo "
	<footer>
		<a href='./request.php?entry_no=$row[0]' class='iframe'> Contact Admin </a>
	</footer>
	
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
	
	
	echo "<p id='header'> Your Pending Transactions </p>";

	$query = "SELECT * FROM transactions WHERE entry_no='$entry_no'";
	$result = mysql_query($query);

	if(!$result){
		echo "<br />The server says : ".mysql_error();
	}

	$num_rows = mysql_num_rows($result);
	if ($num_rows){
		echo "	<table>
					<thead>
						<tr>
							<th> Book ISBN Code </th>
							<th> Date/time of Transaction </th>
						</tr>
					</thead>";
		while ($rows = mysql_fetch_row($result)){
			echo "<tr>
					<td> $rows[0] </td>
					<td> $rows[2] </td>
				</tr>";
		};
		echo "</table>";
	} else {
		echo "
		<br />
		<table>
			<tr>
				<td> No current enteries. </td>
			</tr>
		</table>
		<br/>
		<br/>";
	}
?>
</div>

</form>
</body>
</html>