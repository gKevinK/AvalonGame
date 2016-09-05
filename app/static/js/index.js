$('#start-btn').click(function() {
    $.post('/start_new', {
        name: $('#name').val(),
        player_num: $('#player-num').val(),
        use_index: $('#use-index').is(':checked'),
        index: $('#index').val()
    }, function() {
        alert('moew');
        window.location.href = '/';
    });
    
});

$('#join-btn').click(function() {
    alert('Hello~');
});

$('#use-index').click(function() {
    if ($('#use-index').is(':checked')) {
        $('#index-field').hide();
    } else {
        $('#index-field').show();
    }
});

