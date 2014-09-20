$(function() {
	var tintRepos = $.getJSON("https://api.github.com/users/tintapplication/repos?type=member");
	var shownRepos = $(".repo");

	for (var i = 0; i < tintRepos.length; i++) {
		for (var j = 0; j < shownRepos.length; j++) {
			if (tintRepos[i]['name'] == shownRepos[j].textContent()) {
				$(shownRepos[j]).addClass('tintified');
			}
		}
	}

	$('.repo').click(function(event) {
		if ($(event.target).hasClass('tintified'))
			return;

		a = event.target;
		$(event.target).addClass('tinting');
		$.get(window.location.origin + '/client-callback',
			{
				'action': 'tint',
				'username': $('#username').text(),
				'repo': $(event.target).text()
			},
			function() {
				$(event.target).addClass('tinted');
				$(event.target).removeClass('tinting');
			}
		);
	});
});
