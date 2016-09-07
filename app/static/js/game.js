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
    setTimeout(function() {
        comet();
    }, 1000);
});

var comet = function() {
    $.get('/game/comet', function(data) {
        alert(data);
        setTimeout(comet, 1000);
    })
}

$('#make-team').click(function() {
    $.post('/game/action', {
        action: 'make-team',
        content: []
    })
})

// Test
$('#test-message').click(function() {
    $.post('/game/action', {
        action: 'message',
        content: 'test-message'
    });
})