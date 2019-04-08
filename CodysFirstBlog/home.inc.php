<p>Welcome to my blog!  I'm excited to share my thoughts with the world.  I have many important and controversial positions, which I hope to get across here.</p>

<?php
foreach(scandir("posts", 1) as $value) {
	if($value == "." || $value == "..") continue;
	ob_start();
	include("posts/" . $value);
	$body = ob_get_clean();
	?>
	<h2><?php echo $title; ?></h2>
	<?php
	echo $body;
}
?>

<?php $title = "Home"; ?>