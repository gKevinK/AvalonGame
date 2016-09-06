$('#exit').click(function() {
    $.post('/exit', {
        exit: true
    }, function() {
        window.location.href = '/';
    });
});

