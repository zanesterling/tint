$(function() {
	var tintRepos = $.getJSON("https://api.github.com/users/tintapplication/repos?type=member");
	var shownRepos = $(".repo");

	for (var i = 0; i < tintRepos.length; i++) {
		for (var j = 0; j < shownRepos.length; j++) {
			if (tintRepos[i]['name'] == shownRepos[j].textContent()) {
				$(shownRepos[j]).addClass('tinted');
			}
		}
	}

	for (var i = 0; i < shownRepos.length; i++) {
		if (!$(shownRepos[j]).hasClass('tintified')) {
			$(shownRepos[j]).addClass('untinted');
		}
	}

	$('.repo').click(function(event) {
		if ($(event.target).hasClass('tinted'))
			return;

		a = event.target;
		$(event.target).removeClass('untinted');
		$(event.target).addClass('tinting');
		$.get(window.location.origin + '/client-callback',
			{
				'action': 'tint',
				'username': $('#username').text(),
				'repo': $(event.target).text()
			},
			function() {
				$(event.target).removeClass('tinting');
				$(event.target).addClass('tinted');
			}
		);
	});
});
