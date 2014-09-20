$.ready(function() {
	var tintRepos = $.getJSON("https://api.github.com/users/tintapplication/repos/?type=member");
	var shownRepos = $(".repo");

	for (var i = 0; i < tintRepos.length; i++) {
		for (var j = 0; j < shownRepos.length; j++) {
			if (tintRepos[i]['name'] == shownRepos[j].textContent()) {
				$(shownRepos[j]).addClass('tintified');
			}
		}
	}
});
