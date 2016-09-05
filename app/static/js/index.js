$('#start-btn').click(function() {
    $.post('/start-new');
    window.location.href = ''
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

