<!DOCTYPE HTML>
<head>
	<title>Library Management System</title>
</head>

<style>
body{
	font: 100%/30px 'verdana', 'helvetica', 'arial', 'sans-serif';
	text-align: center;
	font-weight: bold;
}

#header{
	color: blue;
	text-decoration: underline;
}

</style>

<body>
	<p id="header">Library Management System, IIT Delhi</p>
	<hr/>
	<form method="post" action="login_admin.php" target="_top" >
<?php

	session_start();
	
	if ($_POST['login']){

		$user = $_POST['user'];
		$pass = $_POST['pass'];

		$server = mysql_connect('localhost','root','');
		// $server = mysql_connect('mysql.hostinger.in','u642211610_admin','col362');

		if(!$server) die("Unable to connect to MySQL: " . mysql_error());	

		$res = mysql_select_db('u642211610_lib');
		
		if(mysql_error()){
				echo mysql_error();
		}

		$query = "SELECT * FROM admins WHERE ((username='$user') AND (password='$pass'))";
		$result = mysql_query($query);
		$num_rows = mysql_num_rows($result);		

		if ($num_rows){
			$_SESSION['username'] = $user;
			header("Location: ./admin.php");
			exit();
		} else {
			echo "Access Denied! Contact Database Administrator!";
		}
	} else{
	echo "
	<p>Enter Administrative Credentials to continue </p>
	<table style='margin:0 auto'>
		<tr>
			<td> Username </td>
			<td> <input name='user' type='text' /> </td>
		</tr>
		<tr>
			<td> Password </td>
			<td> <input name='pass' type='password' /> </td>
		</tr>
	</table>
	<input type='submit' name='login' value='Login To The System' />";
	}
?>
	</form>
</body>