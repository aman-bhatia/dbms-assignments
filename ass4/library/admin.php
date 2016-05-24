<!DOCTYPE HTML>
<head>
	<title>Library Management System</title>
	<link type="text/css" rel="stylesheet" href="css/stylesheet.css" />
	<link type="text/css" rel="stylesheet" href="jquery/css/ui-lightness/jquery-ui-1.10.4.custom.min.css" />
	<link href="js/fancybox/jquery.fancybox-1.3.4.css" rel="stylesheet" />

	<script src="js/jquery-1.7.2.min.js"></script>
	<script src="jquery/js/jquery-ui-1.10.4.custom.min.js" ></script>
	<script src="js/fancybox/jquery.fancybox-1.3.4.min.js"></script>
	<script>
		$(document).ready(function() {
			$('.iframe').fancybox({
				width : 900,
				height : 500
			});
			$("#dob").datepicker({
				changeMonth : true,
				changeYear : true
			});
			$("#grad_year").datepicker({
				changeMonth : true,
				changeYear : true
			});
		});
	</script>
</head>

<body>
	<br/>
	<p id="header"> Library Management System , IIT Delhi </p>
	<form method="post" action="admin.php" enctype="multipart/form-data">
	<br/>
	<!-- <div id="div_css"> -->
		<input class="button" type="submit" name="book" value="Books Database" />
		<input class="button" type="submit" name="trans" value="Manage Transactions" />
		<input class="button" type="submit" name="stud" value="Student Database" /><br /><br />
	<!-- </div> -->
	<!-- <div id="div_css" style="background: #eee;"> -->
	
