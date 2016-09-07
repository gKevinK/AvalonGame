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
    setTimeout(init, 1000);
});
    
var init = function() {
    $.get('/game/init', function(data) {
        $('#message-box').append('<div>' + JSON.stringify(data) + '</div>');
        var content = data['content'];
        for (var i = 0; i < content.length; i += 1) content[i] += 1;
        info.role = data['role']
        info.role_name = config.Role[data['role']]
        info.player_id = data['player_id'] + 1
        info.known_player = content
        alert('我的身份：' + info.role_name + '\n\n'
            + '我的次序：' + info.player_id + '号\n\n'
            + '看到的玩家：'　+ info.known_player.join('，'));
    });
    setTimeout(comet, 1);
};

var comet = function() {
    $.get('/game/comet', function(data) {
        setTimeout(comet, 1);
        if (data == '') {
            setTimeout(comet, 1);
            return;
        }
        if (data['type'] == 'message') {
            $('#message-box').append('<div>Player ' + (data['sender'] + 1) + ": " + data['content'] + '</div>');
        } else if (data['type'] == 'player_info') {
            $('#make-team-panel').show();
        } else if (data['type'] == 'register') {
            $('#message-box').append('<div>Player ' + (data['player_id'] + 1) + ": " + data['name'] + ' 已加入。</div>');
        } else if (data['type'] == 'make-team') {
            $('#make-team-panel').show();
        } else if (data['type'] == 'team-vote') {

        } else if (data['type'] == 'task-vote') {

        } else if (date['type'] == 'mission-result') {
            var res = data['result'] ? '成功' : '失败';
            $('#message-box').append('<div>任务' + res + '，' + data['bad_vote_num'] + ' 张失败票。</div>');
        }
    })
}

$('#make-team-btn').click(function() {
    $('#make-team-panel').hide();
    $.post('/game/action', {
        action: 'make-team',
        content: []
    });
})

$('#team-vote-btn').click(function() {
    vote = $('input[name="team-vote"]:checked').val();
    $.post('/game/action', {
        action: 'team-vote',
        content: vote
    });
})

$('#task-vote').click(function() {
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
$('#test-message').click(function() {
    $.post('/game/action', {
        action: 'message',
        content: 'test-message'
    });
})