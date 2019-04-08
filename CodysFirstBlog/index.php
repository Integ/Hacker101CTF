<?php
	// ^FLAG^323ac2e274d345a3dc218d4aaad0f41d505200b49a801844561315c024ac535f$FLAG$
	mysql_connect("localhost", "root", "");
	mysql_select_db("level4");
	$page = isset($_GET['page']) ? $_GET['page'] : 'home.inc';
	if(strpos($page, ':') !== false && substr($page, 0, 5) !== "http:")
		$page = "home.inc";

	if(isset($_POST['body'])) {
		mysql_query("INSERT INTO comments (page, body, approved) VALUES ('" . mysql_real_escape_string($page) . "', '" . mysql_real_escape_string($_POST['body']) . "', 0)");
		if(strpos($_POST['body'], '<?php') !== false)
			echo '<p>^FLAG^4565931eb083f30b0ccb28c5d797e63796dae2466939c475d267acfd13ac02a5$FLAG$</p>';
?>
	<p>Comment submitted and awaiting approval!</p>
	<a href="javascript:window.history.back()">Go back</a>
<?php
		exit();
	}

	ob_start();
	include($page . ".php");
	$body = ob_get_clean();
?>
<!doctype html>
<html>
	<head>
		<title><?php echo $title; ?> -- Cody's First Blog</title>
	</head>
	<body>
		<h1><?php echo $title; ?></h1>
		<?php echo $body; ?>
		<br>
		<br>
		<hr>
		<h3>Comments</h3>
		<!--<a href="?page=admin.auth.inc">Admin login</a>-->
		<h4>Add comment:</h4>
		<form method="POST">
			<textarea rows="4" cols="60" name="body"></textarea><br>
			<input type="submit" value="Submit">
		</form>
<?php
	$q = mysql_query("SELECT body FROM comments WHERE page='" . mysql_real_escape_string($page) . "' AND approved=1");
	while($row = mysql_fetch_assoc($q)) {
		?>
		<hr>
		<p><?php echo $row["body"]; ?></p>
		<?php
	}
?>
	</body>
</html>