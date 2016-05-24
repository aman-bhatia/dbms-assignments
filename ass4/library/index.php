<!DOCTYPE HTML>
<head>
	<title>Library Management System</title>
	<link rel="stylesheet" href="css/alertify.core.css" />
	<link rel="stylesheet" href="css/alertify.default.css" />
	<link type="text/css" rel="stylesheet" href="css/stylesheet_index.css" />
	<link type="text/css" rel="stylesheet" href="jquery/css/ui-lightness/jquery-ui-1.10.4.custom.min.css" />
	<link href="js/fancybox/jquery.fancybox-1.3.4.css" rel="stylesheet" />

	<script src="js/jquery-1.7.2.min.js"></script>
	<script src="js/alertify.min.js"></script>
	<script src="jquery/js/jquery-ui-1.10.4.custom.min.js" ></script>
	<script src="js/fancybox/jquery.fancybox-1.3.4.min.js"></script>
	<script>
		$(document).ready(function() {
			$('.iframe').fancybox({
				width : 700,
				height : 350
			});
		});
	</script>

	<link rel="stylesheet" type="text/css" href="css/demo.css" />
    <link rel="stylesheet" type="text/css" href="css/style3.css" />
	<script type="text/javascript" src="js/modernizr.custom.86080.js"></script>

</head>

<body>
	<ul class="cb-slideshow">
		<li><span></span></li>
		<li><span></span></li>
		<li><span></span></li>
		<li><span></span></li>
		<li><span></span></li>
		<li><span></span></li>
	 </ul>

<div class='container'>
	<a href='./login_admin.php' class='iframe'> Administration Login </a>
	<a href='./login_user.php' class='iframe' style='float:left'> User Login </a>
	<!-- <br/> -->
	<br/>
	<br/>
	<!-- <p id="header">Library Management System, IIT Delhi</p> -->
	<form method="post" action="index.php" >
		<br/>
		<input id='input_box' name='search_string' type='text' placeholder=' Search Books ' />
		<input id='button' type='submit' name='search' value='Search' />
	</form>
	<br/>


<?php
	if ($_POST['search']){
		$search_string = $_POST['search_string'];

		$server = mysql_connect('localhost','root','');
		// $server = mysql_connect('mysql.hostinger.in','u642211610_admin','col362');

		if(!$server) die("Unable to connect to MySQL: " . mysql_error());	

		$res = mysql_select_db('u642211610_lib');
		
		if(mysql_error()){
				echo mysql_error();
		}

		$query = "SELECT * FROM books WHERE ((title LIKE '%$search_string%') OR (author LIKE '%$search_string%'))";
		if(mysql_error()){
				echo mysql_error();
		}

		$result = mysql_query($query);
		if(mysql_error()){
				echo mysql_error();
		}

		$num_rows = mysql_num_rows($result);
		if ($num_rows){
			echo "
					<div class='tbl-header'>

					<script>
						function checkAvail(x,avail){
							if (avail==0){
								alertify.alert('Book with ISBN code ' + x.toString() + ' is available');
							} else {
								alertify.alert('Book with ISBN code ' + x.toString() + ' is not available');
							}
						}
					</script>

					<table>
						<thead>
							<tr>
								<th> ISBN Code </th>
								<th> Title </th>
								<th> Author </th>
							</tr>
						</thead>
					</table>
					</div>
					<div class='tbl-content'>
					<table>";
			while ($rows = mysql_fetch_row($result)){
				
				$sub_query = "SELECT * FROM transactions WHERE isbn='$rows[0]'";
				$sub_result = mysql_query($sub_query);
				$avail = mysql_num_rows($sub_result);
				echo "
					<tr>
						<td> $rows[0] </td>
						<td> <a href='javascript:checkAvail($rows[0],$avail);' style='float:left'> $rows[2] </a> </td>
						<td> $rows[1] </td>
					</tr>";
			};
			echo "</table>
				</div>";
		} else {
			echo "
			<table>
				<tr>
					<td>Sorry, no books found!</td>
				</tr>
			</table>";
		}		

	}
?>
</div>
</body>