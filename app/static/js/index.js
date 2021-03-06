$('#start-btn').click(function() {
    if ($('#name').val().length < 4) {
        alert('昵称小于4字');
        return;
    }
    $.post('/start_new', {
        name: $('#name').val(),
        player_num: $('#player-num').val(),
        use_id: !($('#use-index').is(':checked')),
        player_id: $('#index').val()
    }, function(data) {
        if (data === '') {
            window.location.href = '/game';
        } else {
            alert('失败了...\n\n' + data);
        }
    });
});

$('#join-btn').click(function() {
    if ($('#name').val().length < 4) {
        alert('昵称小于4字');
        return;
    }
    $.post('/join', {
        name: $('#name').val(),
        room_id: $('#room-num').val(),
        use_id: !($('#use-index').is(':checked')),
        player_id: $('#index').val()
    }, function(data) {
        if (data === '') {
            window.location.href = '/game';
        } else {
            alert('失败了...\n\n' + data);
        }
    });
});

$('#use-index').click(function() {
    if ($('#use-index').is(':checked')) {
        $('#index-field').slideUp();
    } else {
        $('#index-field').slideDown();
    }
});