<?php
	session_start();

	if (!isset($_SESSION['username'])){
		header('Location: ./index.php');
	}

	$server = mysql_connect('localhost','root','');
	// $server = mysql_connect('mysql.hostinger.in','u642211610_admin','col362');

	if(!$server) die("Unable to connect to MySQL: " . mysql_error());	

	$res = mysql_select_db('u642211610_lib');
	
	if(mysql_error()){
			echo mysql_error();
	}
	
	$book_buttons = "<input class='button' type='submit' name='ab' value='Add Books' />
					<input class='button' type='submit' name='db' value='Delete Books' />
					<input class='button' type='submit' name='vb' value='View Books' /><br /><br /><br />";
	
	if($_POST['book']){
		echo $book_buttons;
	}
	if($_POST['vb']){
		echo $book_buttons;
		$query = "SELECT * FROM books";
		$result = mysql_query($query);
		$num_rows = mysql_num_rows($result);
		if ($num_rows){
			echo "
					<table>
						<thead>
							<tr>
								<th> ISBN Code </th>
								<th> Title </th>
								<th> Author </th>
							</tr>
						</thead>";
			while ($rows = mysql_fetch_row($result)){
				echo "<tr>
						<td> $rows[0] </td>
						<td> $rows[2] </td>
						<td> $rows[1] </td>
					</tr>";
			};
			echo "</table>";
		} else {
			echo "
			<table>
				<tr>
					<td> No current enteries </td>
				</tr>
			</table>";
		}
	}

	if($_POST['ab']){
		echo $book_buttons;
		echo   "
			<table>
				<tr>
					<td> Book Title </td>
					<td> <input class='inputbox' type='text' name='btitle' /><br /> </td>
				</tr>
				<tr>
					<td> Book Author </td>
					<td> <input class='inputbox' type='text' name='bauthor' /><br /> </td>
				</tr>
				<tr>
					<td> ISBN Code </td>
					<td> <input class='inputbox' type='text' name='bisbn' /><br /> </td>
				</tr>
			</table>
			<input class='button' type='submit' name='addbooks' value='Submit' />";
	}
	
	if ($_POST['addbooks']){
		echo $book_buttons;
		$isbn = $_POST['bisbn'];
		$title = $_POST['btitle'];
		$author = $_POST['bauthor'];
		$query = "INSERT INTO books VALUES('$isbn','$author','$title')";
		$result = mysql_query($query);
		if(mysql_error()){
			echo "error";
			echo mysql_error();
		} else {
			echo "
			<table>
				<tr>
					<td>Your responses are saved to the database.</td>
				</tr>
			</table>
			";
		}
	}

	if($_POST['db']){
		echo $book_buttons;
		echo "
		<table>
			<tr>
				<td> Give the ISBN Code of the book </td>
				<td> <input class='inputbox' type='text' name='delisbn' /> </td>
			</tr>
		</table>
		<input class='button' type='submit' value='Delete Book'  name='delbook' />";
	}

	if($_POST['delbook']){
		echo $book_buttons;
		$delisbn = $_POST['delisbn'];
		
		$query = "DELETE FROM books WHERE isbn=$delisbn";
		$result=mysql_query($query);
		$num_rows_affected = mysql_affected_rows();

		if(!$result){
			$error_string = mysql_error();
			echo "
			<table>
				<tr>
					<td> The server says : $error_string </td>
				</tr>
			</table>";
		} else if ($num_rows_affected==0){
			echo "
			<table>
				<tr>
					<td> The server says : The book with given ISBN does not exist in the database. </td>
				</tr>
			</table>";
		} else {
			echo "
			<table>
				<tr>
					<td> The book with ISBN Code $delisbn is deleted from the database.</td>
				</tr>
			</table>
			";
		}
	}

	$trans_buttons = "<input class='button' type='submit' name='mtrans' value='New Transaction' />
					  <input class='button' type='submit' name='vtrans' value='View Transactions' /><br /><br />" ;
	
	if($_POST['trans']){
		echo $trans_buttons;
	}
	
	if ($_POST['mtrans']){
		echo $trans_buttons;
		echo  "
		<table>
			<tr>
				<td> Book ISBN Code </td>
				<td> <input class='inputbox' type='text' name='trans_isbn' /> </td>
			</tr>
			<tr>
				<td> Student Entry No. </td>
				<td> <input class='inputbox' type='text' name='trans_entry_no' /> </td>
			</tr>
			<tr>
				<td> Type of transaction </td>
				<td>
					<span style='font-size:1.1em'> Issue </span> <input class='inputbox' style='width:70px;' type='radio' name='transmode' value='Issue' />
					<br/><br/>
					<span style='font-size:1.1em'> Return </span> <input class='inputbox' style='width:50px;' type='radio' name='transmode' value='Return' />
				</td>
			</tr>
		</table>
		<input class='button' type='submit' name='maketrans' value='Make Transaction'  />";
	}

	if($_POST['maketrans']){
		echo $trans_buttons;
		$entry_no = $_POST['trans_entry_no'];
		$isbn = $_POST['trans_isbn'];
		$mode = $_POST['transmode'];
		$date = date("d-m-Y");

		if ($mode=='Issue'){
			$query = "SELECT * FROM transactions WHERE entry_no='$entry_no'";
			$result= mysql_query($query);
			if (mysql_num_rows($result) == 3){
				echo "
				<table>
					<tr>
						<td> The server says : Maximum book issue limit reached for this user. </td>
					</tr>
				</table>";
			} else {
				$query = "SELECT * FROM students WHERE entry_no='$entry_no'";
				$result= mysql_query($query);
				$diff = 1;
				if (mysql_num_rows($result)){
					$row = mysql_fetch_row($result);
					$date1= $row[5];
					$date2 = date("m/d/Y");
					$diff = strtotime($date1) - strtotime($date2);

					if ($diff < 0){
						echo "
						<table>
							<tr>
								<td> User's membership is expired! </td>
							</tr>
						</table>
						";
					}
				};

				if ($diff > 0){
					$query = "INSERT INTO transactions VALUES ('$isbn','$entry_no','$date')";
					$result= mysql_query($query);
					if(!$result){
						$error_string = mysql_error();
						echo "
						<table>
							<tr>
								<td> The server says : $error_string </td>
							</tr>
						</table>";
					
					} else {
						echo "<br />
						<table>
							<tr>
								<td> Your transaction was successful ! </td>
							</tr>
						</table>";
					}
				}
			}
		} else {		// mode='return'

			$query = "SELECT * FROM transactions WHERE ((isbn='$isbn') AND (entry_no='$entry_no'))";
			$result= mysql_query($query);
		
			if(mysql_num_rows($result)==0){
				echo "
				<table>
					<tr>
						<td> The server says : Illegal Transaction. Please provide Correct Input! </td>
					</tr>
				</table>";
			} else {
				$row = mysql_fetch_row($result);
				$date1 = $row[2];
				$date2 = date("d-m-Y");
				$diff = intval(((abs(strtotime($date2) - strtotime($date1))))*10/(24*60*60))+10;
				
				$query = "DELETE FROM transactions WHERE ((isbn='$isbn') AND (entry_no='$entry_no'))";
				$result= mysql_query($query);

				echo "<br />
				<table>
					<tr>
						<td> Your transaction was successful ! </td>
					</tr>
					<tr>
						<td> Charges : Rs. $diff </td>
					</tr>

				</table>";
			}
		}
	}

	if($_POST['vtrans']){
		echo $trans_buttons;
		$query = "SELECT * FROM transactions";
		$result = mysql_query($query);
		if(!$result){
			echo "<br />The server says : ".mysql_error();
		}
		$num_rows = mysql_num_rows($result);
		if ($num_rows){
			echo "  <br />
					<table>
						<thead>
							<tr>
								<th> Book ISBN Code </th>
								<th> Student Entry No.</th>
								<th> Date/time of Transaction </th>
							</tr>
						</thead>";
			while ($rows = mysql_fetch_row($result)){
				echo "<tr>
						<td> $rows[0] </td>
						<td> $rows[1] </td>
						<td> $rows[2] </td>
					</tr>";
			};
			echo "</table>";
		} else {
			echo "<br />
			<table>
				<tr>
					<td> No current enteries. </td>
				</tr>
			</table>
			";
		}
	}

	$stud_buttons = "<input class='button' type='submit' name='addstu' value='Add a Student Entry' />
					 <input class='button' type='submit' name='delstu' value='Delete a Student Entry' />
					 <input class='button' type='submit' name='viewstu' value='View Student Database' /><br /><br />";
	if($_POST['stud']){
		echo $stud_buttons;
	}
	if($_POST['viewstu']){
		echo $stud_buttons;
		$query = "SELECT * FROM students";
		$result = mysql_query($query);
		if(!$result){
			echo "The server says : ".mysql_error();
		}
		$num_rows = mysql_num_rows($result);
		if ($num_rows){
			echo "
					<table>
						<thead>
							<tr>
								<th> Entry No. </th>
								<th> Student Name </th>
								<th> Degree </th>
								<th> Email </th>
							</tr>
						</thead>";
			while ($rows = mysql_fetch_row($result)){
				echo "<tr>
						<td> <a rel='student' href='query.php?entry_no=$rows[0]' class='iframe' >$rows[0]</a> </td>
						<td> $rows[1] </td>
						<td> $rows[4] </td>
						<td> $rows[7] </td>
					</tr>";
			};
			echo "</table>";
		} else {
			echo "
				<table>
					<tr>
						<td> No current enteries. </td>
					</tr>
				</table>
				";
		}
	}
	if($_POST['addstu']){
		echo $stud_buttons;
		echo "
		<table>
			<tr>
				<td> Student Name </td>
				<td> <input class='inputbox' id='name' name='name' type='text' /> </td>
			</tr>

			<tr>
				<td> Entry Number </td>
				<td> <input class='inputbox' id='entry_no' name='entry_no' type='text' /> </td>
			</tr>

			<tr>
				<td> Gender </td>
				<td>
					Male <input type='radio' value='Male' name='gender' id='male' />
					Female <input id='female' value='Female' type='radio' name='gender'/>
				</td>
			</tr>
			
			<tr>
				<td>  Date of Birth </td>
				<td> <input class='inputbox' name='dob' id='dob' /> </td>
			</tr>
			
			<tr>
				<td> Degree </td>
				<td>
					<select class='inputbox' id='degree' name='degree'>
						<option value=''>Choose Degree</option>
						<option value='B.Tech'>B.Tech</option>
						<option value='M.Tech'>M.Tech</option>
						<option value='PhD'>PhD</option>
					</select>
				</td>
			</tr>

			<tr>
				<td> Membership Upto </td>
				<td> <input class='inputbox' name='grad_year' id='grad_year' /> </td>
			</tr>			
			
			<tr>
				<td> Mobile No. </td>
				<td> <input id='mob' name='mob' class='inputbox' /> </td>
			</tr>
			
			
			<tr>
				<td> Email Address </td>
				<td> <input id='email' class='inputbox' name='email' type='email' placeholder=' Your Email Address' /> </td>
			</tr>
		
			<tr>
				<td> Upload your photo </td>
				<td> <input type='file' id='photo' name='photo' /> </td>
			</tr>

			<tr>
				<td> Password </td>
				<td> <input type='password' id='pass' name='pass' /> </td>
			</tr>
		</table>
		<input class='button' type='submit' name='addstudent' value='Add Student Entry to Database' />
		<input class='button' type='reset' value='Reset Form' />
		";
	}
	if ($_POST['addstudent']){
		echo $stud_buttons;

		$name = $_POST['name'];
		$entry_no = $_POST['entry_no'];
		$gender = $_POST['gender'];
		$dob = $_POST['dob'];
		$degree = $_POST['degree'];
		$grad_year = $_POST['grad_year'];
		$mob = $_POST['mob'];
		$email = $_POST['email'];
		if ($_FILES['photo']['name']){
			$filetmp = $_FILES['photo']['tmp_name'];
			$filepath = './images/'.$_FILES['photo']['name'];

			move_uploaded_file($filetmp, $filepath);
		} else {
			$filepath =  "./images/photo.png";
		}
		$pass = $_POST['pass'];

		$query = "INSERT INTO students VALUES ('$entry_no','$name','$gender','$dob','$degree','$grad_year','$mob','$email','$filepath','$pass')";

		mysql_query($query);
		if(mysql_error()){
			echo mysql_error();
		}

		echo "
		<table>
			<tr>
				<td> Student Entry added Successfully! </td>
			</tr>
		</table>
		";
	}
	if ($_POST['delstu']){
		echo $stud_buttons;
		echo "
		<table>
			<tr>
				<td> Give the Entry Number of the student </td>
				<td> <input class='inputbox' type='text' name='del_entry_no'> </td>
			</tr>
		</table>
		<input class='button' type='submit' value='Delete Student Entry from Database' name='deletestu'>" ;
	}
	if($_POST['deletestu']){
		echo $stud_buttons;
		$del_entry_no = $_POST['del_entry_no'];

		$query = "DELETE FROM students WHERE entry_no='$del_entry_no'";
		$result=mysql_query($query);
		if (!$result){
			$error_string = mysql_error();
			echo "
				<table>
					<tr>
						<td> The server says : $error_string </td>
					</tr>
				</table>
				";
		} else if (mysql_affected_rows()==0){
			echo "
				<table>
					<tr>
						<td> The server says : Student does not exist in the database! </td>
					</tr>
				</table>
				";
		} else {
			echo "
				<table>
					<tr>
						<td> The Student Entry with entry no. $del_entry_no is deleted from the database. </td>
					</tr>
				</table>
				";
		}
	}
?>
<!-- </div> -->

</form>
</body>
</html>