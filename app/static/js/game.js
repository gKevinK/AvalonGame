$('#exit').click(function() {
    $.post('/exit', {
        exit: true
    }, function() {
        window.location.href = '/';
    });
});

$(document).ready(function() {
    $.get('/game/init', function(data) {
        init_info = JSON.parse(data);
        alert(data);
    });
});

