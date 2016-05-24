<!DOCTYPE HTML>

<html>

<style>

@font-face {
  font-family: 'Open Sans';
  font-style: normal;
  font-weight: 100;
  src: local('Open Sans'), local('OpenSans'), url('http://themes.googleusercontent.com/static/fonts/opensans/v5/cJZKeOuBrn4kERxqtaUH3T8E0i7KZn-EPnyo3HZu7kw.woff') format('woff');
}

body{
	background: linear-gradient(to right, #75745D , #04121F);
	font-family: 'open sans',arial,sans-serif;
	text-align: center;
	color:white;
}

#header{
	margin: 0 auto;
	margin-top: 50px;
	font-size: 32px;
}

textarea{
	border: 1px solid #aaa;
	box-shadow: 1px 1px 0 #DDDDDD;
	display: block;
	/*font-family: 'Marck Script',cursive;*/
	color: #555;
	font-family: 'open sans',arial,sans-serif;
	font-size: 20px;
	line-height: 30px;
	margin: 2% auto;
	padding: 6px;
	resize: none;
	
	background-image: -moz-linear-gradient(top , transparent, transparent 29px,#E7EFF8 0px);
	background-image: -webkit-linear-gradient(top , transparent, transparent 29px,#E7EFF8 0);
	
	-webkit-background-size:  100% 30px;
	background-size: 100% 30px;

}

.button{
	font-family: 'open sans',arial,sans-serif;
	height: 50px;
	min-width: 120px;
	font-size: 18px;
	color:white ;
	background: transparent;
	border: 1px solid white;
	border-radius: 5px;

	-webkit-transition: all 0.2s; 
	   -moz-transition: all 0.2s; 
		-ms-transition: all 0.2s; 
		 -o-transition: all 0.2s; 
			transition: all 0.2s;
}

.button:hover{
	color:black;
	background-color: white;
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
	
	if ($_POST['send']){
		echo "<p id=\"header\"> 
			Your Concern is mailed to admin.
			<br/>
			<br/>
			You will be contacted soon! 
			<br/>
			<br/>
			:)
			</p>";

			$msg = $_POST['msg'];

			$to = "amanbhatia2510@gmail.com";
			$subject = "Library Management System : User Request";
			$headers = "From : $row[0], $row[1]";
			$result = mail($to,$subject,$msg,$headers);

			if(!$result){
				echo mysql_error();
			}
	}
	else{
		echo "
		<p id=\"header\"> Hello $row[1], Tell Us Your Concern!  </p>
		<br/>
		<form method='post' action='./request.php?entry_no=$row[0]' >
			<textarea name='msg' rows='6' cols='50' placeholder='  What is this about?' /></textarea>
			<br/>
			<input class='button' type='submit' name='send' value='Send'>
		</form>
		";
	}

	mysql_close($server);
	?>
</body>
</html>