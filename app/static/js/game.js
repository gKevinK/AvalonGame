var config = {
    Role: {
        0: '梅林', 
        1: '派西维尔',
        2: '忠臣',
        3: '刺客',
        4: '莫甘娜',
        5: '莫德雷德',
        6: '奥伯伦',
        7: '爪牙'
    }
}

var info = {}

$('#exit').click(function() {
    $.post('/exit', {
        exit: true
    }, function() {
        window.location.href = '/';
    });
});

$(document).ready(function() {
    $('.action-panel').hide();
    setTimeout(init, 100);
});

function init() {
    $.get('/game/init', function(data) {
        $('#message-box').append('<div>' + JSON.stringify(data) + '</div>');
        var content = data['content'];
        for (var i = 0; i < content.length; i += 1) content[i] += 1;
        info.role = data['role'];
        info.role_name = config.Role[data['role']];
        info.player_id = data['player_id'] + 1;
        info.player_num = data['player_num'];
        info.known_player = content
        for (var i = 0; i < info.player_num; i += 1) {
            $('#make-team-field').append('<label class="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect" for="make-team-0">'
                + '<input type="checkbox" id="make-team-' + i + '" class="mdl-checkbox__input team-select">'
                + '<span class="mdl-checkbox__label">' + (i + 1) + '</span>'
                + '</label>');
        }
        alert('我的身份：' + info.role_name + '\n\n'
            + '我的次序：' + info.player_id + '号\n\n'
            + '看到的玩家：'　+ info.known_player.join('，'));
    });
    setTimeout(comet, 10);
};

function comet() {
    $.get('/game/comet', function(data) {
        setTimeout(comet, 10);
        if (data == '') return;
        if (data['type'] == 'message') {
            $('#message-box').append('<div>Player ' + (data['sender'] + 1) + ": " + data['content'] + '</div>');
        } else if (data['type'] == 'player_info') {
            
        } else if (data['type'] == 'register') {
            $('#message-box').append('<div>Player ' + (data['player_id'] + 1) + ": " + data['name'] + ' 已加入。</div>');
        } else if (data['type'] == 'make-team') {
            $('#make-team-panel').show();
            alert(data['num']);
        } else if (data['type'] == 'team-vote') {
            $('#team-vote-panel').show();
        } else if (data['type'] == 'task-vote') {
            $('#task-vote-panel').show();
        } else if (data['type'] == 'mission-result') {
            var res = data['result'] ? '成功' : '失败';
            $('#message-box').append('<div>任务' + res + '，' + data['bad_vote_num'] + ' 张失败票。</div>');
        } else {
            $('#message-box').append('<div>' + JSON.stringify(data) + '</div>');
        }
    })
}

function add_message(sender, content) {
    $('#message-box').append('');
}

$('#make-team-btn').click(function() {
    $('#make-team-panel').slideUp();
    content = $('.team-select:checked').
    $.post('/game/action', {
        action: 'make-team',
        content: []
    });
})

$('#team-vote-btn').click(function() {
    $('#team-vote-panel').hide();
    vote = $('input[name="team-vote"]:checked').val();
    $.post('/game/action', {
        action: 'team-vote',
        content: vote
    });
})

$('#task-vote').click(function() {
    $('#task-vote-panel').hide();
    vote = $('input[name="task-vote"]:checked').val();
    $.post('/game/action', {
        action: 'task-vote',
        content: vote
    });
})

$('#assassin').click(function() {
    $.post('/game/action', {
        action: 'assasin',
        content: []
    })
})

$('#info').click(function() {
    alert('我的身份：' + info.role_name + '\n\n'
        + '我的次序：' + info.player_id + '号\n\n'
        + '看到的玩家：'　+ info.known_player.join('，'));
})

// Test
$('#send-message').click(function() {
    $.post('/game/action', {
        action: 'message',
        content: $('#message-content').val()
    });
})