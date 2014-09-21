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

	shownRepos.each(function (index, elt) {
		if (!$(elt).hasClass('tinted')) {
			$(elt).addClass('untinted');
		}
	});

	$('.repo').click(function(event) {
		targ = $(event.target);
		if (targ.hasClass('untinted')) {
			targ.removeClass('untinted');
			targ.addClass('tinting');
			$.get(window.location.origin + '/client-callback',
				{
					'action': 'tint',
					'username': $('#username').text(),
					'repo': targ.text()
				},
				function() {
					targ.removeClass('tinting');
					targ.addClass('tinted');
				}
			);
		} else if (targ.hasClass('tinted')) {
			targ.removeClass('tinted');
			targ.addClass('untinting');
			$.get(window.location.origin + '/client-callback',
				{
					'action': 'untint',
					'username': $('#username').text(),
					'repo': targ.text()
				},
				function() {
					targ.removeClass('untinting');
					targ.addClass('untinted');
				}
			);
		} else console.log(targ);
	});
});
