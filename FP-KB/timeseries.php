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

if(empty($_SESSION['output'])){
	$_SESSION['output'] = "Not Running";
	$_SESSION['boolViewAll'] = TRUE;
}
if(isset($_POST['generate'])) {
	$command = escapeshellcmd('timeseries.py');
	$output = shell_exec($command);
	//$output = 'Hehe';
	$_SESSION['output'] = $output;
	//echo $output;
	header("Location: timeseries.php");
}

if(isset($_POST['changeview'])){
	$_SESSION['boolViewAll'] = ! $_SESSION['boolViewAll'];
	header("Location: timeseries.php");
}
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
    <title>Covid19 Project</title>
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
			<h1>Covid Timeseries Project</h1>
			<?php  
				if($_SESSION['output'] == 'Not Running'){
					?>
					
					<div class="containerHehe">
					<img src=img/summary.png style="" height="400" width="auto" />
						<div class="text-block">
		    				<h4>Coba Generate dulu...</h4>
		  				</div>
		  			</div>
					
					<?php
				}
				else{
					if($_SESSION['boolViewAll'] == TRUE){
					?>

					<div id="comparison">
					  <figure>
					    <div id="divisor"></div>
					  </figure>
					  <input type="range" min="0" max="100" value="0" id="slider" oninput="moveDivisor()">
					</div>

					<?php
					}
					else{
					?>
					<div class="containerHehe">
						<img src=img/summaryPrediction.png height="400" width="auto" />
		  			</div>
					<?php
					}
				}
			?>
			<form method="post" enctype="multipart/form-data">
				<table>
					<tr>
						<th>
							<td><button class="btn blue-gradient" type="submit" name="generate"> Generate New Prediction</button></td>
						</th>
						<th>
							<?php
								if($_SESSION['output'] != 'Not Running'){
									if($_SESSION['boolViewAll'] == TRUE){
							?>
								<td><button class="btn blue-gradient" style="width: 250px" type="submit" name="changeview"> View Predicted</button></td>
							<?php
									}
									else{
							?>
								<td><button class="btn blue-gradient" style="width: 250px" type="submit" name="changeview"> View Confirmed All</button></td>
							<?php 
									}
								} 
							?>
						</th>
					</tr>
				</table>
				<p>Status</p>
				<textarea name="message" rows="8" cols="100"> <?php echo $_SESSION['output'] ?> </textarea>
			</form>
		</div>
	</div>

<script>
	var divisor = document.getElementById("divisor"),
	slider = document.getElementById("slider");
	function moveDivisor() { 
		divisor.style.width = slider.value+"%";
	}
</script>>

</body>
</html>

