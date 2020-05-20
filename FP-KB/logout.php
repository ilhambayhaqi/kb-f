<?php

session_start();
//session_unset("user");
//session_unset("output");
session_destroy();
header("Location: index.php");

?>