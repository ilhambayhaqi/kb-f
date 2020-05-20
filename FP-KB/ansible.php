<?php 
require_once("auth.php");
require_once("config.php");

if(!empty($_SESSION['message'])) {
   	$message = $_SESSION['message'];
	?>
		<script>alert("<?php echo $message ?>")</script>
	<?php
	$_SESSION['message'] = NULL;
}

$id = $_SESSION['user']['id'];
$username = $_SESSION['user']['username'];

?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
	<!-- Font Awesome -->
	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.11.2/css/all.css">
	<!-- Bootstrap core CSS -->
	<link href="css/bootstrap.min.css" rel="stylesheet">
  	<!-- Material Design Bootstrap -->
	<link href="css/mdb.min.css" rel="stylesheet">
	<link rel="stylesheet" href="css/styles3.css">
    <title>Ansible</title>
</head>
<body>	
	<div class="topnav" id="myTopnav">
		<a href="timeline.php">Home</a>
		<a href="edit.php">Edit</a>
		<a href="view.php">Users</a>
		<a href="ansible.php">Ansible</a>
		<a href="timeseries.php" class="active">Covid19</a>
		<a href="logout.php" class="out">Logout</a>
		<a href="javascript:void(0);" class="icon" onclick="myFunction()">
		<i class="fa fa-bars"></i>
 		</a>
	</div>

	
	<div class="split left">
		<div class="centered">
			<img src="img/<?php echo $_SESSION['user']['photo'] ?>" />
			<h3><?php echo  $_SESSION["user"]["name"] ?></h3>
			<p><?php echo $_SESSION["user"]["email"] ?></p>
		</div>
	</div>

	<div class="split right">
		<div class="box1">
			<h1>Ansible</h1>
			<h3> Error :( </h3>
			<p>Datanya ilang, lupa ga kesimpen</p>			
		</div>
	</div>
		

</body>
</html>