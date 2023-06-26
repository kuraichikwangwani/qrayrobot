<?php
// database connection code

$servername = "localhost";
$username = "username";
$password = "password";
$db = "dbname";

$con = mysqli_connect('$servername, $username, $password,$db');

if(isset($_POST['save']))
{
// get the post records
$username = $_POST['username'];
$password = $_POST['password'];
$phone_number = $_POST['phone_number'];

// database insert SQL code
$sql = "INSERT INTO `gonai_login` (`ID`, `username`, `password`, `phone_number`, `number_of_days_left`) VALUES (NULL, '$username', '$password', '$phone_number', '30')";

// insert in database 
$rs = mysqli_query($con, $sql);
if($rs)
{
	echo "Contact Records Inserted";
}

else
{
	echo "Are you a genuine visitor?";
	
}
?>
